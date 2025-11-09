"""
Training module for YOLO11 segmentation models
"""
import os
import streamlit as st
from ultralytics import YOLO
import yaml
from pathlib import Path
from typing import Dict, Optional
import time
from datetime import datetime
import shutil
from modules.utils import (
    load_config, split_dataset, create_dataset_yaml,
    validate_dataset, count_annotations
)


class TrainingInterface:
    """Interface for training YOLO11 segmentation models"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.raw_images_dir = config['paths']['raw_images']
        self.annotations_dir = config['paths']['annotations']
        self.dataset_dir = config['paths']['dataset']
        self.pretrained_models_dir = config['paths']['pretrained_models']
        self.trained_models_dir = config['paths']['trained_models']
        self.training_results_dir = config['paths']['training_results']
        
        # Initialize session state
        if 'training_in_progress' not in st.session_state:
            st.session_state.training_in_progress = False
        if 'training_model' not in st.session_state:
            st.session_state.training_model = None
    
    def render(self):
        """Render the training interface"""
        st.header("🎓 Model Training")
        st.markdown("YOLO11 segmentasyon modelini özel veri setiniz üzerinde eğitin.")
        
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["📊 Dataset Preparation", "⚙️ Model Training", "📈 Training History"])
        
        with tab1:
            self._render_dataset_preparation()
        
        with tab2:
            self._render_training_config()
        
        with tab3:
            self._render_training_history()
    
    def _render_dataset_preparation(self):
        """Render dataset preparation section"""
        st.subheader("Dataset Preparation")
        
        # Check annotated images
        if os.path.exists(self.annotations_dir):
            annotation_files = [f for f in os.listdir(self.annotations_dir) if f.endswith('.txt')]
            n_annotated = len(annotation_files)
            
            st.metric("Annotated Images Count", n_annotated)
            
            if n_annotated > 0:
                total_annotations = count_annotations(self.annotations_dir)
                st.metric("Total Annotations Count", total_annotations)
            
            if n_annotated < 10:
                st.warning("⚠️ En az 10 etiketlenmiş görüntü önerilir. Daha fazla görüntü etiketleyin.")
        else:
            st.error("❌ Etiket dizini bulunamadı!")
            return
        
        st.markdown("---")
        
        # Dataset split configuration
        st.subheader("Veri Seti Bölme Ayarları")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            train_ratio = st.slider(
                "Eğitim Oranı",
                min_value=0.5,
                max_value=0.9,
                value=self.config['dataset']['train_ratio'],
                step=0.05,
                help="Eğitim için kullanılacak veri oranı"
            )
        
        with col2:
            val_ratio = st.slider(
                "Doğrulama Oranı",
                min_value=0.05,
                max_value=0.3,
                value=self.config['dataset']['val_ratio'],
                step=0.05,
                help="Doğrulama için kullanılacak veri oranı"
            )
        
        with col3:
            test_ratio = 1.0 - train_ratio - val_ratio
            st.metric("Test Oranı", f"{test_ratio:.2f}")
        
        # Validate ratios
        if abs(train_ratio + val_ratio + test_ratio - 1.0) > 0.01:
            st.error("❌ Oranların toplamı 1.0 olmalıdır!")
            return
        
        st.markdown("---")
        
        # Prepare dataset button
        if st.button("📦 Veri Setini Hazırla", type="primary", use_container_width=True):
            with st.spinner("Veri seti hazırlanıyor..."):
                try:
                    # Split dataset
                    split_counts = split_dataset(
                        self.raw_images_dir,
                        self.annotations_dir,
                        self.dataset_dir,
                        train_ratio,
                        val_ratio,
                        test_ratio
                    )
                    
                    # Create data.yaml
                    class_names = [c['name'] for c in self.config['classes']]
                    create_dataset_yaml(self.dataset_dir, class_names)
                    
                    # Display results
                    st.success("✅ Veri seti başarıyla hazırlandı!")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Eğitim", split_counts['train'])
                    col2.metric("Doğrulama", split_counts['val'])
                    col3.metric("Test", split_counts['test'])
                    
                except Exception as e:
                    st.error(f"❌ Hata: {str(e)}")
        
        # Validate dataset
        st.markdown("---")
        if st.button("✅ Veri Setini Doğrula"):
            validation = validate_dataset(self.dataset_dir)
            
            if validation['valid']:
                st.success("✅ Veri seti geçerli!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Eğitim:**")
                    st.write(f"- Görüntü: {validation['train_images']}")
                    st.write(f"- Etiket: {validation['train_labels']}")
                with col2:
                    st.write("**Doğrulama:**")
                    st.write(f"- Görüntü: {validation['val_images']}")
                    st.write(f"- Etiket: {validation['val_labels']}")
            else:
                st.error("❌ Veri seti geçersiz!")
                for error in validation['errors']:
                    st.error(f"- {error}")
    
    def _render_training_config(self):
        """Render training configuration section"""
        st.subheader("Model Eğitim Ayarları")
        
        # Check if dataset is ready
        data_yaml_path = os.path.join(self.dataset_dir, 'data.yaml')
        if not os.path.exists(data_yaml_path):
            st.warning("⚠️ Önce veri setini hazırlayın!")
            return
        
        # Model selection
        st.markdown("### Model Seçimi")
        
        model_options = {
            "yolo11n-seg.pt": "Nano (En Hızlı, 2.9M parametre)",
            "yolo11s-seg.pt": "Small (Önerilen, 10.1M parametre)",
            "yolo11m-seg.pt": "Medium (22.4M parametre)",
            "yolo11l-seg.pt": "Large (27.6M parametre)",
            "yolo11x-seg.pt": "Extra Large (En İyi Doğruluk, 62.1M parametre)"
        }
        
        selected_model = st.selectbox(
            "YOLO11 Model Varyantı",
            options=list(model_options.keys()),
            format_func=lambda x: model_options[x],
            index=1,  # Default to small
            help="Model boyutu arttıkça doğruluk artar ancak hız azalır"
        )
        
        st.markdown("---")
        
        # Training parameters
        st.markdown("### Eğitim Parametreleri")
        
        col1, col2 = st.columns(2)
        
        with col1:
            epochs = st.number_input(
                "Epoch Sayısı",
                min_value=10,
                max_value=500,
                value=self.config['training']['default_epochs'],
                step=10,
                help="Eğitim döngüsü sayısı (daha fazla epoch = daha iyi öğrenme)"
            )
            
            batch_size = st.number_input(
                "Batch Boyutu",
                min_value=4,
                max_value=64,
                value=self.config['training']['default_batch_size'],
                step=4,
                help="Her adımda işlenecek görüntü sayısı"
            )
            
            imgsz = st.selectbox(
                "Görüntü Boyutu",
                options=[320, 416, 512, 640, 800, 1024],
                index=3,  # 640
                help="Eğitim için görüntü boyutu (piksel)"
            )
        
        with col2:
            learning_rate = st.number_input(
                "Öğrenme Oranı",
                min_value=0.0001,
                max_value=0.1,
                value=self.config['training']['default_lr'],
                step=0.0001,
                format="%.4f",
                help="Model ağırlıklarının güncelleme hızı"
            )
            
            patience = st.number_input(
                "Patience (Erken Durdurma)",
                min_value=10,
                max_value=100,
                value=self.config['training']['patience'],
                step=5,
                help="İyileşme olmadan beklenecek epoch sayısı"
            )
            
            device = st.selectbox(
                "Cihaz",
                options=["0", "cpu"],
                format_func=lambda x: "GPU (CUDA)" if x == "0" else "CPU",
                help="Eğitim için kullanılacak cihaz"
            )
        
        st.markdown("---")
        
        # Advanced options
        with st.expander("🔧 Gelişmiş Ayarlar"):
            optimizer = st.selectbox(
                "Optimizer",
                options=["SGD", "Adam", "AdamW"],
                index=0,
                help="Optimizasyon algoritması"
            )
            
            augment = st.checkbox(
                "Veri Artırma",
                value=True,
                help="Eğitim sırasında veri artırma uygula"
            )
            
            save_period = st.number_input(
                "Model Kaydetme Periyodu",
                min_value=1,
                max_value=50,
                value=self.config['training']['save_period'],
                help="Her kaç epoch'ta bir model kaydedilecek"
            )
        
        st.markdown("---")
        
        # Training button
        if not st.session_state.training_in_progress:
            if st.button("🚀 Eğitimi Başlat", type="primary", use_container_width=True):
                self._start_training(
                    selected_model, epochs, batch_size, imgsz,
                    learning_rate, patience, device, optimizer,
                    augment, save_period
                )
        else:
            st.warning("⏳ Eğitim devam ediyor...")
            if st.button("⏹️ Eğitimi Durdur", use_container_width=True):
                st.session_state.training_in_progress = False
                st.rerun()
    
    def _start_training(self, model_name: str, epochs: int, batch_size: int,
                       imgsz: int, lr: float, patience: int, device: str,
                       optimizer: str, augment: bool, save_period: int):
        """Start model training"""
        try:
            st.session_state.training_in_progress = True
            
            # Create progress containers
            progress_bar = st.progress(0)
            status_text = st.empty()
            metrics_container = st.container()
            
            with st.spinner("Model yükleniyor..."):
                # Load model
                model = YOLO(model_name)
                st.session_state.training_model = model
            
            status_text.info("🎓 Eğitim başlatılıyor...")
            
            # Training configuration
            data_yaml_path = os.path.join(self.dataset_dir, 'data.yaml')
            
            # Create unique training name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            project_name = f"training_{timestamp}"
            
            # Train model
            results = model.train(
                data=data_yaml_path,
                epochs=epochs,
                batch=batch_size,
                imgsz=imgsz,
                lr0=lr,
                patience=patience,
                device=device,
                optimizer=optimizer,
                augment=augment,
                save_period=save_period,
                project=self.training_results_dir,
                name=project_name,
                exist_ok=True,
                verbose=True
            )
            
            # Training completed
            progress_bar.progress(100)
            status_text.success("✅ Eğitim tamamlandı!")
            
            # Copy best model to trained models directory
            best_model_path = os.path.join(
                self.training_results_dir, project_name, 'weights', 'best.pt'
            )
            
            if os.path.exists(best_model_path):
                dest_model_path = os.path.join(
                    self.trained_models_dir,
                    f"model_{timestamp}.pt"
                )
                shutil.copy2(best_model_path, dest_model_path)
                
                st.success(f"✅ En iyi model kaydedildi: model_{timestamp}.pt")
                
                # Display training results
                self._display_training_results(
                    os.path.join(self.training_results_dir, project_name)
                )
            
            st.session_state.training_in_progress = False
            
        except Exception as e:
            st.error(f"❌ Eğitim hatası: {str(e)}")
            st.session_state.training_in_progress = False
    
    def _display_training_results(self, results_dir: str):
        """Display training results"""
        st.markdown("---")
        st.subheader("📊 Eğitim Sonuçları")
        
        # Display result images
        result_images = {
            'results.png': 'Eğitim Metrikleri',
            'confusion_matrix.png': 'Karışıklık Matrisi',
            'val_batch0_pred.jpg': 'Doğrulama Tahminleri'
        }
        
        cols = st.columns(len(result_images))
        
        for idx, (img_name, title) in enumerate(result_images.items()):
            img_path = os.path.join(results_dir, img_name)
            if os.path.exists(img_path):
                with cols[idx]:
                    st.image(img_path, caption=title, use_container_width=True)
    
    def _render_training_history(self):
        """Render training history"""
        st.subheader("Training History")
        
        # List trained models
        if os.path.exists(self.trained_models_dir):
            model_files = [f for f in os.listdir(self.trained_models_dir) if f.endswith('.pt')]
            
            if model_files:
                st.metric("Eğitilmiş Model Sayısı", len(model_files))
                
                st.markdown("### Eğitilmiş Modeller")
                
                for model_file in sorted(model_files, reverse=True):
                    model_path = os.path.join(self.trained_models_dir, model_file)
                    file_size = os.path.getsize(model_path) / (1024 * 1024)  # MB
                    
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.text(f"📦 {model_file}")
                    with col2:
                        st.text(f"{file_size:.1f} MB")
                    with col3:
                        if st.button("🗑️", key=f"delete_model_{model_file}"):
                            os.remove(model_path)
                            st.rerun()
            else:
                st.info("Henüz eğitilmiş model yok")
        
        # List training results
        st.markdown("---")
        st.markdown("### Eğitim Sonuçları")
        
        if os.path.exists(self.training_results_dir):
            training_dirs = [d for d in os.listdir(self.training_results_dir)
                           if os.path.isdir(os.path.join(self.training_results_dir, d))]
            
            if training_dirs:
                selected_training = st.selectbox(
                    "Eğitim Seç",
                    options=sorted(training_dirs, reverse=True)
                )
                
                if selected_training:
                    results_dir = os.path.join(self.training_results_dir, selected_training)
                    self._display_training_results(results_dir)
            else:
                st.info("Henüz eğitim sonucu yok")


def render_training_page(config: Dict):
    """Main function to render training page"""
    interface = TrainingInterface(config)
    interface.render()

