# ARIA — Automated Response & Intelligence Analyst

> SOC inteligente que analiza alertas de seguridad en tiempo real usando IA local.

ARIA conecta Wazuh SIEM con un LLM local (Mistral via Ollama) para analizar automáticamente cada alerta de seguridad, mapear tácticas MITRE ATT&CK, calcular el reisgo y generar recomendaciones de respuesta.

Sin enviar datos a servicios externos para asegurar máxima privacidad

---

## Arquitectura

```
Endpoints (agentes Wazuh Ubuntu y Windows)
Configurados con IDS (Suricata), FIM, reglas YARA y Threat Huntig (Virus total)
        ↓
   Wazuh Manager     ← VM Ubuntu Server 22.04   
        ↓
   Webhook (HTTP POST)
        ↓
   FastAPI Backend   ← ARIA core
   /api/v1/ingest    ← recibe alertas
        ↓
   Ollama (Mistral)  ← LLM local
        ↓
   Análisis + MITRE mapping + Threat Score
```

---

## Stack tecnológico

| Componente | Tecnología |
|---|---|
| SIEM | Wazuh |
| Backend | Python + FastAPI |
| LLM | Mistral via Ollama (local) |
| Threat Intel | VirusTotal API |
| IDS de red | Suricata |
| FIM | Wazuh Syscheck + YARA |
| Endpoints | Agentes Wazuh (Windows + Linux) |

---

## Funcionalidades implementadas

- Webhook en tiempo real desde Wazuh hacia ARIA
- Análisis automático de alertas con LLM local
- Explicación en lenguaje natural de cada evento
- Mapeo a tácticas y técnicas MITRE ATT&CK
- Threat scoring: LOW / MEDIUM / HIGH / CRITICAL
- Detección de falsos positivos
- Integración con VirusTotal para análisis de ficheros (FIM)
- File Integrity Monitoring en Windows y Linux
- Agentes Wazuh en Windows 11 y Ubuntu Desktop

---

## Fases

- [x]  1 — Infraestructura base + Webhook
- [x]  2 — LLM local + análisis de alertas

---

## Instalación

### Requisitos previos

- Python
- Wazuh instalado y corriendo
- Ollama instalado con modelo Mistral (`ollama pull mistral`)
- Wazuh configurado con webhook a `http://<IP>:8000/api/v1/ingest`

### Setup

```bash
git clone https://github.com/JorgeGonzalezVlc/ARIA.git
cd ARIA
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r api/requirements.txt
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Configuración del webhook en Wazuh e integracion de VirusTotal

Wazuh tiene una excelente documentacion por lo que animo a echar un ojo para configurarlo de manera personalizada. 
[Documentacion Wazuh](https://documentation.wazuh.com/current/index.html)

En este Reedme me centraré en aquellos pasos que puediesen ser menos frecunetes

Añadir en `/var/ossec/etc/ossec.conf`:

```xml
<integration>
  <name>custom-aria</name>
  <hook_url>http://<IP-ARIA>:8000/api/v1/ingest</hook_url>
  <level>3</level>
  <alert_format>json</alert_format>
</integration>

<integration>
     <name>virustotal</name>
     <api_key>xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx</api_key>
     <group>syscheck</group>
     <alert_format>json</alert_format>
</integration>
```

Segundo paso para webhook; necesitamos crear el script en `/var/ossec/integrations/custom-aria`:
Lee la alerta que Wazuh ha dejado en un fichero temporal y la manda por HTTP POST a ARIA, importante tener una ip fija para esto.

```python
#!/usr/bin/env python3
import sys, json, requests

with open(sys.argv[1]) as f:
    alert = json.load(f)

requests.post("http://direccion_ip_donde_corre_aria:8000/api/v1/ingest", json=alert, timeout=5)
```

```bash
sudo chmod +x /var/ossec/integrations/custom-aria
sudo chown root:wazuh /var/ossec/integrations/custom-aria
sudo systemctl restart wazuh-manager
```

## Proximos pasos

- Limpiar el resultado y la visualizacion
- Prevenir falsos positivos
- Crear base de datos con los resultados
- Resumen semanal de resultados


## Demo

### Ejemplo comprobaciond e archivo
<img width="1499" height="261" alt="Captura de pantalla 2026-06-02 195711" src="https://github.com/user-attachments/assets/42eb00eb-9393-42f9-90c7-c6be4a31fbfe" />
<img width="2539" height="1015" alt="Captura de pantalla 2026-06-02 195831" src="https://github.com/user-attachments/assets/020ab817-4437-4716-9057-ea84cbe5b93f" />

### Ejemplo intento de inicio de sesion fallido
<img width="1546" height="264" alt="Captura de pantalla 2026-06-02 195942" src="https://github.com/user-attachments/assets/032b3e23-d3a6-4dd0-b375-26511aefeefb" />
<img width="1229" height="1189" alt="Captura de pantalla 2026-06-02 200036" src="https://github.com/user-attachments/assets/93c33f0c-8a47-46e9-ba6a-3f284ec25f48" />




---

## Autor

**Jorge González** — Junior Cybersecurity Analyst  
[LinkedIn](https://linkedin.com/in/jorgegonzalezvlc) · [Portfolio](https://jorgegonzalezvlc.github.io)
