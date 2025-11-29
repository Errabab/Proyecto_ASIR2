# auditoria_avanzada.py
# (GENERADO COMPLETO)
# Script de auditoría avanzada con escaneo rápido, WHOIS, GEO-IP,
# banners, riesgo por puerto, recomendaciones y envío de PDF por correo.

import nmap
import whois
import requests
import socket
from fpdf import FPDF
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from datetime import datetime

# ============================
# MAPA DE PUERTOS → DESCRIPCIÓN + RIESGO
# ============================
PUERTOS_INFO = {
    22: ("SSH", "Acceso remoto seguro", "MEDIO", "Usar claves, desactivar login por contraseña"),
    80: ("HTTP", "Web sin cifrar", "MEDIO", "Forzar HTTPS y añadir firewall de aplicación"),
    443: ("HTTPS", "Web cifrada", "BAJO", "Mantener certificados actualizados"),
    3000: ("WebApp/Node", "Servicios Express/NodeJS", "ALTO", "Proteger con firewall y autenticación"),
    3306: ("MySQL", "Base de datos", "ALTO", "No exponer a Internet, usar firewall"),
    5432: ("PostgreSQL", "Base de datos", "ALTO", "Restringir por IP"),
    9100: ("JetDirect", "Servicio de impresión", "MEDIO", "Cerrar si no se usa"),
}

# ============================
# ESCANEO NMAP
# ============================
def escanear_puertos(ip):
    nm = nmap.PortScanner()
    nm.scan(ip, ports="1-2000", arguments="-T4 --open --max-retries 1 --host-timeout 20s")

    resultados = []
    if ip in nm.all_hosts():
        for proto in nm[ip].all_protocols():
            puertos = nm[ip][proto].keys()
            for p in sorted(puertos):
                estado = nm[ip][proto][p]["state"]
                resultados.append((p, estado))
    return resultados

# ============================
# WHOIS
# ============================
def obtener_whois(obj):
    try:
        data = whois.whois(obj)
        return str(data)
    except:
        return "No disponible"

# ============================
# GEO-IP
# ============================
def geoip(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}").json()
        return r
    except:
        return None

# ============================
# BANNERS
# ============================
def obtener_banner(ip, puerto):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((ip, puerto))
        banner = s.recv(1024).decode(errors="ignore")
        s.close()
        return banner if banner else "No accesible"
    except:
        return "No accesible"

# ============================
# DETECCIÓN DE WAF
# ============================
def detectar_waf(ip):
    try:
        r = requests.get(f"http://{ip}")
        headers = str(r.headers).lower()
        if "cloudflare" in headers:
            return "Cloudflare Detectado"
        if "sucuri" in headers:
            return "Sucuri Detectado"
        if "incapsula" in headers:
            return "Incapsula Detectado"
        return "No se detecta WAF"
    except:
        return "No accesible"

# ============================
# GENERAR PDF
# ============================
def generar_pdf(nombre_pdf, ip, geo, whois_info, waf, puertos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, f"INFORME DE AUDITORIA - {ip}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", size=11)
    pdf.cell(0, 8, "=== GEO-IP ===", ln=True)
    for k, v in geo.items():
        pdf.cell(0, 6, f"{k}: {v}", ln=True)
    pdf.ln(5)

    pdf.cell(0, 8, "=== WAF ===", ln=True)
    pdf.cell(0, 6, waf, ln=True)
    pdf.ln(5)

    pdf.cell(0, 8, "=== PUERTOS DETECTADOS ===", ln=True)
    for p, estado, banner, riesgo, rec, desc in puertos:
        pdf.multi_cell(0, 6, f"Puerto {p} ({desc}) - {estado} - Riesgo: {riesgo}\nBanner: {banner}\nRecomendación: {rec}")
        pdf.ln(2)

    pdf.ln(5)
    pdf.cell(0, 8, "=== WHOIS ===", ln=True)
    pdf.set_font_size(9)
    pdf.multi_cell(0, 5, whois_info)

    pdf.output(nombre_pdf)

# ============================
# ENVÍO DE CORREO
# ============================
def enviar_email(archivo):
    remitente = "esalahr535@g.educaand.es"
    clave = "lqdj uhid csff cjfd"
    destino = "rababsalecahrayam@gmail.com"

    msg = MIMEMultipart()
    msg["From"] = remitente
    msg["To"] = destino
    msg["Subject"] = "Informe de Auditoría Avanzada"

    msg.attach(MIMEText("Se adjunta el informe en PDF.", "plain"))

    with open(archivo, "rb") as adj:
        parte = MIMEBase("application", "octet-stream")
        parte.set_payload(adj.read())
        encoders.encode_base64(parte)
        parte.add_header("Content-Disposition", f"attachment; filename={archivo}")
        msg.attach(parte)

    servidor = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    servidor.login(remitente, clave)
    servidor.sendmail(remitente, destino, msg.as_string())
    servidor.quit()

# ============================
# PROGRAMA PRINCIPAL
# ============================
print("=== Auditoría Interna Avanzada ===")
objetivo = input("Introduce la IP o dominio a escanear: ")

print("\n🔍 Escaneando puertos...")
puertos_raw = escanear_puertos(objetivo)

print("📡 Obteniendo WHOIS...")
info_whois = obtener_whois(objetivo)

print("🌍 Obteniendo GEO-IP...")
info_geo = geoip(objetivo)

print("🛡️ Detectando WAF...")
info_waf = detectar_waf(objetivo)

# Preparar datos puertos enriquecidos
puertos_full = []
for p, estado in puertos_raw:
    banner = obtener_banner(objetivo, p)
    nombre, desc, riesgo, rec = PUERTOS_INFO.get(p, ("Desconocido", "Servicio desconocido", "MEDIO", "Investigar"))
    puertos_full.append((p, estado, banner, riesgo, rec, desc))

# ============================
# GUARDAR TXT
# ============================
nombre_txt = f"informe_auditoria_{objetivo}.txt"
f = open(nombre_txt, "w")
f.write(f"=== INFORME DE AUDITORÍA INTERNA ===\nObjetivo: {objetivo}\nFecha: {datetime.now()}\n\n")

f.write("=== GEOLOCALIZACIÓN ===\n")
for k, v in info_geo.items():
    f.write(f"{k}: {v}\n")
f.write("\n\n=== WHOIS ===\n")
f.write(info_whois + "\n\n")

f.write("=== DETECCIÓN DE WAF ===\n")
f.write(info_waf + "\n\n")

f.write("=== PUERTOS ABIERTOS ===\n\n")
for p, estado, banner, riesgo, rec, desc in puertos_full:
    f.write(f"Puerto {p} - {estado} - {desc} - Riesgo {riesgo}\nBanner: {banner}\nRecomendación: {rec}\n\n")

f.close()
print(f"📄 Informe TXT generado: {nombre_txt}")

# ============================
# PDF
# ============================
nombre_pdf = f"informe_auditoria_{objetivo}.pdf"
print("🖨️ Generando informe PDF...")
generar_pdf(nombre_pdf, objetivo, info_geo, info_whois, info_waf, puertos_full)

# ============================
# Enviar correo
# ============================
print("📧 Enviando correo...")
enviar_email(nombre_pdf)

print("\n✅ Auditoría finalizada con éxito.")
