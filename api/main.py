from fastapi import FastAPI, Request
import json
import sys
sys.path.append(".")
from ai_engine.ollama_client import analyze_alert

app = FastAPI(title="ARIA - Automated Response & Intelligence Analyst")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "ARIA"}

@app.post("/api/v1/ingest")
async def ingest_alert(request: Request):
    alert = await request.json()
    print(f"[ARIA] Alerta recibida: {alert.get('rule', {}).get('description', 'sin descripción')}")
    
    print("[ARIA] Enviando a Ollama...")
    try:
        analysis = analyze_alert(alert)
        print(f"[ARIA] Análisis completado: {json.dumps(analysis, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"[ARIA] Error en análisis: {e}")
        analysis = {"error": str(e)}
    
    return {"status": "received", "analysis": analysis}