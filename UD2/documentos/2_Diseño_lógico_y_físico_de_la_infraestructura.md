[Volver Atras](../ud2.md)

## **2. Diseño lógico y físico de la infraestructura**

### ✅ **Diseño lógico**

La plataforma estará organizada en módulos independientes:

- **Módulo 1: Auditoría Web General**
  - Escaneo de puertos.
  - Análisis SSL.
  - Seguridad de cabeceras HTTP.
  - Detección de configuraciones débiles.
  - Vulnerabilidades comunes con ZAP.

- **Módulo 2: Auditoría WordPress**
  - Detección de plugins vulnerables.
  - Análisis de temas.
  - Versiones obsoletas.
  - Enumeración de usuarios.
  - Pruebas de fuerza bruta controladas.
  - Revisión de archivos sensibles.

- **Base de datos**: almacena resultados, informes y estados históricos.

- **Panel web (Dashboard)**:
  - Mostrar alertas.
  - Histórico de auditorías.
  - Estado general de seguridad.
  - Recomendaciones.

- **Sistema de alertas**:
  - Email.
  - Telegram.
  - Alertas instantáneas cuando se detecten vulnerabilidades críticas.

- **Automatización**:
  - Ejecución periódica programada por cron o servicios internos.

---

### ✅ **Diseño físico**

El diseño físico se basa en un entorno Linux con contenedores Docker aislados:

- **Servidor físico o VPS** (Ubuntu/Debian).  
- **Contenedor Docker 1**: análisis web general.  
- **Contenedor Docker 2**: análisis WordPress.  
- **Contenedor Docker 3**: backend + API + lógica interna.  
- **Contenedor Docker 4**: panel web.  
- **Contenedor Docker 5**: base de datos.  

Los contenedores estarán conectados mediante una red interna de Docker para aumentar la seguridad y evitar exposición accidental al exterior.

Se utilizarán volúmenes persistentes para guardar:

- Informes generados (PDF/JSON).  
- Logs.  
- Histórico de escaneos.  

---
