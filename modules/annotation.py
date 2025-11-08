"""
Annotation module for dental panoramic X-ray segmentation
"""
import os
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import cv2
import json
from pathlib import Path
from typing import List, Dict, Tuple
from modules.utils import (
    load_config, save_yolo_annotation, load_yolo_annotation,
    hex_to_rgb, rgb_to_bgr, draw_polygon_on_image, get_image_dimensions
)


class AnnotationInterface:
    """Interface for annotating dental panoramic X-rays"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.classes = config['classes']
        self.raw_images_dir = config['paths']['raw_images']
        self.annotations_dir = config['paths']['annotations']
        
        # Initialize session state
        if 'current_image' not in st.session_state:
            st.session_state.current_image = None
        if 'current_annotations' not in st.session_state:
            st.session_state.current_annotations = []
        if 'annotation_mode' not in st.session_state:
            st.session_state.annotation_mode = 'draw'
    
    def render(self):
        """Render the annotation interface"""
        st.header("🖊️ Etiketleme Arayüzü")
        st.markdown("Panoramik diş röntgenlerinde diş, lezyon ve diğer yapıları etiketleyin.")
        
        # Create two columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self._render_canvas()
        
        with col2:
            self._render_controls()
    
    def _render_controls(self):
        """Render control panel"""
        st.subheader("Kontroller")
        
        # Image upload
        uploaded_file = st.file_uploader(
            "Panoramik X-Ray Yükle",
            type=self.config['image']['supported_formats'],
            help="Diş panoramik röntgen görüntüsü yükleyin"
        )
        
        if uploaded_file is not None:
            # Save uploaded image
            image_path = os.path.join(self.raw_images_dir, uploaded_file.name)
            with open(image_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            st.session_state.current_image = image_path
            st.success(f"✅ Görüntü yüklendi: {uploaded_file.name}")
            
            # Load existing annotations if any
            self._load_existing_annotations()
        
        # Image selection from existing
        st.markdown("---")
        st.subheader("📁 Panoramik Filmler")
        
        if os.path.exists(self.raw_images_dir):
            image_files = [f for f in os.listdir(self.raw_images_dir)
                          if f.lower().endswith(tuple(self.config['image']['supported_formats']))]
            
            if image_files:
                # Display image count
                st.info(f"📊 Toplam {len(image_files)} panoramik film")
                
                # List all images with thumbnails
                st.markdown("**Film Listesi:**")
                for idx, img_file in enumerate(image_files, 1):
                    img_path = os.path.join(self.raw_images_dir, img_file)
                    
                    # Create expandable section for each image
                    with st.expander(f"🦷 {idx}. {img_file}", expanded=False):
                        # Show thumbnail
                        try:
                            img = Image.open(img_path)
                            st.image(img, use_column_width=True)
                            
                            # Image info
                            img_width, img_height = img.size
                            st.caption(f"📐 Boyut: {img_width} x {img_height} piksel")
                            
                            # Check if annotated
                            label_name = Path(img_file).stem + '.txt'
                            label_path = os.path.join(self.annotations_dir, label_name)
                            if os.path.exists(label_path):
                                st.success("✅ Etiketlenmiş")
                            else:
                                st.warning("⚠️ Henüz etiketlenmemiş")
                            
                            # Load button
                            if st.button(f"📂 Bu Filmi Yükle", key=f"load_{idx}"):
                                st.session_state.current_image = img_path
                                self._load_existing_annotations()
                                st.rerun()
                        except Exception as e:
                            st.error(f"Görüntü yüklenemedi: {e}")
                
                st.markdown("---")
                # Quick select dropdown
                st.markdown("**Hızlı Seçim:**")
                selected_image = st.selectbox(
                    "Film Seç",
                    options=image_files,
                    help="Etiketlemek için bir film seçin"
                )
                
                if st.button("📂 Seçili Filmi Yükle", type="primary"):
                    st.session_state.current_image = os.path.join(self.raw_images_dir, selected_image)
                    self._load_existing_annotations()
                    st.rerun()
            else:
                st.info("📭 Henüz yüklenmiş film yok")
                st.markdown("👆 Yukarıdaki 'Panoramik X-Ray Yükle' butonunu kullanarak film ekleyin")
        
        # Class selection
        if st.session_state.current_image:
            st.markdown("---")
            st.subheader("Sınıf Seçimi")
            
            class_options = [f"{c['name_tr']} ({c['name']})" for c in self.classes]
            selected_class_idx = st.selectbox(
                "Etiket Sınıfı",
                options=range(len(self.classes)),
                format_func=lambda x: class_options[x],
                help="Çizmek istediğiniz yapının sınıfını seçin"
            )
            
            st.session_state.selected_class = selected_class_idx
            
            # Display color
            selected_color = self.classes[selected_class_idx]['color']
            st.color_picker("Sınıf Rengi", selected_color, disabled=True)
            
            # Annotation list
            st.markdown("---")
            st.subheader("Etiketler")
            
            if st.session_state.current_annotations:
                for idx, ann in enumerate(st.session_state.current_annotations):
                    class_name = self.classes[ann['class_id']]['name_tr']
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.text(f"{idx + 1}. {class_name} ({len(ann['polygon'])} nokta)")
                    with col_b:
                        if st.button("🗑️", key=f"delete_{idx}"):
                            st.session_state.current_annotations.pop(idx)
                            self._save_annotations()
                            st.rerun()
            else:
                st.info("Henüz etiket yok")
            
            # Save button
            st.markdown("---")
            if st.button("💾 Etiketleri Kaydet", type="primary", use_container_width=True):
                self._save_annotations()
                st.success("✅ Etiketler kaydedildi!")
            
            # Clear all button
            if st.session_state.current_annotations:
                if st.button("🗑️ Tüm Etiketleri Temizle", use_container_width=True):
                    st.session_state.current_annotations = []
                    self._save_annotations()
                    st.rerun()
    
    def _render_canvas(self):
        """Render the annotation canvas"""
        if st.session_state.current_image is None:
            st.info("👈 Lütfen sol panelden bir görüntü yükleyin veya seçin")
            return
        
        # Load image
        image = Image.open(st.session_state.current_image)
        img_array = np.array(image)
        
        # Get image dimensions
        img_width, img_height = image.size
        
        # Calculate canvas size (maintain aspect ratio)
        canvas_width = self.config['image']['display_width']
        aspect_ratio = img_height / img_width
        canvas_height = int(canvas_width * aspect_ratio)
        
        # Display image info
        st.info(f"📐 Görüntü Boyutu: {img_width} x {img_height} piksel")
        
        # Instructions
        with st.expander("📖 Kullanım Talimatları", expanded=False):
            st.markdown("""
            ### Poligon Çizimi
            1. Sağ panelden etiket sınıfını seçin
            2. Görüntü üzerinde yapının etrafına tıklayarak poligon çizin
            3. Poligonu kapatmak için ilk noktaya yakın tıklayın
            4. Birden fazla yapı etiketleyebilirsiniz
            5. "Etiketleri Kaydet" butonuna tıklayarak kaydedin
            
            ### İpuçları
            - Diş, lezyon, dolgu gibi yapıları dikkatli çizin
            - Poligon en az 3 nokta içermelidir
            - Yanlış etiketleri silmek için sağ paneldeki çöp kutusu ikonunu kullanın
            """)
        
        # Drawing mode selection
        drawing_mode = st.radio(
            "Mod",
            options=["Poligon Çiz", "Görüntüle"],
            horizontal=True,
            help="Poligon çizmek veya sadece görüntülemek için mod seçin"
        )
        
        # Canvas for drawing
        if drawing_mode == "Poligon Çiz":
            stroke_color = self.classes[st.session_state.get('selected_class', 0)]['color']
            
            # Convert PIL Image to numpy array for canvas
            canvas_image = np.array(image)
            
            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",
                stroke_width=2,
                stroke_color=stroke_color,
                background_image=canvas_image,
                update_streamlit=True,
                height=canvas_height,
                width=canvas_width,
                drawing_mode="polygon",
                point_display_radius=3,
                key="canvas",
            )
            
            # Process canvas result
            if canvas_result.json_data is not None:
                objects = canvas_result.json_data["objects"]
                
                # Add new polygons to annotations
                if st.button("➕ Poligonu Ekle"):
                    if objects:
                        # Get the last drawn object
                        last_obj = objects[-1]
                        if last_obj['type'] == 'path':
                            # Extract polygon points
                            path = last_obj['path']
                            polygon = []
                            
                            for point in path:
                                if len(point) >= 2:
                                    # Scale coordinates back to original image size
                                    x = int((point[1] / canvas_width) * img_width)
                                    y = int((point[2] / canvas_height) * img_height)
                                    polygon.append((x, y))
                            
                            if len(polygon) >= 3:
                                # Add annotation
                                st.session_state.current_annotations.append({
                                    'class_id': st.session_state.get('selected_class', 0),
                                    'polygon': polygon
                                })
                                st.success(f"✅ Poligon eklendi ({len(polygon)} nokta)")
                                st.rerun()
                            else:
                                st.warning("⚠️ Poligon en az 3 nokta içermelidir")
        
        else:  # View mode
            # Draw existing annotations on image
            img_with_annotations = self._draw_annotations_on_image(img_array)
            st.image(img_with_annotations, use_container_width=True, caption="Etiketli Görüntü")
    
    def _draw_annotations_on_image(self, image: np.ndarray) -> np.ndarray:
        """Draw all annotations on the image"""
        img_copy = image.copy()
        
        for ann in st.session_state.current_annotations:
            class_id = ann['class_id']
            polygon = ann['polygon']
            
            # Get class color
            hex_color = self.classes[class_id]['color']
            rgb_color = hex_to_rgb(hex_color)
            bgr_color = rgb_to_bgr(rgb_color)
            
            # Draw polygon
            img_copy = draw_polygon_on_image(
                img_copy, polygon, bgr_color,
                thickness=3, fill=True, alpha=0.3
            )
            
            # Add label text
            if polygon:
                centroid_x = int(np.mean([p[0] for p in polygon]))
                centroid_y = int(np.mean([p[1] for p in polygon]))
                class_name = self.classes[class_id]['name_tr']
                
                cv2.putText(
                    img_copy, class_name,
                    (centroid_x, centroid_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, bgr_color, 2
                )
        
        return img_copy
    
    def _load_existing_annotations(self):
        """Load existing annotations for current image"""
        if st.session_state.current_image is None:
            return
        
        image_name = os.path.basename(st.session_state.current_image)
        label_name = Path(image_name).stem + '.txt'
        label_path = os.path.join(self.annotations_dir, label_name)
        
        if os.path.exists(label_path):
            img_width, img_height = get_image_dimensions(st.session_state.current_image)
            st.session_state.current_annotations = load_yolo_annotation(
                label_path, img_width, img_height
            )
        else:
            st.session_state.current_annotations = []
    
    def _save_annotations(self):
        """Save current annotations to file"""
        if st.session_state.current_image is None:
            return
        
        image_name = os.path.basename(st.session_state.current_image)
        img_width, img_height = get_image_dimensions(st.session_state.current_image)
        
        save_yolo_annotation(
            image_name,
            st.session_state.current_annotations,
            self.annotations_dir,
            img_width,
            img_height
        )


def render_annotation_page(config: Dict):
    """Main function to render annotation page"""
    interface = AnnotationInterface(config)
    interface.render()

