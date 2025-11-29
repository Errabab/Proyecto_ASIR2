#!/usr/bin/env python3
"""
Módulo de auditoría externa de WordPress: análisis de puertos HTTP accesibles.

- Comprueba si el servidor web está escuchando en puertos HTTP/HTTPS comunes:
  80, 443, 8080, 8443, 8000, 8001, 8888, 2082, 2083, 2095, 2096
- Solo utiliza peticiones externas (HTTP/HTTPS), sin acceso a la máquina del servidor.
- Indica cuáles son accesibles y su estado HTTP.
- Sirve para detectar posibles puertos web expuestos que puedan suponer un riesgo de seguridad.
- 100% legal y seguro: análisis externo, tipo black-box.
"""
import requests
from urllib.parse import urlparse

# ------------------------------
#  CONFIGURACIÓN DE PUERTOS A ANALIZAR
# ------------------------------
PUERTOS_HTTP = [80, 443, 8080, 8443, 8000, 8001, 8888, 2082, 2083, 2095, 2096]

def comprobar_puerto(domain, port):
    protocolos = ["http", "https"]

    for protocolo in protocolos:
        url = f"{protocolo}://{domain}:{port}"
        try:
            respuesta = requests.get(url, timeout=3)
            return (url, respuesta.status_code)
        except requests.exceptions.RequestException:
            continue
    return None

# ------------------------------
#  EJECUCIÓN PRINCIPAL
# ------------------------------
def analizar_puertos(url):
    print("🔍 Iniciando análisis de puertos HTTP accesibles...\n")

    domain = urlparse(url).hostname
    resultados = []

    for puerto in PUERTOS_HTTP:
        print(f"⏳ Probando puerto {puerto}...")
        resultado = comprobar_puerto(domain, puerto)

        if resultado:
            resultados.append(resultado)
            print(f"   ✔ Puerto accesible → {resultado[0]}  (Estado: {resultado[1]})")
        else:
            print(f"   ❌ No accesible")

    print("\n============================================================")
    print("🔎 RESULTADOS DEL ANÁLISIS DE PUERTOS")
    print("============================================================")

    if not resultados:
        print("✔ No se encontraron puertos HTTP alternativos accesibles. Buen nivel de seguridad.")
    else:
        print("⚠ Puertos web alternativos accesibles encontrados:")
        for url, code in resultados:
            print(f" - {url}   → Estado HTTP {code}")

    print("\n✅ Análisis completado.")
    return resultados

# ------------------------------
# EJEMPLO DE USO
# ------------------------------
if __name__ == "__main__":
    analizar_puertos("http://52.2.136.15")
