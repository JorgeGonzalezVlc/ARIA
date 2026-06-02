import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"

def analyze_alert(alert: dict) -> dict:
    prompt = f"""Eres un analista SOC senior. Analiza esta alerta de seguridad y responde ÚNICAMENTE en JSON válido, sin texto adicional, sin markdown, sin backticks.

ALERTA:
{json.dumps(alert, indent=2)}

Responde SOLO con este JSON:
{{
  "what_happened": "qué ocurrió en lenguaje claro",
  "why_dangerous": "por qué es peligroso",
  "impact": "impacto potencial",
  "false_positive_probability": 0.0,
  "mitre_tactic": "nombre de la táctica",
  "mitre_technique": "T1XXX",
  "threat_score": "LOW|MEDIUM|HIGH|CRITICAL",
  "recommendations": ["acción 1", "acción 2"]
}}"""

    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })

    result = response.json()
    text = result.get("response", "").strip()
    
    # Limpia markdown si lo hay
    text = text.replace("```json", "").replace("```", "").strip()
    
    try:
        text = text.replace("```json", "").replace("```", "").strip()
        
        # Encuentra el JSON
        start = text.find("{")
        end = text.rfind("}") + 1
        if start == -1 or end == 0:
            return {"error": "No se encontró JSON", "raw": text}
        
        json_str = text[start:end]
        
        # Decodifica \n y \" literales
        json_str = json_str.encode().decode('unicode_escape').encode('latin1').decode('utf-8')
        
        return json.loads(json_str)
    except Exception as e:
        return {"error": f"Parse error: {e}", "raw": text}