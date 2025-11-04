[Volver Atras](../ud4.md)

## **2. Gestión de incidencias y cambios**

Durante el desarrollo han aparecido varias incidencias técnicas, especialmente relacionadas con la integración de herramientas externas y la sincronización entre módulos. Para gestionarlas he seguido un proceso simple pero efectivo.

### ✅ **Registro de incidencias**
Todas las incidencias, errores y modificaciones se han anotado en:
- GitHub Issues  
- Archivo interno `incidencias.md`  

Cada incidencia incluye:
- Descripción del problema  
- Fecha  
- Módulo afectado  
- Solución aplicada  

### ✅ **Clasificación de prioridades**
Las incidencias se han dividido en:
- **Críticas** → impiden el funcionamiento del sistema (ej: fallos en ZAP o MariaDB).  
- **Medias** → afectan a la experiencia pero no rompen el sistema.  
- **Bajas** → mejoras o pequeños detalles visuales del panel web.

### ✅ **Cambios controlados**
Cualquier cambio importante (panel web, base de datos, scripts) se hacía siempre en ramas separadas:
- `feature/auditoria-web`  
- `feature/wordpress`  
- `feature/panel-web`  

Después, se probaban en AWS y se fusionaban solo si todo funcionaba correctamente.

---