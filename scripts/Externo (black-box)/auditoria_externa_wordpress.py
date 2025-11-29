#!/usr/bin/env python3
"""
Auditoría externa de WordPress (black-box):

- Analiza puertos HTTP accesibles
- Verifica headers de seguridad
- Enumera usuarios públicos (si existen)
- Comprueba la API REST y sus endpoints
- Revisa archivos sensibles
- Detecta directorios abiertos
- Evalúa riesgos básicos
- Detecta redirecciones y flujo HTTP
- Genera un informe bonito con colores y símbolos
"""

import requests

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    INFO = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

PUERTOS_HTTP = [80, 443, 8080, 8443, 8000, 8001, 8888, 2082, 2083, 2095, 2096]
USUARIOS_COMUNES = ["admin", "editor", "test", "root", "user"]
ARCHIVOS_SENSIBLES = [
    "wp-config.php", "readme.html", "xmlrpc.php", ".git/", "_backup/", "wp-content/debug.log"
]
DIRECTORIOS_ABIERTOS = [
    "wp-content/uploads/", "wp-includes/", "wp-admin/"
]

# ==============================
# Función para escribir informe
# ==============================
def escribir_informe(contenido, nombre_archivo="informe_auditoria_externa.txt"):
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(contenido)
    print(f"\n{Colors.OK}📁 Informe generado:{Colors.END} {nombre_archivo}")

# ==============================
# 1️⃣ Comprobación de puertos
# ==============================
def analizar_puertos(url):
    resultado = f"{Colors.HEADER}🔍 Puertos HTTP accesibles:{Colors.END}\n"
    accesibles = []
    for puerto in PUERTOS_HTTP:
        prueba_url = f"{url}:{puerto}" if puerto not in [80, 443] else url
        try:
            r = requests.get(prueba_url, timeout=3, allow_redirects=True)
            if r.status_code < 400:
                accesibles.append((prueba_url, r.status_code))
                resultado += f"  {Colors.OK}✔{Colors.END} {prueba_url}  (Estado: {r.status_code})\n"
        except requests.exceptions.RequestException:
            continue
    if not accesibles:
        resultado += f"  {Colors.WARNING}⚠ No se detectaron puertos HTTP accesibles.{Colors.END}\n"
    return resultado, accesibles

# ==============================
# 2️⃣ Análisis de headers
# ==============================
def analizar_headers(url):
    resultado = f"\n{Colors.HEADER}🔍 Headers de seguridad para {url}:{Colors.END}\n"
    try:
        r = requests.get(url, timeout=5)
        headers = r.headers
        for header in ["X-Frame-Options", "X-Content-Type-Options",
                       "Strict-Transport-Security", "Content-Security-Policy",
                       "Referrer-Policy", "Permissions-Policy", "Server"]:
            valor = headers.get(header, None)
            if valor is None:
                resultado += f"  {Colors.WARNING}⚠ {header}: NO configurado{Colors.END}\n"
            else:
                resultado += f"  {Colors.OK}✔ {header}: {valor}{Colors.END}\n"
    except requests.exceptions.RequestException as e:
        resultado += f"  {Colors.FAIL}❌ Error al analizar headers: {e}{Colors.END}\n"
        headers = {}
    return resultado, headers

