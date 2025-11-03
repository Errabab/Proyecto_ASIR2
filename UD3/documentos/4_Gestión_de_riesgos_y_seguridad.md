[Volver Atras](../ud3.md)

## **4. Gestión de riesgos y seguridad**

Este proyecto trata con herramientas de auditoría, así que la gestión de riesgos es fundamental. A continuación detallo los principales riesgos identificados y cómo los voy a mitigar.

### ✅ **Riesgos técnicos**
| Riesgo | Impacto | Solución |
|--------|---------|----------|
| Escanear webs sin permiso | Alto | Solo usar dominios propios o con autorización expresa |
| Alta carga o ralentización en servidores analizados | Medio | Limitar peticiones y configurar umbrales |
| Falsos positivos en vulnerabilidades | Medio | Revisar resultados críticos manualmente |
| Fallos en contenedores Docker | Bajo | Reinicios automáticos y logs persistentes |
| Errores en la base de datos | Medio | Backups frecuentes |

### ✅ **Riesgos de seguridad**
- No explotar vulnerabilidades, solo detectarlas.  
- No almacenar datos personales.  
- Aislar los contenedores para evitar fugas de información.  
- Evitar registros innecesarios que puedan contener datos sensibles.  

El proyecto cumple las normas éticas de la ciberseguridad y la LSSI-CE.

---