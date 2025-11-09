"""
Vir AI - Dental Panoramic X-Ray Segmentation Application
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
        st.title("Vir AI")
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigation",
            options=["🏠 Home", "🖊️ Annotation", "🎓 Model Training", "🔍 AI Segmentation"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Info
        with st.expander("ℹ️ About"):
            st.markdown("""
            **Vir AI - Dental X-Ray Segmentation**
            
            YOLO11-based AI segmentation tool
            
            **Features:**
            - Polygon-based annotation
            - Custom model training
            - Automatic segmentation
            - Multi-class support
            
            **Classes:**
            """)
            for cls in config['classes']:
                st.markdown(f"- {cls['name'].title()}")
        
        # Statistics
        with st.expander("📊 Statistics"):
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
            
            st.metric("Uploaded Images", n_images)
            st.metric("Annotated Images", n_annotations)
            st.metric("Trained Models", n_models)
    
    # Main content
    if page == "🏠 Home":
        render_home_page(config)
    elif page == "🖊️ Annotation":
        render_annotation_page(config)
    elif page == "🎓 Model Training":
        render_training_page(config)
    elif page == "🔍 AI Segmentation":
        render_inference_page(config)


def render_home_page(config):
    """Render home page"""
    st.markdown('<div class="main-header">🦷 Vir AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Dental Panoramic X-Ray Analysis</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Introduction
    st.markdown("""
    ## Welcome! 👋
    
    This application is an AI tool developed to automatically detect and segment **teeth**, **lesions**, **fillings**, 
    and other dental structures in panoramic dental X-rays.
    
    ### 🚀 How It Works?
    
    The application consists of three main steps:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 1️⃣ Annotation
        
        - Upload panoramic X-ray images
        - Mark teeth, lesions and other structures with polygons
        - Assign class labels
        - Save annotations in YOLO format
        """)
    
    with col2:
        st.markdown("""
        ### 2️⃣ Model Training
        
        - Prepare labeled dataset
        - Select YOLO11 model variant
        - Configure training parameters
        - Train model and view results
        """)
    
    with col3:
        st.markdown("""
        ### 3️⃣ AI Segmentation
        
        - Load trained model
        - Upload new panoramic X-ray
        - Perform automatic segmentation
        - Save and analyze results
        """)
    
    st.markdown("---")
    
    # Features
    st.markdown("""
    ## ✨ Features
    
    ### 🎯 Annotation Interface
    - **Interactive Polygon Drawing**: Easy labeling with Streamlit canvas
    - **Multi-Class Support**: Tooth, lesion, filling, crown, implant, root canal, caries
    - **Color-Coded Labels**: Different color for each class
    - **Edit and Delete**: Easily manage annotations
    - **YOLO Format**: Automatic format conversion
    
    ### 🎓 Model Training
    - **5 Model Variants**: From Nano to Extra Large
    - **Customizable Parameters**: Epochs, batch size, learning rate, etc.
    - **Real-Time Monitoring**: Track training progress
    - **Auto-Save**: Best model saved automatically
    - **Visualization**: Metrics, confusion matrix, predictions
    
    ### 🔍 AI Segmentation
    - **Automatic Detection**: Instant segmentation with trained model
    - **Adjustable Thresholds**: Customize confidence and IoU thresholds
    - **Visualization Options**: Masks, labels, scores
    - **Export Results**: Images, masks and details
    - **Batch Processing**: Process multiple images
    
    ## 📋 Supported Classes
    """)
    
    # Display classes
    for cls in config['classes']:
        col_a, col_b = st.columns([1, 4])
        with col_a:
            st.markdown(f'<div style="width:30px;height:30px;background-color:{cls["color"]};border-radius:5px;"></div>', 
                       unsafe_allow_html=True)
        with col_b:
            st.markdown(f"**{cls['name'].title()}**")
    
    st.markdown("---")
    
    # Getting started
    st.markdown("""
    ## 🎬 Getting Started
    
    ### Step 1: Upload Images
    1. Go to **🖊️ Annotation** page from left menu
    2. Upload panoramic dental X-ray
    3. Your image will be loaded automatically
    
    ### Step 2: Annotation
    1. Select label class from right panel
    2. Draw polygon around structure on image
    3. Click "Add Polygon" button
    4. After labeling all structures, click "Save Annotations"
    
    ### Step 3: Dataset Preparation
    1. Label at least 10-20 images (more is better)
    2. Go to **🎓 Model Training** page
    3. Click "Prepare Dataset" button
    4. Dataset will be automatically split into train/val/test
    
    ### Step 4: Model Training
    1. Select model variant (Small recommended for beginners)
    2. Configure training parameters
    3. Click "Start Training" button
    4. Wait for training to complete
    
    ### Step 5: AI Segmentation
    1. Go to **🔍 AI Segmentation** page
    2. Load trained model
    3. Upload new panoramic X-ray
    4. Click "Run Segmentation" button
    5. View and save results
    
    ## 💡 Tips
    
    - **Quality Annotation**: Draw polygons as accurately as possible
    - **Sufficient Data**: At least 50-100 annotated images recommended
    - **Balanced Dataset**: Ensure sufficient examples from each class
    - **Data Augmentation**: Use data augmentation during training
    - **Model Selection**: Nano/small for small datasets, medium/large for large datasets
    - **Epoch Count**: 100-200 epochs usually sufficient
    - **GPU Usage**: Train with GPU if possible (much faster)
    
    ## 🔧 Technical Details
    
    - **Model**: YOLO11 Instance Segmentation
    - **Framework**: Ultralytics
    - **Backend**: PyTorch
    - **UI**: Streamlit
    - **Format**: YOLO polygon format
    - **Image Size**: 640x640 (default)
    
    ## 📚 Resources
    
    - [YOLO11 Documentation](https://docs.ultralytics.com/)
    - [Instance Segmentation Guide](https://docs.ultralytics.com/tasks/segment/)
    - [Training Tips](https://docs.ultralytics.com/modes/train/)
    
    ---
    
    ### 🚀 Let's Get Started!
    
    Go to **🖊️ Annotation** page from left menu to upload your first image.
    """)


if __name__ == "__main__":
    main()
