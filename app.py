"""
Dental Panoramic X-Ray Segmentation Application
YOLO11-based AI segmentation tool for dental imaging
"""
import streamlit as st
import os
import sys
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.utils import load_config
from modules.annotation import render_annotation_page
from modules.training import render_training_page
from modules.inference import render_inference_page


def main():
    """Main application"""
    
    # Load configuration
    config = load_config()
    
    # Page configuration
    st.set_page_config(
        page_title=config['app']['title'],
        page_icon=config['app']['page_icon'],
        layout=config['app']['layout'],
        initial_sidebar_state=config['app']['initial_sidebar_state']
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            color: #1f77b4;
            margin-bottom: 1rem;
        }
        .sub-header {
            text-align: center;
            color: #666;
            margin-bottom: 2rem;
        }
        .stButton>button {
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/tooth.png", width=80)
        st.title(config['app']['title'])
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigasyon",
            options=["🏠 Ana Sayfa", "🖊️ Etiketleme", "🎓 Model Eğitimi", "🔍 AI Segmentasyon"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Info
        with st.expander("ℹ️ Hakkında"):
            st.markdown("""
            **Dental Panoramik X-Ray Segmentasyon**
            
            YOLO11 tabanlı AI segmentasyon aracı
            
            **Özellikler:**
            - Poligon tabanlı etiketleme
            - Özel model eğitimi
            - Otomatik segmentasyon
            - Çoklu sınıf desteği
            
            **Sınıflar:**
            """)
            for cls in config['classes']:
                st.markdown(f"- {cls['name_tr']} ({cls['name']})")
        
        # Statistics
        with st.expander("📊 İstatistikler"):
            # Count files
            n_images = 0
            n_annotations = 0
            n_models = 0
            
            raw_images_dir = config['paths']['raw_images']
            annotations_dir = config['paths']['annotations']
            trained_models_dir = config['paths']['trained_models']
            
            if os.path.exists(raw_images_dir):
                n_images = len([f for f in os.listdir(raw_images_dir)
                               if f.lower().endswith(tuple(config['image']['supported_formats']))])
            
            if os.path.exists(annotations_dir):
                n_annotations = len([f for f in os.listdir(annotations_dir)
                                    if f.endswith('.txt')])
            
            if os.path.exists(trained_models_dir):
                n_models = len([f for f in os.listdir(trained_models_dir)
                               if f.endswith('.pt')])
            
            st.metric("Yüklenmiş Görüntü", n_images)
            st.metric("Etiketlenmiş Görüntü", n_annotations)
            st.metric("Eğitilmiş Model", n_models)
    
    # Main content
    if page == "🏠 Ana Sayfa":
        render_home_page(config)
    elif page == "🖊️ Etiketleme":
        render_annotation_page(config)
    elif page == "🎓 Model Eğitimi":
        render_training_page(config)
    elif page == "🔍 AI Segmentasyon":
        render_inference_page(config)


def render_home_page(config):
    """Render home page"""
    st.markdown('<div class="main-header">🦷 Dental Panoramik X-Ray Segmentasyon</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">YOLO11 ile AI Destekli Diş Görüntü Analizi</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Introduction
    st.markdown("""
    ## Hoş Geldiniz! 👋
    
    Bu uygulama, panoramik diş röntgenlerinde **diş**, **lezyon**, **dolgu** ve diğer dental yapıları 
    otomatik olarak tespit etmek ve segmente etmek için geliştirilmiş bir AI aracıdır.
    
    ### 🚀 Nasıl Çalışır?
    
    Uygulama üç ana adımdan oluşur:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 1️⃣ Etiketleme
        
        - Panoramik röntgen görüntülerini yükleyin
        - Diş, lezyon ve diğer yapıları poligonlarla işaretleyin
        - Sınıf etiketleri atayın
        - Etiketleri YOLO formatında kaydedin
        """)
    
    with col2:
        st.markdown("""
        ### 2️⃣ Model Eğitimi
        
        - Etiketlenmiş veri setini hazırlayın
        - YOLO11 model varyantını seçin
        - Eğitim parametrelerini ayarlayın
        - Modeli eğitin ve sonuçları görüntüleyin
        """)
    
    with col3:
        st.markdown("""
        ### 3️⃣ AI Segmentasyon
        
        - Eğitilmiş modeli yükleyin
        - Yeni panoramik röntgen yükleyin
        - Otomatik segmentasyon yapın
        - Sonuçları kaydedin ve analiz edin
        """)
    
    st.markdown("---")
    
    # Features
    st.markdown("""
    ## ✨ Özellikler
    
    ### 🎯 Etiketleme Arayüzü
    - **İnteraktif Poligon Çizimi**: Streamlit canvas ile kolay etiketleme
    - **Çoklu Sınıf Desteği**: Diş, lezyon, dolgu, kron, implant, kanal tedavisi, çürük
    - **Renk Kodlu Etiketler**: Her sınıf için farklı renk
    - **Düzenleme ve Silme**: Etiketleri kolayca yönetin
    - **YOLO Format**: Otomatik format dönüşümü
    
    ### 🎓 Model Eğitimi
    - **5 Model Varyantı**: Nano'dan Extra Large'a kadar
    - **Özelleştirilebilir Parametreler**: Epoch, batch size, learning rate, vb.
    - **Gerçek Zamanlı İzleme**: Eğitim ilerlemesini takip edin
    - **Otomatik Kaydetme**: En iyi model otomatik kaydedilir
    - **Görselleştirme**: Metrikler, confusion matrix, tahminler
    
    ### 🔍 AI Segmentasyon
    - **Otomatik Tespit**: Eğitilmiş model ile anlık segmentasyon
    - **Ayarlanabilir Eşikler**: Güven ve IoU eşiklerini özelleştirin
    - **Görselleştirme Seçenekleri**: Maskeler, etiketler, skorlar
    - **Sonuç Dışa Aktarma**: Görüntüler, maskeler ve detaylar
    - **Batch İşleme**: Birden fazla görüntüyü işleyin
    
    ## 📋 Desteklenen Sınıflar
    """)
    
    # Display classes
    for cls in config['classes']:
        col_a, col_b, col_c = st.columns([1, 2, 4])
        with col_a:
            st.markdown(f'<div style="width:30px;height:30px;background-color:{cls["color"]};border-radius:5px;"></div>', 
                       unsafe_allow_html=True)
        with col_b:
            st.markdown(f"**{cls['name_tr']}**")
        with col_c:
            st.markdown(f"{cls['name']}")
    
    st.markdown("---")
    
    # Getting started
    st.markdown("""
    ## 🎬 Başlangıç
    
    ### Adım 1: Görüntü Yükleme
    1. Sol menüden **🖊️ Etiketleme** sayfasına gidin
    2. Panoramik diş röntgeni yükleyin
    3. Görüntünüz otomatik olarak yüklenecektir
    
    ### Adım 2: Etiketleme
    1. Sağ panelden etiket sınıfını seçin
    2. Görüntü üzerinde yapının etrafına poligon çizin
    3. "Poligonu Ekle" butonuna tıklayın
    4. Tüm yapıları etiketledikten sonra "Etiketleri Kaydet"
    
    ### Adım 3: Veri Seti Hazırlama
    1. En az 10-20 görüntü etiketleyin (daha fazlası daha iyi)
    2. **🎓 Model Eğitimi** sayfasına gidin
    3. "Veri Setini Hazırla" butonuna tıklayın
    4. Veri seti otomatik olarak train/val/test'e bölünecek
    
    ### Adım 4: Model Eğitimi
    1. Model varyantını seçin (başlangıç için Small önerilir)
    2. Eğitim parametrelerini ayarlayın
    3. "Eğitimi Başlat" butonuna tıklayın
    4. Eğitim tamamlanana kadar bekleyin
    
    ### Adım 5: AI Segmentasyon
    1. **🔍 AI Segmentasyon** sayfasına gidin
    2. Eğitilmiş modeli yükleyin
    3. Yeni panoramik röntgen yükleyin
    4. "Segmentasyon Yap" butonuna tıklayın
    5. Sonuçları görüntüleyin ve kaydedin
    
    ## 💡 İpuçları
    
    - **Kaliteli Etiketleme**: Poligonları mümkün olduğunca doğru çizin
    - **Yeterli Veri**: En az 50-100 etiketlenmiş görüntü önerilir
    - **Dengeli Veri Seti**: Her sınıftan yeterli örnek bulundurun
    - **Veri Artırma**: Eğitim sırasında veri artırma kullanın
    - **Model Seçimi**: Küçük veri setleri için nano/small, büyük veri setleri için medium/large
    - **Epoch Sayısı**: 100-200 epoch genellikle yeterlidir
    - **GPU Kullanımı**: Mümkünse GPU ile eğitim yapın (çok daha hızlı)
    
    ## 🔧 Teknik Detaylar
    
    - **Model**: YOLO11 Instance Segmentation
    - **Framework**: Ultralytics
    - **Backend**: PyTorch
    - **UI**: Streamlit
    - **Format**: YOLO polygon format
    - **Görüntü Boyutu**: 640x640 (varsayılan)
    
    ## 📚 Kaynaklar
    
    - [YOLO11 Dokümantasyonu](https://docs.ultralytics.com/)
    - [Instance Segmentation Guide](https://docs.ultralytics.com/tasks/segment/)
    - [Training Tips](https://docs.ultralytics.com/modes/train/)
    
    ---
    
    ### 🚀 Hadi Başlayalım!
    
    Sol menüden **🖊️ Etiketleme** sayfasına giderek ilk görüntünüzü yükleyin.
    """)


if __name__ == "__main__":
    main()

