[Volver Atras](../ud3.md)

## **2. Gestión de recursos y logística**

Para poder desarrollar y probar la plataforma de forma eficiente, voy a utilizar varios recursos, tanto software como hardware:

### ✅ **Recursos técnicos**
- Servidor VPS o máquina local con Linux (Debian/Ubuntu).
- Entornos aislados con Docker para cada módulo.
- GitHub para control de versiones y seguimiento de cambios.
- Máquinas virtuales para probar WordPress vulnerable.
- Python y Bash instalados para los scripts.
- Base de datos (MariaDB o SQLite) para almacenar resultados.
- Herramientas de auditoría open source:
  - Nmap  
  - Nikto  
  - OWASP ZAP  
  - WPScan  

### ✅ **Logística del proyecto**
- El código estará siempre versionado en GitHub.
- Cada módulo se desarrollará por separado antes de integrarlo.
- Las pruebas se realizarán en entornos aislados para evitar riesgos.
- Las auditorías se ejecutarán únicamente con permisos y sobre sitios controlados.

---