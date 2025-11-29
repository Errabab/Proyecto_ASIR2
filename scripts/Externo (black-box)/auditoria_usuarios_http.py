#!/usr/bin/env python3
"""
Módulo de auditoría externa de WordPress: enumeración avanzada de usuarios.

- Detecta usuarios públicos de WordPress de forma legal, usando:
    - URLs de autor (/author/{id})
    - API REST /wp-json/wp/v2/users
- Solo hace peticiones HTTP/HTTPS, tipo black-box, sin acceso a la máquina.
- Reporta los nombres de usuario encontrados y posibles riesgos.
"""

import requests

# ------------------------------
# CONFIGURACIÓN DE USUARIOS COMUNES A PROBAR
# ------------------------------
USUARIOS_COMUNES = ["admin", "editor", "test", "root", "user"]

def comprobar_autores(url):
    print("🔍 Iniciando enumeración de usuarios...\n")
    domain = url.rstrip("/")
    encontrados = []

    # 1️⃣ Intentar usuarios comunes
    for user in USUARIOS_COMUNES:
        author_url = f"{domain}/author/{user}/"
        try:
            r = requests.get(author_url, timeout=5, allow_redirects=True)
            if r.status_code == 200:
                encontrados.append(user)
                print(f"✔ Usuario detectado: {user} (URL: {author_url})")
        except requests.exceptions.RequestException:
            continue

    # 2️⃣ Intentar API REST si existe
    api_url = f"{domain}/wp-json/wp/v2/users"
    try:
        r = requests.get(api_url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            for usuario in data:
                username = usuario.get("slug")
                if username and username not in encontrados:
                    encontrados.append(username)
                    print(f"✔ Usuario detectado vía API: {username}")
    except requests.exceptions.RequestException:
        pass
    except ValueError:
        pass  # JSON no válido o API deshabilitada

    if not encontrados:
        print("⚠ No se detectaron usuarios públicos.")
    print("\n✅ Enumeración de usuarios completada.")
    return encontrados

# ------------------------------
# EJEMPLO DE USO
# ------------------------------
if __name__ == "__main__":
    usuarios = comprobar_autores("http://52.2.136.15")
