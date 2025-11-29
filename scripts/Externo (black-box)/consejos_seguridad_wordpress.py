#!/usr/bin/env python3
"""
Generador de consejos de seguridad para WordPress
basado en el informe de auditoría externa, con niveles de riesgo.
"""

import re

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    INFO = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

# Definición de niveles de riesgo
RIESGO = {
    "ALTO": f"{Colors.FAIL}ALTO{Colors.END}",
    "MEDIO": f"{Colors.WARNING}MEDIO{Colors.END}",
    "BAJO": f"{Colors.OK}BAJO{Colors.END}"
}

def analizar_informe(nombre_archivo="informe_auditoria_externa.txt"):
    consejos = []
    
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        contenido = f.read()
    
    # Headers de seguridad
    headers_no_config = re.findall(r"⚠ (X-Frame-Options|X-Content-Type-Options|Strict-Transport-Security|Content-Security-Policy|Referrer-Policy|Permissions-Policy): NO configurado", contenido)
    if headers_no_config:
        consejos.append({
            "riesgo": RIESGO["ALTO"],
            "mensaje": f"Configura los headers de seguridad: {', '.join(set(headers_no_config))}"
        })
    
    # Archivos sensibles
    archivos_sensibles = re.findall(r"⚠ (wp-config\.php|readme\.html|xmlrpc\.php): \d+", contenido)
    if archivos_sensibles:
        consejos.append({
            "riesgo": RIESGO["ALTO"],
            "mensaje": f"Restringe el acceso a los archivos sensibles: {', '.join(set(archivos_sensibles))}"
        })
    
    # Directorios abiertos
    directorios_abiertos = re.findall(r"⚠ (wp-content/uploads/|wp-includes/|wp-admin/): \d+", contenido)
    if directorios_abiertos:
        consejos.append({
            "riesgo": RIESGO["MEDIO"],
            "mensaje": f"Revisa permisos y protección de los directorios abiertos: {', '.join(set(directorios_abiertos))}"
        })
    
    # Usuarios expuestos
    if "No se detectaron usuarios públicos" not in contenido:
        consejos.append({
            "riesgo": RIESGO["ALTO"],
            "mensaje": "Verifica la seguridad de los usuarios expuestos y limita la información pública"
        })
    
    # API REST
    if "API REST no accesible" in contenido:
        consejos.append({
            "riesgo": RIESGO["BAJO"],
            "mensaje": "API REST deshabilitada, esto es seguro si no la necesitas"
        })
    else:
        consejos.append({
            "riesgo": RIESGO["MEDIO"],
            "mensaje": "Revisa los permisos de la API REST y limita el acceso solo a usuarios autorizados"
        })
    
    # Puertos HTTP alternativos
    puertos = re.findall(r"✔ (http://[\d\.]+)(:\d+)?  \(Estado: (\d+)\)", contenido)
    for url, puerto, estado in puertos:
        if puerto and puerto != ":80":
            consejos.append({
                "riesgo": RIESGO["MEDIO"],
                "mensaje": f"Puerto web alternativo accesible detectado en {url}{puerto}, revisa si es necesario"
            })
    
    # Si no hay problemas detectados
    if not consejos:
        consejos.append({
            "riesgo": RIESGO["BAJO"],
            "mensaje": "No se detectaron problemas críticos, sigue manteniendo tu WordPress actualizado y seguro"
        })
    
    return consejos

if __name__ == "__main__":
    print(f"{Colors.HEADER}{Colors.BOLD}🔎 CONSEJOS DE SEGURIDAD BASADOS EN EL INFORME DE AUDITORÍA{Colors.END}\n")
    consejos = analizar_informe()
    for c in consejos:
        print(f"- {c['riesgo']} → {c['mensaje']}")
    print(f"\n{Colors.OK}✅ FIN DE LOS CONSEJOS DE SEGURIDAD CON RIESGO.{Colors.END}")
