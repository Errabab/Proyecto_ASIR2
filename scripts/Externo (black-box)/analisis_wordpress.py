"""
Script para analizar un sitio WordPress:
- Rastrea páginas internas.
- Obtiene título, meta descripción y estado HTTP de cada página.
- Detecta el tema activo y si la API REST está habilitada.
- Muestra los resultados en consola para análisis rápido del sitio.
"""

import requests
from bs4 import BeautifulSoup
import re

WORDPRESS_URL = "http://52.2.136.15"

def obtener_paginas_internas(url):
    """Rastrea enlaces internos del sitio"""
    paginas = set()
    try:
        respuesta = requests.get(url, timeout=10)
        soup = BeautifulSoup(respuesta.text, "html.parser")
        for enlace in soup.find_all("a", href=True):
            href = enlace["href"]
            if href.startswith(url) or href.startswith("/"):
                if href.startswith("/"):
                    href = url + href
                paginas.add(href)
    except:
        pass
    return paginas

def analizar_pagina(url):
    """Analiza título, meta descripción y estado HTTP"""
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        titulo = soup.title.string if soup.title else "Sin título"
        meta_desc = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta_desc["content"] if meta_desc else "Sin meta descripción"

        return {
            "url": url,
            "status": r.status_code,
            "titulo": titulo,
            "descripcion": meta_desc
        }
    except:
        return {
            "url": url,
            "status": "Error",
            "titulo": "N/A",
            "descripcion": "N/A"
        }

def detectar_plugins(url):
    """Detecta plugins visibles desde /wp-content/plugins/"""
    plugins = []
    try:
        r = requests.get(url + "/wp-content/plugins/", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            for link in soup.find_all("a", href=True):
                if "/" in link["href"] and not link["href"].startswith("?"):
                    plugins.append(link["href"].replace("/", ""))
    except:
        pass
    return plugins

def detectar_tema(url):
    """Detecta el theme desde wp-content/themes"""
    try:
        r = requests.get(url, timeout=10)
        temas = re.findall(r"wp-content/themes/([^/]+)/", r.text)
        return list(set(temas))
    except:
        return []

def api_rest_activa(url):
    """Verifica si la API REST está activa"""
    try:
        r = requests.get(url + "/wp-json/", timeout=10)
        return r.status_code == 200
    except:
        return False

# --- EJECUCIÓN PRINCIPAL ---
print("🔍 ANALIZANDO WORDPRESS EN:", WORDPRESS_URL)

paginas = obtener_paginas_internas(WORDPRESS_URL)
print("\n📄 Páginas encontradas:")
for p in paginas:
    print(" -", p)

print("\n📌 Análisis de páginas:")
for p in paginas:
    info = analizar_pagina(p)
    print(f"\n➡ {info['url']}")
    print("  Estado:", info["status"])
    print("  Título:", info["titulo"])
    print("  Meta:", info["descripcion"])

print("\n🔌 Plugins detectados:")
print(detectar_plugins(WORDPRESS_URL))

print("\n🎨 Tema detectado:")
print(detectar_tema(WORDPRESS_URL))

print("\n🔗 API REST activa:")
print(api_rest_activa(WORDPRESS_URL))
