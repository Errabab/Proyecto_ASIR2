[Volver Atras](../ud5.md)

## 1. Instalación y despliegue paso a paso

- **Instalación de dependencias en Debian:**

```bash
sudo apt update
sudo apt install -y wget curl tar
sudo mkdir -p /opt/proyecto/monitoring/prometheus/data
sudo chown -R nobody:nogroup /opt/proyecto/monitoring/prometheus
```

- **Descarga y configuración de Prometheus:**

```bash
cd /opt/proyecto/monitoring/prometheus
sudo wget https://github.com/prometheus/prometheus/releases/download/v3.7.3/prometheus-3.7.3.linux-amd64.tar.gz
sudo tar -xvf prometheus-3.7.3.linux-amd64.tar.gz
sudo mv prometheus-3.7.3.linux-amd64 prometheus
```
- **Creación del archivo de configuración `prometheus.yml`**
```yaml

global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: []

rule_files: []

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
        labels:
          app: "prometheus"

```

- **Creación del servicio systemd**
  
```bash
sudo nano /etc/systemd/system/prometheus.service
```
**Agregar:**

```ini
[Unit]
Description=Prometheus Monitoring
Wants=network-online.target
After=network-online.target

[Service]
User=nobody
Group=nogroup
Type=simple
ExecStart=/opt/proyecto/monitoring/prometheus/prometheus/prometheus --config.file=/opt/proyecto/monitoring/prometheus/prometheus/prometheus.yml --storage.tsdb.path=/opt/proyecto/monitoring/prometheus/data

[Install]
WantedBy=multi-user.target

```

- **Arrancar Prometheus y habilitarlo al inicio:**
  
```bash
sudo systemctl daemon-reload
sudo systemctl start prometheus
sudo systemctl enable prometheus
sudo systemctl status prometheus
```