#!/usr/bin/env python3
import nmap
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# ============================
# 1. ENVÍO DE CORREO
# ============================

def enviar_informe(ruta_informe):
    remitente = "esalahr535@g.educaand.es"
    contraseña = "lqdj uhid csff cjfd"  # contraseña de aplicación Gmail
    destinatario = "rababsalecahrayam@gmail.com"

    asunto = "Informe de Auditoría Interna"
    cuerpo = "Adjunto encontrarás el informe generado automáticamente."

    mensaje = MIMEMultipart()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.attach(MIMEText(cuerpo, "plain"))

    # Adjuntar archivo
    with open(ruta_informe, "rb") as adjunto:
        parte = MIMEBase("application", "octet-stream")
        parte.set_payload(adjunto.read())
        encoders.encode_base64(parte)
        parte.add_header("Content-Disposition", f"attachment; filename={ruta_informe}")
        mensaje.attach(parte)

    # Enviar con SMTP
    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(remitente, contraseña)
    servidor.send_message(mensaje)
    servidor.quit()

    print("📧 Informe enviado correctamente.")


# ============================
# 2. ESCANEO RÁPIDO Y EFICIENTE
# ============================

def escanear(objetivo):
    print(f"\n🔍 Iniciando escaneo rápido sobre {objetivo}...\n")

    nm = nmap.PortScanner()

    # Escaneo rápido (-T4 reduce el tiempo, --top-ports 100 evita bloqueos)
    nm.scan(hosts=objetivo, ports=None, arguments="-T4 --top-ports 100")

    resultados = {
        "objetivo": objetivo,
        "puertos": []
    }

    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            puertos = nm[host][proto].keys()
            for p in puertos:
                estado = nm[host][proto][p]["state"]
                servicio = nm[host][proto][p]["name"]
                resultados["puertos"].append((p, estado, servicio))

    return resultados


# ============================
# 3. GENERAR INFORME
# ============================

def generar_informe(resultados):
    nombre_informe = f"informe_auditoria_{resultados['objetivo']}.txt"

    with open(nombre_informe, "w") as f:
        f.write("=== INFORME DE AUDITORÍA INTERNA ===\n")
        f.write(f"Objetivo: {resultados['objetivo']}\n")
        f.write(f"Fecha: {datetime.now()}\n\n")
        f.write("Puertos detectados:\n")
        f.write("---------------------\n")

        if resultados["puertos"]:
            for p, estado, servicio in resultados["puertos"]:
                f.write(f"Puerto {p} - {estado} - {servicio}\n")
        else:
            f.write("No se detectaron puertos abiertos.\n")

    print(f"\n📄 Informe generado: {nombre_informe}")
    return nombre_informe


# ============================
# 4. MAIN
# ============================

if __name__ == "__main__":
    print("=== Auditoría Interna Completa (White-Box) ===")
    objetivo = input("Introduce la IP o dominio a escanear: ")

    resultados = escanear(objetivo)
    informe = generar_informe(resultados)
    enviar_informe(informe)

    print("\n✅ Auditoría finalizada con éxito.\n")
