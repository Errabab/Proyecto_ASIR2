[Volver Atras](../ud5.md)

## 2. Comandos y ejecución práctica

- **Verificar acceso a la interfaz web de Prometheus:**

```bash
curl http://localhost:9090
```
- **Reiniciar Prometheus tras cambios:**
  
```bash
sudo systemctl restart prometheus
```

- **Revisar logs de Prometheus:**
```bash
journalctl -u prometheus -f
``` 