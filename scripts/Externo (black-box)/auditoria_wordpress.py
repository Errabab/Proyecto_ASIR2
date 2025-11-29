"""
Script avanzado de auditoría externa para un sitio WordPress:
- Rastrea URLs internas y elimina duplicados.
- Analiza estado HTTP, títulos y meta descripciones.
- Detecta tema activo y plugins visibles.
- Revisa API REST, directorios abiertos y archivos sensibles.
- Intenta identificar accesos sin permisos.
- Genera un informe de texto bonito y visual, igual que en consola.
"""

import requests
from bs4 import BeautifulSoup
import re

WORDPRESS_URL = "http://52.2.136.15"
INFORME_FILE = "informe_auditoria_wordpress.txt"

requests.packages.urllib3.disable_warnings()

# ---------------------- CRAWLER --------------------------

def normalizar_url(url):
    if url.endswith("/"):
        return url[:-1]
    return url

def obtener_paginas_internas(url):
    paginas = set()
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.startswith("/"):
                href = url + href
            if href.startswith(url):
                paginas.add(normalizar_url(href))
    except:
        pass
    return paginas

# ---------------------- ANÁLISIS --------------------------

def analizar_pagina(url):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        titulo = soup.title.string if soup.title else "Sin título"
        meta = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta["content"] if meta else "Sin meta descripción"

        return {
            "status": r.status_code,
            "titulo": titulo,
            "descripcion": meta_desc
        }
    except:
        return {"status": "Error", "titulo": "N/A", "descripcion": "N/A"}

def detectar_tema(url):
    try:
        r = requests.get(url, timeout=10)
        return list(set(re.findall(r"wp-content/themes/([^/]+)/", r.text)))
    except:
        return []

def detectar_plugins(url):
    plugins = []
    try:
        r = requests.get(url + "/wp-content/plugins/", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            for link in soup.find_all("a", href=True):
                if not link["href"].startswith("?"):
                    name = link["href"].strip("/")
                    plugins.append(name)
    except:
        pass
    return plugins

def api_rest_activa(url):
    try:
        r = requests.get(url + "/wp-json/", timeout=10)
        return r.status_code == 200
    except:
        return False

# ---------------------- SEGURIDAD --------------------------

def probar_archivos_sensibles(url):
    archivos = [
        "wp-config.php", "readme.html", "xmlrpc.php", ".git/", "_backup/",
        "wp-content/debug.log"
    ]
    resultados = {}
    for archivo in archivos:
        try:
            r = requests.get(url + "/" + archivo, timeout=5)
            resultados[archivo] = r.status_code
        except:
            resultados[archivo] = "Error"
    return resultados

def probar_directorios(url):
    dirs = ["wp-content/uploads/", "wp-includes/", "wp-admin/"]
    resultado = {}
    for d in dirs:
        try:
            r = requests.get(url + "/" + d, timeout=5)
            resultado[d] = r.status_code
        except:
            resultado[d] = "Error"
    return resultado

def enumerar_usuarios(url):
    try:
        r = requests.get(url + "/?author=1", allow_redirects=True, timeout=10)
        if "author" in r.url:
            usuario = r.url.split("/author/")[-1].replace("/", "")
            return usuario
        return None
    except:
        return None

# ---------------------- GENERAR INFORME --------------------------

def generar_informe(paginas, tema, plugins, api, usuario, archivos, directorios, archivo_salida):
    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write("🔍 Iniciando auditoría avanzada de WordPress...\n\n")
        for p in paginas:
            info = analizar_pagina(p)
            f.write("="*60 + "\n")
            f.write(f"📌 TÍTULO: {info['titulo']}\n")
            f.write(f"🌐 URL: {p}\n")
            f.write(f"📶 Estado HTTP: {info['status']}\n")
            f.write(f"📝 Meta descripción: {info['descripcion']}\n")
            f.write(f"🎨 Tema activo: {', '.join(tema) if tema else 'No detectado'}\n")
            f.write(f"🔌 Plugins visibles: {', '.join(plugins) if plugins else 'Ninguno detectado'}\n")
            f.write(f"🔗 API REST activa: {api}\n")
            f.write(f"👤 Usuario filtrado: {usuario if usuario else 'Ninguno'}\n")
            f.write("⚠ Archivos sensibles:\n")
            for archivo, estado in archivos.items():
                f.write(f"   - {archivo}: {estado}\n")
            f.write("📂 Directorios abiertos:\n")
            for d, estado in directorios.items():
                f.write(f"   - {d}: {estado}\n")
            f.write("="*60 + "\n\n")
        f.write("✅ Auditoría finalizada.\n")
    print(f"✅ Auditoría finalizada. Informe generado: {archivo_salida}")

# ---------------------- EJECUCIÓN --------------------------

paginas = obtener_paginas_internas(WORDPRESS_URL)
tema = detectar_tema(WORDPRESS_URL)
plugins = detectar_plugins(WORDPRESS_URL)
api = api_rest_activa(WORDPRESS_URL)
archivos = probar_archivos_sensibles(WORDPRESS_URL)
directorios = probar_directorios(WORDPRESS_URL)
usuario = enumerar_usuarios(WORDPRESS_URL)

generar_informe(paginas, tema, plugins, api, usuario, archivos, directorios, INFORME_FILE)
