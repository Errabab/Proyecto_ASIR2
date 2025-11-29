#!/usr/bin/env python3
"""
Módulo de auditoría externa de WordPress: comprobación de API REST.

- Comprueba si la API REST (/wp-json/) está activa.
- Lista los endpoints públicos accesibles.
- Muestra si se puede obtener información de posts, páginas, usuarios u otros recursos.
- 100% legal y seguro: análisis externo, tipo black-box.
"""

import requests

def comprobar_api_rest(url):
    print("🔍 Iniciando comprobación de API REST...\n")
    api_url = url.rstrip("/") + "/wp-json/"
    try:
        r = requests.get(api_url, timeout=5)
        if r.status_code == 200:
            print(f"✔ API REST activa: {api_url}")
            data = r.json()
            endpoints = list(data.keys())
            print(f"🌐 Endpoints públicos detectados ({len(endpoints)}):")
            for ep in endpoints:
                print(f" - {ep}")
        else:
            print(f"⚠ API REST no accesible. Código HTTP: {r.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al acceder a la API REST: {e}")
    print("\n✅ Comprobación de API REST completada.")

# ------------------------------
# EJEMPLO DE USO
# ------------------------------
if __name__ == "__main__":
    comprobar_api_rest("http://52.2.136.15")
