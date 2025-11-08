# 🚀 Hızlı Başlangıç Kılavuzu

Bu kılavuz, uygulamayı 10 dakikada çalıştırmanızı sağlar.

## 1. Kurulum (2 dakika)

```bash
# Depoyu klonlayın
git clone https://github.com/yourusername/dental-segmentation-app.git
cd dental-segmentation-app

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Uygulamayı başlatın
streamlit run app.py
```

Tarayıcınızda otomatik olarak açılacaktır: http://localhost:8501

## 2. İlk Etiketleme (3 dakika)

1. **Görüntü Yükle**
   - Sol menüden "🖊️ Etiketleme" seçin
   - "Panoramik X-Ray Yükle" butonuna tıklayın
   - Bir diş röntgeni seçin

2. **Poligon Çiz**
   - Sağ panelden "diş" sınıfını seçin
   - Bir dişin etrafına poligon çizin (en az 3 nokta)
   - "Poligonu Ekle" butonuna tıklayın

3. **Kaydet**
   - "Etiketleri Kaydet" butonuna tıklayın

**Tebrikler!** İlk etiketinizi oluşturdunuz. 🎉

## 3. Veri Seti Hazırlama (1 dakika)

1. En az 10-20 görüntü daha etiketleyin (daha fazlası daha iyi)
2. "🎓 Model Eğitimi" sayfasına gidin
3. "Veri Seti Hazırlama" sekmesinde
4. "Veri Setini Hazırla" butonuna tıklayın

## 4. Model Eğitimi (2 dakika + eğitim süresi)

1. "Model Eğitimi" sekmesine geçin
2. Model: **Small** seçin (önerilir)
3. Parametreler:
   - Epochs: 50 (hızlı test için)
   - Batch Size: 16
   - Image Size: 640
4. "Eğitimi Başlat" butonuna tıklayın

**Not**: Eğitim GPU ile 30-60 dakika, CPU ile 3-6 saat sürebilir.

## 5. Segmentasyon (2 dakika)

1. Eğitim tamamlandıktan sonra
2. "🔍 AI Segmentasyon" sayfasına gidin
3. Eğitilmiş modeli seçin ve "Modeli Yükle"
4. Yeni bir röntgen yükleyin
5. "Segmentasyon Yap" butonuna tıklayın

**Tebrikler!** İlk AI segmentasyonunuzu yaptınız! 🎊

## 💡 Hızlı İpuçları

- **Daha iyi sonuçlar için**: En az 50-100 görüntü etiketleyin
- **GPU kullanın**: Eğitimi 10-20x hızlandırır
- **Küçük başlayın**: İlk denemede Nano veya Small model kullanın
- **Etiketleme kalitesi**: Poligonları dikkatli çizin
- **Güven eşiği**: Çok az tespit varsa düşürün (0.25 → 0.15)

## 🆘 Sorun mu Yaşıyorsunuz?

### Eğitim başlamıyor
```bash
# Batch size'ı azaltın
Batch Size: 16 → 8
```

### Hiçbir şey tespit edilmiyor
```bash
# Güven eşiğini düşürün
Confidence: 0.25 → 0.15
```

### CUDA hatası
```bash
# CPU kullanın
Device: GPU → CPU
```

## 📚 Daha Fazla Bilgi

Detaylı dokümantasyon için `README.md` dosyasına bakın.

---

**Başarılar!** 🚀