# ==============================
# 3️⃣ Enumeración de usuarios
# ==============================
def enumerar_usuarios(url):
    resultado = f"\n{Colors.HEADER}🔍 Usuarios públicos detectados:{Colors.END}\n"
    encontrados = []

    for user in USUARIOS_COMUNES:
        author_url = f"{url}/author/{user}/"
        try:
            r = requests.get(author_url, timeout=3)
            if r.status_code == 200:
                encontrados.append(user)
                resultado += f"  {Colors.OK}✔ {user} (URL: {author_url}){Colors.END}\n"
        except:
            continue

    api_url = f"{url}/wp-json/wp/v2/users"
    try:
        r = requests.get(api_url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            for usuario in data:
                username = usuario.get("slug")
                if username and username not in encontrados:
                    encontrados.append(username)
                    resultado += f"  {Colors.OK}✔ {username} (vía API REST){Colors.END}\n"
    except:
        pass

    if not encontrados:
        resultado += f"  {Colors.WARNING}⚠ No se detectaron usuarios públicos.{Colors.END}\n"

    return resultado, encontrados

# ==============================
# 4️⃣ Comprobación API REST
# ==============================
def comprobar_api_rest(url):
    resultado = f"\n{Colors.HEADER}🔍 Comprobación API REST:{Colors.END}\n"
    api_url = url.rstrip("/") + "/wp-json/"
    try:
        r = requests.get(api_url, timeout=5)
        if r.status_code == 200:
            resultado += f"  {Colors.OK}✔ API REST activa: {api_url}{Colors.END}\n"
            data = r.json()
            endpoints = list(data.keys())
            resultado += f"  🌐 Endpoints públicos ({len(endpoints)}):\n"
            for ep in endpoints:
                resultado += f"    - {ep}\n"
        else:
            resultado += f"  {Colors.WARNING}⚠ API REST no accesible. Código HTTP: {r.status_code}{Colors.END}\n"
    except:
        resultado += f"  {Colors.FAIL}❌ Error al acceder a la API REST.{Colors.END}\n"
    return resultado

# ==============================
# 5️⃣ Archivos sensibles
# ==============================
def comprobar_archivos(url):
    resultado = f"\n{Colors.HEADER}🔍 Archivos sensibles:{Colors.END}\n"
    for archivo in ARCHIVOS_SENSIBLES:
        prueba_url = f"{url}/{archivo}"
        try:
            r = requests.get(prueba_url, timeout=3)
            if r.status_code < 400:
                resultado += f"  {Colors.WARNING}⚠ {archivo}: {r.status_code}{Colors.END}\n"
            else:
                resultado += f"  {Colors.OK}✔ {archivo}: {r.status_code}{Colors.END}\n"
        except:
            resultado += f"  {Colors.FAIL}❌ {archivo}: Error{Colors.END}\n"
    return resultado

# ==============================
# 6️⃣ Directorios abiertos
# ==============================
def comprobar_directorios(url):
    resultado = f"\n{Colors.HEADER}🔍 Directorios abiertos:{Colors.END}\n"
    for directorio in DIRECTORIOS_ABIERTOS:
        prueba_url = f"{url}/{directorio}"
        try:
            r = requests.get(prueba_url, timeout=3)
            if r.status_code < 400:
                resultado += f"  {Colors.WARNING}⚠ {directorio}: {r.status_code}{Colors.END}\n"
            else:
                resultado += f"  {Colors.OK}✔ {directorio}: {r.status_code}{Colors.END}\n"
        except:
            resultado += f"  {Colors.FAIL}❌ {directorio}: Error{Colors.END}\n"
    return resultado

# ==============================
# 7️⃣ Redirecciones y flujo HTTP
# ==============================
def analizar_redirecciones(url):
    resultado = f"\n{Colors.HEADER}🔍 Redirecciones y flujo HTTP:{Colors.END}\n"
    try:
        r = requests.get(url, timeout=5, allow_redirects=True)
        for i, resp in enumerate(r.history):
            resultado += f"  {Colors.INFO}➡ Redirección {i+1}: {resp.status_code} → {resp.url}{Colors.END}\n"
        resultado += f"  {Colors.OK}✔ Página final: {r.status_code} → {r.url}{Colors.END}\n"
    except:
        resultado += f"  {Colors.FAIL}❌ Error al analizar flujo HTTP{Colors.END}\n"
    return resultado

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    URL_OBJETIVO = input(f"{Colors.BOLD}Introduce la URL de la página WordPress a auditar: {Colors.END}").strip()
    
    informe = f"{Colors.HEADER}🔎 INICIANDO AUDITORÍA EXTERNA DE WORDPRESS: {URL_OBJETIVO}{Colors.END}\n\n"
    
    p_texto, puertos = analizar_puertos(URL_OBJETIVO)
    informe += p_texto
    
    h_texto, headers = analizar_headers(URL_OBJETIVO)
    informe += h_texto
    
    u_texto, usuarios = enumerar_usuarios(URL_OBJETIVO)
    informe += u_texto
    
    api_texto = comprobar_api_rest(URL_OBJETIVO)
    informe += api_texto
    
    arch_texto = comprobar_archivos(URL_OBJETIVO)
    informe += arch_texto
    
    dir_texto = comprobar_directorios(URL_OBJETIVO)
    informe += dir_texto
    
    redir_texto = analizar_redirecciones(URL_OBJETIVO)
    informe += redir_texto
    
    informe += f"\n{Colors.OK}✅ AUDITORÍA COMPLETADA.{Colors.END}\n"
    
    print(informe)
    escribir_informe(informe)
