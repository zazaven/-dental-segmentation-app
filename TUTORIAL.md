# 📚 Detaylı Kullanım Eğitimi

Bu eğitim, uygulamayı sıfırdan kullanarak kendi dental segmentasyon modelinizi oluşturmanızı sağlar.

## 📋 İçindekiler

1. [Giriş](#1-giriş)
2. [Veri Toplama](#2-veri-toplama)
3. [Etiketleme](#3-etiketleme)
4. [Veri Seti Hazırlama](#4-veri-seti-hazırlama)
5. [Model Eğitimi](#5-model-eğitimi)
6. [Model Değerlendirme](#6-model-değerlendirme)
7. [Segmentasyon](#7-segmentasyon)
8. [İleri Seviye](#8-ileri-seviye)

---

## 1. Giriş

### 1.1 Uygulama Nedir?

Bu uygulama, panoramik diş röntgenlerinde dental yapıları (diş, lezyon, dolgu, vb.) otomatik olarak tespit eden ve segmente eden bir AI aracıdır.

### 1.2 Nasıl Çalışır?

**3 Ana Adım**:
1. **Etiketleme**: Görüntülerde yapıları manuel olarak işaretleyin
2. **Eğitim**: AI modelini etiketli verilerle eğitin
3. **Segmentasyon**: Yeni görüntülerde otomatik tespit yapın

### 1.3 Gereksinimler

**Donanım**:
- Bilgisayar: 8GB+ RAM
- GPU: Önerilir (eğitim için)
- Disk: 5GB+ boş alan

**Yazılım**:
- Python 3.8+
- Streamlit
- YOLO11 (Ultralytics)

**Veri**:
- Panoramik diş röntgenleri
- En az 50-100 görüntü (daha fazlası daha iyi)

---

## 2. Veri Toplama

### 2.1 Görüntü Gereksinimleri

**Format**: JPG, PNG, BMP
**Çözünürlük**: 1000x500 piksel veya üzeri
**Kalite**: Net, iyi aydınlatılmış
**Çeşitlilik**: Farklı hasta, cihaz, koşullar

### 2.2 Veri Kaynakları

1. **Klinik Veriler**: Kendi kliniğinizden (etik onay gerekli)
2. **Açık Veri Setleri**: 
   - Tufts Dental Database
   - UFBA-UESC Dataset
3. **Sentetik Veri**: Veri artırma ile

### 2.3 Veri Hazırlama

```bash
# Görüntüleri bir klasöre koyun
mkdir panoramic_xrays
cp /path/to/images/*.jpg panoramic_xrays/

# Görüntü sayısını kontrol edin
ls panoramic_xrays/ | wc -l
```

**İpucu**: Görüntüleri anlamlı isimlerle kaydedin (örn: `patient_001.jpg`)

---

## 3. Etiketleme

### 3.1 Etiketleme Arayüzüne Giriş

1. Uygulamayı başlatın: `streamlit run app.py`
2. Sol menüden **🖊️ Etiketleme** seçin
3. İlk görüntünüzü yükleyin

### 3.2 Sınıfları Anlama

| Sınıf | Açıklama | Örnek |
|-------|----------|-------|
| **Diş** | Bireysel dişler | Kesici, azı dişi |
| **Lezyon** | Anormal oluşumlar | Kist, tümör |
| **Dolgu** | Restorasyon materyalleri | Amalgam, kompozit |
| **Kron** | Diş kaplamalar | Metal, seramik |
| **İmplant** | Yapay diş kökleri | Titanyum implant |
| **Kanal Tedavisi** | Endodontik tedavi | Kök kanal dolgusu |
| **Çürük** | Diş çürükleri | Kavite |

### 3.3 Poligon Çizme Teknikleri

#### Temel Adımlar

1. **Sınıf Seçin**: Sağ panelden (örn: "diş")
2. **Poligon Çizin**: 
   - Yapının kenarlarına tıklayın
   - En az 3 nokta
   - İlk noktaya yakın tıklayarak kapatın
3. **Ekleyin**: "Poligonu Ekle" butonuna tıklayın
4. **Kaydedin**: "Etiketleri Kaydet"

#### En İyi Uygulamalar

✅ **Yapılması Gerekenler**:
- Yapının tüm kenarlarını kapsayın
- Tutarlı olun (aynı yapıları aynı şekilde)
- Net olmayan yapıları atlayın
- Düzenli olarak kaydedin

❌ **Yapılmaması Gerekenler**:
- Çok gevşek poligonlar çizmeyin
- Farklı yapıları karıştırmayın
- Belirsiz bölgeleri zorlamayın
- Etiketleri kaydetmeyi unutmayın

#### Örnek: Diş Etiketleme

```
1. Bir dişi seçin (örn: üst sol kesici)
2. Dişin taç kısmının etrafına poligon çizin
3. Kök kısmını dahil edin
4. Komşu dişlerle çakışmayın
5. "Poligonu Ekle" → "Kaydet"
```

### 3.4 Etiketleme Stratejileri

#### Hızlı Etiketleme (Başlangıç)

- Her görüntüde 2-3 ana yapı
- Sadece net görünen yapılar
- 20-30 görüntü ile başlayın

#### Detaylı Etiketleme (İleri)

- Her görüntüde tüm yapılar
- Küçük lezyonlar dahil
- 100+ görüntü hedefleyin

#### Dengeli Etiketleme (Önerilen)

- Her sınıftan eşit sayıda örnek
- Farklı büyüklüklerde yapılar
- 50-100 görüntü

### 3.5 Kalite Kontrol

Her 10 görüntüde bir:
1. "Görüntüle" moduna geçin
2. Etiketleri kontrol edin
3. Hataları düzeltin
4. Yeniden kaydedin

---

## 4. Veri Seti Hazırlama

### 4.1 Veri Seti Bölme

**Önerilen Oranlar**:
- **Eğitim (Train)**: 70% - Modeli eğitmek için
- **Doğrulama (Val)**: 20% - Hiperparametre ayarı için
- **Test**: 10% - Final performans testi için

**Örnek**: 100 görüntü
- Train: 70 görüntü
- Val: 20 görüntü
- Test: 10 görüntü

### 4.2 Veri Seti Hazırlama Adımları

1. **Model Eğitimi** sayfasına gidin
2. **Veri Seti Hazırlama** sekmesini seçin
3. Oranları ayarlayın (varsayılan: 70/20/10)
4. **"Veri Setini Hazırla"** butonuna tıklayın

**Sonuç**:
```
✅ Veri seti başarıyla hazırlandı!
Eğitim: 70
Doğrulama: 20
Test: 10
```

### 4.3 Veri Seti Doğrulama

**"Veri Setini Doğrula"** butonuna tıklayın

**Kontrol Edilen**:
- Dizin yapısı
- Görüntü-etiket eşleşmesi
- Dosya sayıları

**Hata Durumunda**:
- Eksik dizinleri oluşturun
- Etiketleri kontrol edin
- Yeniden hazırlayın

---

## 5. Model Eğitimi

### 5.1 Model Seçimi

| Model | Ne Zaman Kullanılır | Avantaj | Dezavantaj |
|-------|---------------------|---------|------------|
| **Nano** | Hızlı test, küçük veri | Çok hızlı | Düşük doğruluk |
| **Small** | Genel kullanım | Dengeli | - |
| **Medium** | Daha iyi doğruluk | Yüksek performans | Daha yavaş |
| **Large** | Yüksek doğruluk | Çok iyi performans | Yavaş |
| **Extra Large** | En iyi doğruluk | En iyi performans | Çok yavaş |

**Öneri**: Small ile başlayın

### 5.2 Hiperparametre Ayarları

#### Epoch Sayısı

- **Az (50-100)**: Hızlı test
- **Orta (100-200)**: Genel kullanım ✅
- **Çok (200-500)**: Büyük veri setleri

#### Batch Size

- **Küçük (4-8)**: Sınırlı RAM/GPU
- **Orta (16-32)**: Normal ✅
- **Büyük (32-64)**: Güçlü GPU

#### Learning Rate

- **Düşük (0.0001)**: Hassas ayar
- **Orta (0.001)**: Varsayılan ✅
- **Yüksek (0.01)**: Hızlı öğrenme

#### Görüntü Boyutu

- **Küçük (416)**: Hızlı
- **Orta (640)**: Önerilen ✅
- **Büyük (800-1024)**: Detaylı

### 5.3 Eğitim Başlatma

1. **Model Eğitimi** sekmesine geçin
2. Model seçin: **Small**
3. Parametreleri ayarlayın:
   ```
   Epoch: 100
   Batch Size: 16
   Image Size: 640
   Learning Rate: 0.001
   Device: GPU (varsa)
   ```
4. **"Eğitimi Başlat"** butonuna tıklayın

### 5.4 Eğitim İzleme

**Eğitim Sırasında**:
- Progress bar: İlerleme
- Loss curves: Kayıp fonksiyonu
- mAP: Doğruluk metrikleri

**Beklenen Süre**:
- GPU ile: 1-4 saat
- CPU ile: 10-20 saat

**İpucu**: Eğitim sırasında bilgisayarı kullanabilirsiniz, ancak ağır işlemler yapmayın.

### 5.5 Eğitim Sorunları

#### Out of Memory

**Çözüm**: Batch size'ı azaltın
```
16 → 8 → 4
```

#### Çok Yavaş

**Çözüm**: 
- GPU kullanın
- Küçük model seçin (Small → Nano)
- Epoch azaltın

#### Loss Düşmüyor

**Çözüm**:
- Learning rate ayarlayın
- Daha fazla veri ekleyin
- Etiketleri kontrol edin

---

## 6. Model Değerlendirme

### 6.1 Eğitim Sonuçları

Eğitim bitince otomatik olarak gösterilir:

#### Loss Curves

- **Train Loss**: Eğitim kaybı (düşmeli)
- **Val Loss**: Doğrulama kaybı (düşmeli)
- **Overfitting**: Val loss artıyorsa

#### Confusion Matrix

- **Diagonal**: Doğru tahminler (yüksek olmalı)
- **Off-diagonal**: Yanlış tahminler (düşük olmalı)

#### Validation Predictions

- Görsel sonuçlar
- Doğru/yanlış tespitler

### 6.2 Metrikler

#### mAP (mean Average Precision)

- **0.0-0.3**: Kötü
- **0.3-0.5**: Orta
- **0.5-0.7**: İyi ✅
- **0.7-0.9**: Çok iyi
- **0.9-1.0**: Mükemmel

#### Precision & Recall

- **Precision**: Doğru pozitif / Tüm pozitif
- **Recall**: Doğru pozitif / Gerçek pozitif

### 6.3 Model İyileştirme

**Düşük Doğruluk**:
1. Daha fazla veri ekleyin
2. Etiketleme kalitesini artırın
3. Daha büyük model deneyin
4. Daha fazla epoch

**Overfitting**:
1. Daha fazla veri ekleyin
2. Veri artırma kullanın
3. Erken durdurma (patience)
4. Daha küçük model

---

## 7. Segmentasyon

### 7.1 Model Yükleme

1. **AI Segmentasyon** sayfasına gidin
2. Eğitilmiş modeli seçin (örn: `model_20250101_120000.pt`)
3. **"Modeli Yükle"** butonuna tıklayın

**Sonuç**: "✅ Model yüklendi"

### 7.2 Segmentasyon Yapma

1. **"Panoramik X-Ray Yükle"** ile yeni görüntü yükleyin
2. Parametreleri ayarlayın:
   - Güven Eşiği: 0.25 (varsayılan)
   - IoU Eşiği: 0.45 (varsayılan)
3. **"Segmentasyon Yap"** butonuna tıklayın

### 7.3 Sonuçları Yorumlama

#### Tespit Sayısı

- **Çok az**: Güven eşiğini düşürün
- **Çok fazla**: Güven eşiğini yükseltin
- **Uygun**: Dengeli

#### Güven Skorları

- **Yüksek (>0.7)**: Kesin tespit
- **Orta (0.4-0.7)**: Olası tespit
- **Düşük (<0.4)**: Belirsiz

#### Görsel Kontrol

- Maskeler doğru mu?
- Sınırlar net mi?
- Yanlış pozitif var mı?

### 7.4 Sonuçları Kaydetme

**"Sonuçları Kaydet"** butonuna tıklayın

**Kaydedilen**:
- Orijinal görüntü
- Segmentasyon sonucu
- Her tespit için maske
- Detaylı rapor (TXT)

**Konum**: `outputs/inference_results/inference_YYYYMMDD_HHMMSS/`

---

## 8. İleri Seviye

### 8.1 Batch İşleme

Birden fazla görüntüyü aynı anda işleyin:

```python
# example_usage.py kullanın
python example_usage.py

# Seçenek 4: Batch Processing
```

### 8.2 Model Karşılaştırma

Farklı modelleri karşılaştırın:

1. Nano, Small, Medium eğitin
2. Aynı test görüntüsünde deneyin
3. Sonuçları karşılaştırın

### 8.3 Veri Artırma

Daha fazla veri için:

```python
from PIL import Image, ImageEnhance

# Parlaklık artırma
img = Image.open('xray.jpg')
enhancer = ImageEnhance.Brightness(img)
img_bright = enhancer.enhance(1.5)
img_bright.save('xray_bright.jpg')
```

### 8.4 Transfer Learning

Farklı veri setlerinden faydalanın:

1. Genel dental veri setiyle ön-eğitim
2. Kendi verinizle fine-tuning

### 8.5 Ensemble Methods

Birden fazla modeli birleştirin:

```python
# Nano + Small + Medium
results_nano = model_nano.predict(img)
results_small = model_small.predict(img)
results_medium = model_medium.predict(img)

# Sonuçları birleştir (voting)
final_results = combine_results([results_nano, results_small, results_medium])
```

---

## 🎯 Özet Checklist

### Etiketleme ✅
- [ ] 50+ görüntü toplandı
- [ ] Her sınıftan örnekler var
- [ ] Poligonlar dikkatli çizildi
- [ ] Kalite kontrol yapıldı

### Eğitim ✅
- [ ] Veri seti hazırlandı (70/20/10)
- [ ] Model seçildi (Small)
- [ ] Parametreler ayarlandı
- [ ] Eğitim tamamlandı

### Değerlendirme ✅
- [ ] Loss curves incelendi
- [ ] mAP > 0.5
- [ ] Confusion matrix kontrol edildi
- [ ] Validation predictions görüldü

### Segmentasyon ✅
- [ ] Model yüklendi
- [ ] Test görüntüleri işlendi
- [ ] Sonuçlar tatmin edici
- [ ] Sonuçlar kaydedildi

---

## 🆘 Yardım

**Sorun mu yaşıyorsunuz?**

1. `README.md` dosyasına bakın
2. `DEPLOYMENT.md` için deployment sorunları
3. GitHub Issues açın
4. Email gönderin

**İyi çalışmalar!** 🚀

