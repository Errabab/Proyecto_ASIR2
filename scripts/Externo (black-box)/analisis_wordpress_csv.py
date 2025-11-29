"""
Script para analizar un sitio WordPress desde fuera:
- Rastrea páginas internas.
- Obtiene título, meta descripción y estado HTTP de cada página.
- Detecta el tema activo y si la API REST está habilitada.
- Genera un informe CSV con todos los datos para análisis SEO y estructural.
"""
"""
formato del csv
URLS,estado del http, titulo,descripcion,tema, api rest

"""

import requests
from bs4 import BeautifulSoup
import re
import csv

WORDPRESS_URL = "http://52.2.136.15"
CSV_FILE = "informe_wordpress.csv"

def obtener_paginas_internas(url):
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

def detectar_tema(url):
    try:
        r = requests.get(url, timeout=10)
        temas = re.findall(r"wp-content/themes/([^/]+)/", r.text)
        return list(set(temas))
    except:
        return []

def api_rest_activa(url):
    try:
        r = requests.get(url + "/wp-json/", timeout=10)
        return r.status_code == 200
    except:
        return False

# --- EJECUCIÓN ---
print("🔍 Analizando WordPress en:", WORDPRESS_URL)

paginas = obtener_paginas_internas(WORDPRESS_URL)
tema = detectar_tema(WORDPRESS_URL)
api = api_rest_activa(WORDPRESS_URL)

# Crear CSV
with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["URL", "Estado HTTP", "Título", "Meta descripción", "Tema", "API REST"])
    
    for p in paginas:
        info = analizar_pagina(p)
        writer.writerow([
            info["url"],
            info["status"],
            info["titulo"],
            info["descripcion"],
            ", ".join(tema),
            api
        ])

print(f"✅ Informe generado: {CSV_FILE}")
