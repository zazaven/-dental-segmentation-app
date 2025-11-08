# Dental Panoramik X-Ray Segmentasyon Uygulaması

YOLO11 tabanlı AI destekli diş görüntü analizi ve segmentasyon aracı.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![YOLO11](https://img.shields.io/badge/YOLO11-Ultralytics-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 İçindekiler

- [Özellikler](#özellikler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Mimari](#mimari)
- [Veri Formatı](#veri-formatı)
- [Model Eğitimi](#model-eğitimi)
- [Segmentasyon](#segmentasyon)
- [Sorun Giderme](#sorun-giderme)
- [Katkıda Bulunma](#katkıda-bulunma)

## ✨ Özellikler

### 🖊️ Etiketleme Arayüzü
- **İnteraktif Poligon Çizimi**: Streamlit canvas ile kolay ve hızlı etiketleme
- **Çoklu Sınıf Desteği**: Diş, lezyon, dolgu, kron, implant, kanal tedavisi, çürük
- **Renk Kodlu Görselleştirme**: Her sınıf için özel renk
- **Düzenleme ve Silme**: Etiketleri kolayca yönetin
- **YOLO Format Desteği**: Otomatik format dönüşümü

### 🎓 Model Eğitimi
- **5 Model Varyantı**: Nano, Small, Medium, Large, Extra Large
- **Özelleştirilebilir Parametreler**: Epoch, batch size, learning rate, optimizer
- **Gerçek Zamanlı İzleme**: Eğitim ilerlemesini canlı takip
- **Otomatik Kaydetme**: En iyi model otomatik kaydedilir
- **Görselleştirme**: Loss curves, confusion matrix, validation predictions

### 🔍 AI Segmentasyon
- **Otomatik Tespit**: Eğitilmiş model ile anlık segmentasyon
- **Ayarlanabilir Eşikler**: Güven ve IoU eşiklerini özelleştirin
- **Görselleştirme Seçenekleri**: Maskeler, etiketler, güven skorları
- **Sonuç Dışa Aktarma**: Görüntüler, maskeler ve detaylı raporlar

## 🚀 Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- CUDA destekli GPU (opsiyonel, ancak önerilir)
- 8GB+ RAM
- 5GB+ disk alanı

### Adım 1: Depoyu Klonlayın

```bash
git clone https://github.com/yourusername/dental-segmentation-app.git
cd dental-segmentation-app
```

### Adım 2: Sanal Ortam Oluşturun

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### Adım 3: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### Adım 4: Uygulamayı Başlatın

```bash
streamlit run app.py
```

Uygulama otomatik olarak tarayıcınızda açılacaktır (varsayılan: http://localhost:8501)

## 📖 Kullanım

### 1. Etiketleme

#### Görüntü Yükleme
1. Sol menüden **🖊️ Etiketleme** sayfasına gidin
2. "Panoramik X-Ray Yükle" butonuna tıklayın
3. Panoramik diş röntgeni seçin (JPG, PNG, BMP)

#### Poligon Çizimi
1. Sağ panelden etiket sınıfını seçin (örn: diş, lezyon)
2. "Poligon Çiz" modunu seçin
3. Görüntü üzerinde yapının etrafına tıklayarak poligon çizin
4. En az 3 nokta ile poligonu kapatın
5. "Poligonu Ekle" butonuna tıklayın

#### Etiketleri Kaydetme
1. Tüm yapıları etiketledikten sonra
2. "Etiketleri Kaydet" butonuna tıklayın
3. Etiketler otomatik olarak YOLO formatında kaydedilir

**İpucu**: "Görüntüle" moduna geçerek etiketlerinizi kontrol edebilirsiniz.

### 2. Model Eğitimi

#### Veri Seti Hazırlama
1. **🎓 Model Eğitimi** sayfasına gidin
2. "Veri Seti Hazırlama" sekmesini seçin
3. Veri seti bölme oranlarını ayarlayın (varsayılan: 70% train, 20% val, 10% test)
4. "Veri Setini Hazırla" butonuna tıklayın

#### Model Eğitimi
1. "Model Eğitimi" sekmesine geçin
2. Model varyantını seçin:
   - **Nano**: En hızlı, küçük veri setleri için
   - **Small**: Önerilen, dengeli performans
   - **Medium**: Daha iyi doğruluk
   - **Large**: Yüksek doğruluk
   - **Extra Large**: En iyi doğruluk, en yavaş
3. Eğitim parametrelerini ayarlayın:
   - Epoch sayısı: 100-200 (varsayılan: 100)
   - Batch size: 8-32 (varsayılan: 16)
   - Görüntü boyutu: 640 (önerilir)
   - Learning rate: 0.001 (varsayılan)
4. "Eğitimi Başlat" butonuna tıklayın

**Önemli**: Eğitim süresi veri seti boyutuna ve donanıma bağlı olarak değişir (GPU ile 1-4 saat, CPU ile 10-20 saat).

#### Eğitim Sonuçları
Eğitim tamamlandığında:
- Loss curves (kayıp eğrileri)
- Confusion matrix (karışıklık matrisi)
- Validation predictions (doğrulama tahminleri)
otomatik olarak görüntülenir.

### 3. AI Segmentasyon

#### Model Yükleme
1. **🔍 AI Segmentasyon** sayfasına gidin
2. Sağ panelden eğitilmiş modeli seçin
3. "Modeli Yükle" butonuna tıklayın

#### Segmentasyon Yapma
1. "Panoramik X-Ray Yükle" ile yeni görüntü yükleyin
2. Güven eşiğini ayarlayın (varsayılan: 0.25)
3. "Segmentasyon Yap" butonuna tıklayın
4. Sonuçları görüntüleyin

#### Sonuçları Kaydetme
1. "Sonuçları Kaydet" butonuna tıklayın
2. Aşağıdakiler kaydedilir:
   - Orijinal görüntü
   - Segmentasyon sonucu (annotated)
   - Her tespit için maske
   - Detaylı rapor (TXT)

## 🏗️ Mimari

```
dental_segmentation_app/
├── app.py                      # Ana Streamlit uygulaması
├── requirements.txt            # Python bağımlılıkları
├── README.md                   # Dokümantasyon
├── config/
│   └── config.yaml            # Uygulama konfigürasyonu
├── modules/
│   ├── __init__.py
│   ├── annotation.py          # Etiketleme modülü
│   ├── training.py            # Eğitim modülü
│   ├── inference.py           # Segmentasyon modülü
│   └── utils.py               # Yardımcı fonksiyonlar
├── data/
│   ├── raw_images/            # Ham görüntüler
│   ├── annotations/           # YOLO etiketleri
│   └── dataset/               # Eğitim veri seti
│       ├── images/
│       │   ├── train/
│       │   ├── val/
│       │   └── test/
│       └── labels/
│           ├── train/
│           ├── val/
│           └── test/
├── models/
│   ├── pretrained/            # Ön-eğitimli modeller
│   └── trained/               # Eğitilmiş modeller
└── outputs/
    ├── training_results/      # Eğitim sonuçları
    └── inference_results/     # Segmentasyon sonuçları
```

## 📊 Veri Formatı

### YOLO Segmentation Format

Her görüntü için bir `.txt` dosyası:

```
<class_id> <x1> <y1> <x2> <y2> ... <xn> <yn>
```

- `class_id`: Sınıf numarası (0-6)
- `x1, y1, ..., xn, yn`: Normalize edilmiş poligon koordinatları (0-1 aralığında)

**Örnek**:
```
0 0.1 0.2 0.15 0.2 0.15 0.25 0.1 0.25
1 0.5 0.5 0.55 0.5 0.55 0.55 0.5 0.55
```

### data.yaml

```yaml
path: /path/to/dataset
train: images/train
val: images/val
test: images/test

nc: 7  # Sınıf sayısı
names: ['tooth', 'lesion', 'filling', 'crown', 'implant', 'root_canal', 'caries']
```

## 🎓 Model Eğitimi

### Model Varyantları

| Model | Parametreler | mAP | Hız | Kullanım |
|-------|-------------|-----|-----|----------|
| Nano | 2.9M | ⭐⭐ | ⚡⚡⚡⚡⚡ | Hızlı prototipleme |
| Small | 10.1M | ⭐⭐⭐ | ⚡⚡⚡⚡ | **Önerilen** |
| Medium | 22.4M | ⭐⭐⭐⭐ | ⚡⚡⚡ | Yüksek doğruluk |
| Large | 27.6M | ⭐⭐⭐⭐⭐ | ⚡⚡ | Çok yüksek doğruluk |
| Extra Large | 62.1M | ⭐⭐⭐⭐⭐ | ⚡ | En iyi doğruluk |

### Önerilen Parametreler

**Küçük Veri Seti (< 100 görüntü)**:
- Model: Nano veya Small
- Epochs: 100-150
- Batch Size: 8-16
- Image Size: 640

**Orta Veri Seti (100-500 görüntü)**:
- Model: Small veya Medium
- Epochs: 150-200
- Batch Size: 16-32
- Image Size: 640

**Büyük Veri Seti (> 500 görüntü)**:
- Model: Medium, Large veya Extra Large
- Epochs: 200-300
- Batch Size: 16-32
- Image Size: 640-800

### Veri Artırma

Eğitim sırasında otomatik olarak uygulanan veri artırma teknikleri:
- Rastgele döndürme
- Ölçekleme
- Yatay çevirme
- Parlaklık/kontrast ayarı
- Mozaik artırma

## 🔍 Segmentasyon

### Güven Eşiği

- **Düşük (0.1-0.2)**: Daha fazla tespit, daha fazla yanlış pozitif
- **Orta (0.25-0.4)**: Dengeli (önerilir)
- **Yüksek (0.5-0.8)**: Daha az tespit, daha yüksek kesinlik

### IoU Eşiği

- **Düşük (0.3-0.4)**: Çakışan tespitleri ayır
- **Orta (0.45-0.5)**: Dengeli (önerilir)
- **Yüksek (0.6-0.8)**: Yalnızca çok farklı tespitler

## 🐛 Sorun Giderme

### Eğitim Başlamıyor

**Sorun**: "CUDA out of memory" hatası
**Çözüm**: Batch size'ı azaltın (örn: 16 → 8)

**Sorun**: "No images found" hatası
**Çözüm**: Veri setini yeniden hazırlayın ve data.yaml'ı kontrol edin

### Düşük Doğruluk

**Sorun**: Model iyi tahmin yapmıyor
**Çözümler**:
1. Daha fazla etiketlenmiş görüntü ekleyin (en az 100+)
2. Etiketleme kalitesini kontrol edin
3. Daha fazla epoch ile eğitin
4. Daha büyük model varyantı deneyin
5. Learning rate'i ayarlayın

### Segmentasyon Sonuçları Yok

**Sorun**: Hiçbir yapı tespit edilmiyor
**Çözümler**:
1. Güven eşiğini düşürün (örn: 0.25 → 0.15)
2. Modelin doğru yüklendiğinden emin olun
3. Görüntü kalitesini kontrol edin

## 💡 En İyi Uygulamalar

### Etiketleme
1. **Tutarlı olun**: Aynı yapıları her zaman aynı şekilde etiketleyin
2. **Dikkatli çizin**: Poligonları mümkün olduğunca doğru çizin
3. **Sınırları dahil edin**: Yapının tüm kenarlarını kapsayın
4. **Belirsiz durumları atlayın**: Net olmayan yapıları etiketlemeyin

### Veri Seti
1. **Yeterli veri**: En az 50-100 etiketlenmiş görüntü
2. **Dengeli dağılım**: Her sınıftan yeterli örnek
3. **Çeşitlilik**: Farklı hasta, cihaz, kalitede görüntüler
4. **Kalite kontrolü**: Etiketleri düzenli olarak gözden geçirin

### Eğitim
1. **GPU kullanın**: Eğitim süresini 10-20x azaltır
2. **Patience kullanın**: Erken durdurma ile aşırı öğrenmeyi önleyin
3. **Checkpoint'leri saklayın**: En iyi modeli kaydedin
4. **Metrikleri izleyin**: Loss ve mAP'i takip edin

### Segmentasyon
1. **Uygun eşik**: Veri setinize göre ayarlayın
2. **Görüntü kalitesi**: Yüksek çözünürlüklü görüntüler kullanın
3. **Sonuçları doğrulayın**: AI tahminlerini manuel kontrol edin
4. **Geri bildirim**: Hataları düzelterek veri setini geliştirin

## 🔧 Gelişmiş Kullanım

### Komut Satırı Eğitimi

```bash
from ultralytics import YOLO

# Model yükle
model = YOLO('yolo11s-seg.pt')

# Eğit
results = model.train(
    data='data/dataset/data.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    device=0  # GPU
)
```

### Batch Segmentasyon

```python
import os
from ultralytics import YOLO

model = YOLO('models/trained/model_20250101_120000.pt')

# Klasördeki tüm görüntüleri işle
image_dir = 'path/to/images'
for img_file in os.listdir(image_dir):
    if img_file.endswith(('.jpg', '.png')):
        img_path = os.path.join(image_dir, img_file)
        results = model.predict(img_path, conf=0.25)
        # Sonuçları işle...
```

## 📚 Kaynaklar

- [YOLO11 Dokümantasyonu](https://docs.ultralytics.com/)
- [Ultralytics GitHub](https://github.com/ultralytics/ultralytics)
- [Instance Segmentation Guide](https://docs.ultralytics.com/tasks/segment/)
- [Training Tips](https://docs.ultralytics.com/modes/train/)

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen:

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 👥 İletişim

Sorularınız veya önerileriniz için:
- Issue açın: [GitHub Issues](https://github.com/yourusername/dental-segmentation-app/issues)
- Email: your.email@example.com

## 🙏 Teşekkürler

- [Ultralytics](https://ultralytics.com/) - YOLO11 framework
- [Streamlit](https://streamlit.io/) - Web framework
- [PyTorch](https://pytorch.org/) - Deep learning backend

---

**Not**: Bu uygulama araştırma ve eğitim amaçlıdır. Klinik kullanım için uygun değildir ve tıbbi teşhis için kullanılmamalıdır.

