# 🚀 Deployment Guide

Bu kılavuz, uygulamanın farklı ortamlarda nasıl deploy edileceğini açıklar.

## 📋 İçindekiler

- [Yerel Deployment](#yerel-deployment)
- [Docker ile Deployment](#docker-ile-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Güvenlik](#güvenlik)

## 🏠 Yerel Deployment

### Gereksinimler

- Python 3.8+
- 8GB+ RAM
- GPU (opsiyonel, ancak önerilir)

### Adımlar

```bash
# 1. Depoyu klonlayın
git clone https://github.com/yourusername/dental-segmentation-app.git
cd dental-segmentation-app

# 2. Sanal ortam oluşturun
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows

# 3. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 4. Uygulamayı başlatın
streamlit run app.py
```

### Port ve Host Ayarları

```bash
# Özel port
streamlit run app.py --server.port 8080

# Tüm ağdan erişim
streamlit run app.py --server.address 0.0.0.0

# Her ikisi
streamlit run app.py --server.port 8080 --server.address 0.0.0.0
```

## 🐳 Docker ile Deployment

### Dockerfile Oluşturma

`Dockerfile`:

```dockerfile
FROM python:3.10-slim

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizini
WORKDIR /app

# Python bağımlılıkları
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyaları
COPY . .

# Port
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Başlat
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose

`docker-compose.yml`:

```yaml
version: '3.8'

services:
  dental-segmentation:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
      - ./outputs:/app/outputs
    environment:
      - STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
    restart: unless-stopped
```

### Build ve Run

```bash
# Build
docker build -t dental-segmentation .

# Run
docker run -p 8501:8501 dental-segmentation

# Docker Compose ile
docker-compose up -d
```

## ☁️ Cloud Deployment

### Streamlit Cloud

1. GitHub'a push edin
2. [share.streamlit.io](https://share.streamlit.io) adresine gidin
3. "New app" tıklayın
4. Repository seçin
5. `app.py` dosyasını seçin
6. Deploy edin

**Avantajlar**:
- Ücretsiz
- Kolay setup
- Otomatik HTTPS

**Dezavantajlar**:
- Sınırlı kaynak
- Public repository gerekli
- GPU desteği yok

### Heroku

```bash
# Heroku CLI yükleyin
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# App oluşturun
heroku create dental-segmentation-app

# Deploy
git push heroku main

# Open
heroku open
```

`Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### AWS EC2

1. **EC2 Instance Oluşturun**
   - Ubuntu 22.04 LTS
   - t3.large veya daha büyük (GPU için p3.2xlarge)
   - 30GB+ storage

2. **SSH ile Bağlanın**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Kurulum**
   ```bash
   # Sistem güncellemesi
   sudo apt update && sudo apt upgrade -y
   
   # Python ve pip
   sudo apt install python3-pip python3-venv -y
   
   # Uygulamayı klonlayın
   git clone https://github.com/yourusername/dental-segmentation-app.git
   cd dental-segmentation-app
   
   # Sanal ortam
   python3 -m venv venv
   source venv/bin/activate
   
   # Bağımlılıklar
   pip install -r requirements.txt
   
   # Systemd service
   sudo nano /etc/systemd/system/dental-segmentation.service
   ```

4. **Systemd Service**
   ```ini
   [Unit]
   Description=Dental Segmentation App
   After=network.target
   
   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/dental-segmentation-app
   Environment="PATH=/home/ubuntu/dental-segmentation-app/venv/bin"
   ExecStart=/home/ubuntu/dental-segmentation-app/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

5. **Service Başlatma**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable dental-segmentation
   sudo systemctl start dental-segmentation
   sudo systemctl status dental-segmentation
   ```

6. **Nginx Reverse Proxy** (Opsiyonel)
   ```bash
   sudo apt install nginx -y
   sudo nano /etc/nginx/sites-available/dental-segmentation
   ```
   
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
   
   ```bash
   sudo ln -s /etc/nginx/sites-available/dental-segmentation /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Google Cloud Platform

1. **Compute Engine VM Oluşturun**
2. **Firewall Kuralı Ekleyin** (port 8501)
3. **SSH ile Bağlanın**
4. AWS EC2 ile aynı adımları izleyin

### Azure

1. **Virtual Machine Oluşturun**
2. **Network Security Group** (port 8501)
3. **SSH ile Bağlanın**
4. AWS EC2 ile aynı adımları izleyin

## 🔒 Güvenlik

### Temel Güvenlik

1. **Environment Variables**
   ```bash
   # .env dosyası
   STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
   STREAMLIT_SERVER_ENABLE_CORS=false
   ```

2. **Secrets Management**
   ```bash
   # .streamlit/secrets.toml
   [passwords]
   admin_password = "your-secure-password"
   ```

3. **HTTPS**
   - Let's Encrypt ile SSL sertifikası
   - Nginx reverse proxy ile HTTPS

### Gelişmiş Güvenlik

1. **Authentication**
   ```python
   # app.py'ye ekleyin
   import streamlit as st
   
   def check_password():
       def password_entered():
           if st.session_state["password"] == st.secrets["passwords"]["admin_password"]:
               st.session_state["password_correct"] = True
               del st.session_state["password"]
           else:
               st.session_state["password_correct"] = False
       
       if "password_correct" not in st.session_state:
           st.text_input("Password", type="password", on_change=password_entered, key="password")
           return False
       elif not st.session_state["password_correct"]:
           st.text_input("Password", type="password", on_change=password_entered, key="password")
           st.error("😕 Password incorrect")
           return False
       else:
           return True
   
   if not check_password():
       st.stop()
   ```

2. **Rate Limiting**
   - Nginx ile rate limiting
   - Cloudflare ile DDoS protection

3. **Data Encryption**
   - Veri tabanı şifreleme
   - Dosya sistemi şifreleme

## 📊 Monitoring

### Logs

```bash
# Streamlit logs
streamlit run app.py --server.enableCORS false --server.enableXsrfProtection true 2>&1 | tee app.log

# Systemd logs
sudo journalctl -u dental-segmentation -f
```

### Metrics

- CPU/RAM kullanımı
- Disk kullanımı
- Request sayısı
- Hata oranı

### Tools

- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Sentry**: Error tracking

## 🔄 Backup

### Otomatik Backup

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backup/dental-segmentation"
DATE=$(date +%Y%m%d_%H%M%S)

# Data backup
tar -czf "$BACKUP_DIR/data_$DATE.tar.gz" data/

# Models backup
tar -czf "$BACKUP_DIR/models_$DATE.tar.gz" models/

# Keep last 7 days
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete
```

### Cron Job

```bash
# Günlük backup (her gece 2:00)
0 2 * * * /path/to/backup.sh
```

## 🚀 Performance Optimization

### 1. Caching

```python
@st.cache_resource
def load_model(model_path):
    return YOLO(model_path)
```

### 2. GPU Acceleration

```bash
# CUDA kurulumu
# https://developer.nvidia.com/cuda-downloads

# PyTorch GPU
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### 3. Nginx Caching

```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;

location / {
    proxy_cache my_cache;
    proxy_cache_valid 200 60m;
    # ...
}
```

## 📱 Mobile Access

### Responsive Design

Streamlit otomatik olarak responsive'dir, ancak:

```python
# Mobil için optimize edilmiş layout
if st.session_state.get('mobile_mode', False):
    st.set_page_config(layout="centered")
else:
    st.set_page_config(layout="wide")
```

## 🆘 Troubleshooting

### Port Already in Use

```bash
# Port'u kullanan process'i bul
lsof -i :8501

# Process'i öldür
kill -9 <PID>
```

### Out of Memory

```bash
# Swap artır
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### CUDA Out of Memory

```python
# Batch size'ı azalt
batch_size = 8  # veya 4
```

## 📚 Kaynaklar

- [Streamlit Deployment](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [AWS EC2 Guide](https://docs.aws.amazon.com/ec2/)
- [Nginx Configuration](https://nginx.org/en/docs/)

---

**Not**: Production deployment için profesyonel DevOps desteği önerilir.

