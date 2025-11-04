[Volver Atras](../ud3.md)

## **5. Valoración económica y control de costes**

El proyecto se ha diseñado para desarrollarse sin ningún coste económico . Toda la infraestructura se ejecutara utilizando herramientas open source y una instancia de AWS proporcionada por el instituto, lo que permite crear el entorno completo sin necesidad de contratar servicios adicionales.

### ✅ **Costes estimados del desarrollo (reales y aplicados al TFG)**

| Plataforma / Herramienta | Uso en el proyecto | Coste |
|--------------------------|--------------------|-------|
| **AWS  (proporcionado por el centro)** | Ejecución del servidor, contenedores Docker y pruebas | 0 € |
| **Docker** | Contenerización de módulos y aislamiento del entorno | 0 € |
| **Nmap** | Escaneo de puertos y detección de servicios | 0 € |
| **Nikto** | Análisis de configuraciones inseguras en servidores web | 0 € |
| **OWASP ZAP (API)** | Auditoría automatizada de vulnerabilidades web | 0 € |
| **WPScan (CLI gratuita)** | Auditoría específica para WordPress | 0 € |
| **Python + Flask** | Backend, API interna y panel web | 0 € |
| **Bash** | Automatización y ejecución de escaneos | 0 € |
| **MariaDB (en Docker, versión gratuita)** | Base de datos para almacenar resultados e históricos | 0 € |
| **Telegram Bot API** | Sistema de alertas en tiempo real | 0 € |

### ✅ **Coste total del proyecto: 0 €**

Todos los componentes utilizados son gratuitos. AWS es proporcionado por el instituto y MariaDB funciona como contenedor sin coste, por lo que la infraestructura completa no genera gastos.

---

### ✅ **Control de costes**

Para mantener el proyecto con coste cero, se han seguido las siguientes directrices:

- Uso exclusivo de **software open source**: Nmap, Nikto, ZAP, WPScan, Docker, MariaDB, Python, Flask.  
- La ejecución del proyecto se realiza en **AWS educativo**, sin necesidad de contratar VPS o servicios externos.  
- MariaDB se despliega en un contenedor Docker, evitando gastos en bases de datos gestionadas o servicios cloud de pago.  
- No se utiliza dominio propio; el acceso puede realizarse mediante IP o subdominio gratuito.  
- Toda la infraestructura se ejecuta en una sola instancia, optimizando el uso de recursos y evitando gastos adicionales.  

Este planteamiento asegura un proyecto **totalmente funcional y profesional**, pero sin coste, cumpliendo los requisitos del TFG y aprovechando al máximo los recursos proporcionados por el instituto.

