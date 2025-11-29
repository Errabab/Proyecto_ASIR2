#!/usr/bin/env python3
"""
Módulo de auditoría externa de WordPress: análisis de headers HTTP de seguridad.

- Realiza peticiones a la URL pública y obtiene headers HTTP.
- Comprueba headers de seguridad importantes:
  X-Frame-Options, X-Content-Type-Options, Strict-Transport-Security,
  Content-Security-Policy, Referrer-Policy, Permissions-Policy, Server.
- Reporta si faltan o están configurados correctamente.
- 100% legal y seguro: análisis externo, tipo black-box.
"""

import requests

HEADERS_SEGUROS = [
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "Referrer-Policy",
    "Permissions-Policy",
    "Server"
]

def analizar_headers(url):
    print("🔍 Iniciando análisis de headers de seguridad HTTP...\n")
    try:
        r = requests.get(url, timeout=5)
        headers = r.headers
    except requests.exceptions.RequestException as e:
        print(f"❌ No se pudo acceder a la URL: {e}")
        return

    print("============================================================")
    print(f"🌐 URL analizada: {url}")
    print("============================================================")
    for header in HEADERS_SEGUROS:
        valor = headers.get(header)
        if valor:
            print(f"✔ {header}: {valor}")
        else:
            print(f"⚠ {header}: NO configurado")
    print("============================================================")
    print("✅ Análisis de headers completado.\n")

# ------------------------------
# EJEMPLO DE USO
# ------------------------------
if __name__ == "__main__":
    analizar_headers("http://52.2.136.15")

