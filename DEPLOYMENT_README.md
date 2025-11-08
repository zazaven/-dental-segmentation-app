# 🚀 Google Cloud Deployment - Hızlı Başlangıç

## ⚡ En Hızlı Yol (5 Dakika)

```bash
# 1. Proje dizinine gidin
cd /home/ubuntu/dental_segmentation_app

# 2. Deployment scriptini çalıştırın
./quick-deploy.sh
```

Script sizi adım adım yönlendirecek! 🎯

---

## 📋 Ön Gereksinimler

### 1. Google Cloud SDK Kurulumu

**Linux/Mac:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

**Windows:**
- İndirin: https://cloud.google.com/sdk/docs/install

### 2. Google Cloud'a Giriş

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

---

## 🎯 Deployment Seçenekleri

### Seçenek 1: İnteraktif (Önerilen) ⭐

```bash
./quick-deploy.sh
```

**Özellikler:**
- ✅ Adım adım rehberlik
- ✅ Otomatik kontroller
- ✅ Bölge seçimi
- ✅ Maliyet tahmini

### Seçenek 2: Otomatik

```bash
./deploy.sh
```

**Özellikler:**
- ✅ Hızlı deployment
- ✅ Minimal etkileşim
- ⚠️ Ayarlar önceden yapılmalı

### Seçenek 3: Manuel

```bash
# Build
gcloud builds submit --tag gcr.io/PROJECT_ID/dental-segmentation-app

# Deploy
gcloud run deploy dental-segmentation-app \
    --image gcr.io/PROJECT_ID/dental-segmentation-app \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 4Gi \
    --cpu 2
```

---

## 💰 Maliyet

| Kullanım | Aylık Maliyet |
|----------|---------------|
| **Test/Demo** | $0-5 |
| **Günlük Kullanım** | $10-20 |
| **7/24 Aktif** | $50-100 |

**Not:** İlk $300 kredi ücretsiz! (90 gün)

---

## 📁 Hazırlanan Dosyalar

```
✅ Dockerfile              - Container tanımı
✅ .dockerignore          - Build optimizasyonu
✅ .gcloudignore          - Upload optimizasyonu
✅ cloudrun.yaml          - Cloud Run config
✅ .streamlit/config.toml - Streamlit ayarları
✅ deploy.sh              - Otomatik deployment
✅ quick-deploy.sh        - İnteraktif deployment
```

---

## 🔧 Deployment Sonrası

### URL'nizi Öğrenin

```bash
gcloud run services describe dental-segmentation-app \
    --region us-central1 \
    --format 'value(status.url)'
```

### Logları Görüntüleyin

```bash
gcloud run logs tail dental-segmentation-app --region us-central1
```

### Güncelleme Yapın

```bash
# Kod değişikliklerinden sonra
./deploy.sh
```

---

## 🐛 Sorun mu Yaşıyorsunuz?

### Hata: "gcloud: command not found"

**Çözüm:** Google Cloud SDK'yı kurun
```bash
curl https://sdk.cloud.google.com | bash
```

### Hata: "Permission denied"

**Çözüm:** Giriş yapın
```bash
gcloud auth login
```

### Hata: "Project not set"

**Çözüm:** Proje seçin
```bash
gcloud config set project YOUR_PROJECT_ID
```

### Hata: "Build timeout"

**Çözüm:** Timeout'u artırın
```bash
gcloud builds submit --timeout=30m
```

---

## 📚 Detaylı Dokümantasyon

Tüm detaylar için bakınız:
- **Google_Cloud_Deployment_Guide.md** - Kapsamlı kılavuz
- **Cloud Run Docs:** https://cloud.google.com/run/docs

---

## ✅ Deployment Checklist

Başlamadan önce:

- [ ] Google Cloud hesabı var
- [ ] gcloud CLI kurulu
- [ ] Giriş yapıldı (`gcloud auth login`)
- [ ] Proje seçildi (`gcloud config set project`)
- [ ] Faturalandırma etkin

Hazırsanız:
```bash
./quick-deploy.sh
```

---

## 🎉 Başarılı Deployment!

Deployment tamamlandıktan sonra:

1. ✅ URL'nizi alın
2. ✅ Tarayıcıda açın
3. ✅ Uygulamanızı test edin
4. ✅ Dünyayla paylaşın!

**İyi çalışmalar! 🦷✨**

---

## 📞 Yardım

Sorun yaşarsanız:
- Logları kontrol edin: `gcloud run logs tail`
- Detaylı kılavuza bakın: `Google_Cloud_Deployment_Guide.md`
- Google Cloud destek: https://cloud.google.com/support

---

**Son Güncelleme:** 08 Kasım 2025
**Versiyon:** 1.0
