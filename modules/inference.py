"""
Inference module for YOLO11 segmentation models
"""
import os
import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
from typing import Dict, List, Tuple
import supervision as sv
from datetime import datetime
from modules.utils import load_config, hex_to_rgb, rgb_to_bgr


class InferenceInterface:
    """Interface for running inference with trained YOLO11 models"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.trained_models_dir = config['paths']['trained_models']
        self.inference_results_dir = config['paths']['inference_results']
        
        # Initialize session state
        if 'loaded_model' not in st.session_state:
            st.session_state.loaded_model = None
        if 'loaded_model_name' not in st.session_state:
            st.session_state.loaded_model_name = None
        if 'inference_results' not in st.session_state:
            st.session_state.inference_results = None
    
    def render(self):
        """Render the inference interface"""
        st.header("🔍 AI Segmentation")
        st.markdown("Eğitilmiş model ile panoramik diş röntgenlerinde otomatik segmentasyon yapın.")
        
        # Create two columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self._render_inference_area()
        
        with col2:
            self._render_controls()
    
    def _render_controls(self):
        """Render control panel"""
        st.subheader("Kontroller")
        
        # Model selection
        st.markdown("### Model Seçimi")
        
        if os.path.exists(self.trained_models_dir):
            model_files = [f for f in os.listdir(self.trained_models_dir) if f.endswith('.pt')]
            
            if model_files:
                selected_model = st.selectbox(
                    "Eğitilmiş Model",
                    options=sorted(model_files, reverse=True),
                    help="Kullanmak istediğiniz eğitilmiş modeli seçin"
                )
                
                # Load model button
                if st.button("📥 Modeli Yükle", use_container_width=True):
                    with st.spinner("Model yükleniyor..."):
                        try:
                            model_path = os.path.join(self.trained_models_dir, selected_model)
                            st.session_state.loaded_model = YOLO(model_path)
                            st.session_state.loaded_model_name = selected_model
                            st.success(f"✅ Model yüklendi: {selected_model}")
                        except Exception as e:
                            st.error(f"❌ Model yükleme hatası: {str(e)}")
                
                # Display loaded model
                if st.session_state.loaded_model_name:
                    st.info(f"🤖 Yüklü Model: {st.session_state.loaded_model_name}")
            else:
                st.warning("⚠️ Henüz eğitilmiş model yok. Önce bir model eğitin.")
                return
        else:
            st.error("❌ Model dizini bulunamadı!")
            return
        
        st.markdown("---")
        
        # Inference parameters
        st.markdown("### Tahmin Parametreleri")
        
        confidence = st.slider(
            "Güven Eşiği",
            min_value=0.0,
            max_value=1.0,
            value=self.config['inference']['default_confidence'],
            step=0.05,
            help="Minimum güven skoru (düşük değer = daha fazla tespit)"
        )
        
        iou_threshold = st.slider(
            "IoU Eşiği",
            min_value=0.0,
            max_value=1.0,
            value=self.config['inference']['default_iou'],
            step=0.05,
            help="Çakışan tespitler için eşik değeri"
        )
        
        st.markdown("---")
        
        # Visualization options
        st.markdown("### Görselleştirme")
        
        show_labels = st.checkbox("Etiketleri Göster", value=True)
        show_confidence = st.checkbox("Güven Skorlarını Göster", value=True)
        show_masks = st.checkbox("Maskeleri Göster", value=True)
        mask_alpha = st.slider("Maske Saydamlığı", 0.0, 1.0, 0.5, 0.1)
        
        # Store parameters in session state
        st.session_state.inference_params = {
            'confidence': confidence,
            'iou': iou_threshold,
            'show_labels': show_labels,
            'show_confidence': show_confidence,
            'show_masks': show_masks,
            'mask_alpha': mask_alpha
        }
        
        st.markdown("---")
        
        # Export options
        if st.session_state.inference_results is not None:
            st.markdown("### Dışa Aktarma")
            
            if st.button("💾 Sonuçları Kaydet", use_container_width=True):
                self._save_results()
    
    def _render_inference_area(self):
        """Render inference area"""
        if st.session_state.loaded_model is None:
            st.info("👉 Lütfen sağ panelden bir model yükleyin")
            return
        
        # Image upload
        uploaded_file = st.file_uploader(
            "Panoramik X-Ray Yükle",
            type=self.config['image']['supported_formats'],
            help="Segmentasyon yapmak için panoramik röntgen yükleyin"
        )
        
        if uploaded_file is not None:
            # Load image
            image = Image.open(uploaded_file)
            img_array = np.array(image)
            
            # Display original image
            st.subheader("Original Image")
            st.image(image, use_container_width=True)
            
            # Run inference button
            if st.button("🚀 Run Segmentation", type="primary", use_container_width=True):
                with st.spinner("Segmentasyon yapılıyor..."):
                    self._run_inference(img_array, uploaded_file.name)
            
            # Display results
            if st.session_state.inference_results is not None:
                self._display_results()
    
    def _run_inference(self, image: np.ndarray, image_name: str):
        """Run inference on image"""
        try:
            params = st.session_state.inference_params
            
            # Run model
            results = st.session_state.loaded_model.predict(
                image,
                conf=params['confidence'],
                iou=params['iou'],
                verbose=False
            )
            
            # Store results
            st.session_state.inference_results = {
                'results': results,
                'image': image,
                'image_name': image_name
            }
            
            st.success("✅ Segmentasyon tamamlandı!")
            
        except Exception as e:
            st.error(f"❌ Segmentasyon hatası: {str(e)}")
    
    def _display_results(self):
        """Display inference results"""
        st.markdown("---")
        st.subheader("Segmentation Results")
        
        results_data = st.session_state.inference_results
        results = results_data['results'][0]
        image = results_data['image']
        params = st.session_state.inference_params
        
        # Get detections
        if results.masks is not None:
            n_detections = len(results.masks)
            st.metric("Tespit Edilen Yapı Sayısı", n_detections)
            
            # Visualize results
            annotated_image = self._visualize_results(
                image.copy(),
                results,
                params
            )
            
            st.image(annotated_image, caption="Segmentasyon Sonucu", use_container_width=True)
            
            # Display detection details
            with st.expander("📋 Tespit Detayları", expanded=False):
                self._display_detection_details(results)
        else:
            st.warning("⚠️ Hiçbir yapı tespit edilemedi. Güven eşiğini düşürmeyi deneyin.")
    
    def _visualize_results(self, image: np.ndarray, results, params: Dict) -> np.ndarray:
        """Visualize segmentation results on image"""
        # Convert to BGR for OpenCV
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        elif image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.masks is None:
            return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Get masks and boxes
        masks = results.masks.data.cpu().numpy()
        boxes = results.boxes.data.cpu().numpy()
        
        # Draw each detection
        for idx, (mask, box) in enumerate(zip(masks, boxes)):
            class_id = int(box[5])
            confidence = float(box[4])
            
            # Get class info
            if class_id < len(self.config['classes']):
                class_info = self.config['classes'][class_id]
                class_name = class_info['name_tr']
                hex_color = class_info['color']
                rgb_color = hex_to_rgb(hex_color)
                bgr_color = rgb_to_bgr(rgb_color)
            else:
                class_name = f"Class {class_id}"
                bgr_color = (255, 0, 0)
            
            # Draw mask
            if params['show_masks']:
                # Resize mask to image size
                mask_resized = cv2.resize(
                    mask.astype(np.uint8),
                    (image.shape[1], image.shape[0])
                )
                
                # Create colored mask
                colored_mask = np.zeros_like(image)
                colored_mask[mask_resized > 0.5] = bgr_color
                
                # Blend with image
                image = cv2.addWeighted(
                    image,
                    1.0,
                    colored_mask,
                    params['mask_alpha'],
                    0
                )
            
            # Draw contours
            mask_resized = cv2.resize(
                mask.astype(np.uint8),
                (image.shape[1], image.shape[0])
            )
            contours, _ = cv2.findContours(
                mask_resized,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )
            cv2.drawContours(image, contours, -1, bgr_color, 2)
            
            # Draw label
            if params['show_labels'] or params['show_confidence']:
                x1, y1 = int(box[0]), int(box[1])
                
                label_parts = []
                if params['show_labels']:
                    label_parts.append(class_name)
                if params['show_confidence']:
                    label_parts.append(f"{confidence:.2f}")
                
                label = " - ".join(label_parts)
                
                # Draw label background
                (text_width, text_height), _ = cv2.getTextSize(
                    label,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    2
                )
                
                cv2.rectangle(
                    image,
                    (x1, y1 - text_height - 10),
                    (x1 + text_width + 10, y1),
                    bgr_color,
                    -1
                )
                
                # Draw label text
                cv2.putText(
                    image,
                    label,
                    (x1 + 5, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )
        
        # Convert back to RGB
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    def _display_detection_details(self, results):
        """Display detailed detection information"""
        if results.masks is None:
            return
        
        boxes = results.boxes.data.cpu().numpy()
        
        for idx, box in enumerate(boxes):
            class_id = int(box[5])
            confidence = float(box[4])
            x1, y1, x2, y2 = box[:4]
            
            # Get class name
            if class_id < len(self.config['classes']):
                class_name = self.config['classes'][class_id]['name_tr']
            else:
                class_name = f"Class {class_id}"
            
            st.markdown(f"**{idx + 1}. {class_name}**")
            st.write(f"- Güven: {confidence:.3f}")
            st.write(f"- Konum: ({int(x1)}, {int(y1)}) - ({int(x2)}, {int(y2)})")
            st.markdown("---")
    
    def _save_results(self):
        """Save inference results"""
        try:
            results_data = st.session_state.inference_results
            image = results_data['image']
            image_name = results_data['image_name']
            results = results_data['results'][0]
            params = st.session_state.inference_params
            
            # Create timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create output directory
            output_dir = os.path.join(
                self.inference_results_dir,
                f"inference_{timestamp}"
            )
            os.makedirs(output_dir, exist_ok=True)
            
            # Save annotated image
            annotated_image = self._visualize_results(
                image.copy(),
                results,
                params
            )
            annotated_path = os.path.join(output_dir, f"annotated_{image_name}")
            cv2.imwrite(annotated_path, cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
            
            # Save original image
            original_path = os.path.join(output_dir, f"original_{image_name}")
            cv2.imwrite(original_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            
            # Save masks
            if results.masks is not None:
                masks = results.masks.data.cpu().numpy()
                for idx, mask in enumerate(masks):
                    mask_path = os.path.join(output_dir, f"mask_{idx}.png")
                    mask_resized = cv2.resize(
                        (mask * 255).astype(np.uint8),
                        (image.shape[1], image.shape[0])
                    )
                    cv2.imwrite(mask_path, mask_resized)
            
            # Save detection info
            info_path = os.path.join(output_dir, "detections.txt")
            with open(info_path, 'w', encoding='utf-8') as f:
                f.write(f"Model: {st.session_state.loaded_model_name}\n")
                f.write(f"Image: {image_name}\n")
                f.write(f"Timestamp: {timestamp}\n")
                f.write(f"Confidence Threshold: {params['confidence']}\n")
                f.write(f"IoU Threshold: {params['iou']}\n\n")
                
                if results.masks is not None:
                    boxes = results.boxes.data.cpu().numpy()
                    f.write(f"Total Detections: {len(boxes)}\n\n")
                    
                    for idx, box in enumerate(boxes):
                        class_id = int(box[5])
                        confidence = float(box[4])
                        
                        if class_id < len(self.config['classes']):
                            class_name = self.config['classes'][class_id]['name_tr']
                        else:
                            class_name = f"Class {class_id}"
                        
                        f.write(f"Detection {idx + 1}:\n")
                        f.write(f"  Class: {class_name}\n")
                        f.write(f"  Confidence: {confidence:.3f}\n")
                        f.write(f"  Box: {box[:4].tolist()}\n\n")
            
            st.success(f"✅ Sonuçlar kaydedildi: {output_dir}")
            
        except Exception as e:
            st.error(f"❌ Kaydetme hatası: {str(e)}")


def render_inference_page(config: Dict):
    """Main function to render inference page"""
    interface = InferenceInterface(config)
    interface.render()

