[Volver Atras](../ud5.md)

## 3. Manual de usuario

- **Acceder a Prometheus en el navegador:**
```cpp
http://<IP_DEL_SERVIDOR>:9090
``` 
- **Consultar métricas:**
  - Usar la barra de búsqueda para introducir queries PromQL.
  - Explorar `Graph` y `Alerts` para ver datos en tiempo real.
- **Integración con Grafana (opcional):**
  - Añadir Prometheus como datasource en Grafana.
- **Backup y recuperación:**
  - Copiar periódicamente `/opt/proyecto/monitoring/prometheus/data`.
- **Mantenimiento:**
  - Actualizar Prometheus siguiendo el mismo procedimiento de descarga y reemplazo del binario.

