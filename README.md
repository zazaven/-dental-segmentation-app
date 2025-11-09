# Vir AI - Dental Panoramic X-Ray Segmentation Application

YOLO11-based AI-powered dental image analysis and segmentation tool.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-red.svg)
![YOLO11](https://img.shields.io/badge/YOLO11-Ultralytics-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌐 Live Demo

**[https://dental-segmentation.streamlit.app](https://dental-segmentation.streamlit.app)**

## ✨ Features

- 🖊️ **Interactive Annotation**: Polygon-based labeling with zoom support
- 🎓 **Model Training**: Train custom YOLO11 segmentation models
- 🔍 **AI Segmentation**: Automatic tooth and lesion detection
- 📊 **Multi-Class Support**: 7 dental structure classes
- 🎨 **Color-Coded Labels**: Visual class differentiation
- 💾 **YOLO Format**: Industry-standard annotation format

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/zazaven/-dental-segmentation-app.git
cd -dental-segmentation-app

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

## 📖 Documentation

For detailed documentation, see the [original README backup](README.md.backup).

## 🏗️ Architecture

```
vir-ai/
├── app.py                  # Main application
├── config/config.yaml      # Configuration
├── modules/               # Core modules
├── data/                  # Images and annotations
├── models/                # Trained models
└── outputs/               # Results
```

## 🤝 Contributing

Contributions welcome! Please submit a Pull Request.

## 📄 License

MIT License

---

**Made with ❤️ using YOLO11 and Streamlit**
