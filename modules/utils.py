"""
Utility functions for dental segmentation application
"""
import os
import yaml
import json
import shutil
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np
from PIL import Image
import cv2


def load_config(config_path: str = "config/config.yaml") -> Dict:
    """Load configuration from YAML file"""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def save_config(config: Dict, config_path: str = "config/config.yaml"):
    """Save configuration to YAML file"""
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)


def normalize_polygon(polygon: List[Tuple[float, float]], img_width: int, img_height: int) -> List[float]:
    """
    Normalize polygon coordinates to 0-1 range for YOLO format
    
    Args:
        polygon: List of (x, y) tuples
        img_width: Image width
        img_height: Image height
    
    Returns:
        Flattened list of normalized coordinates
    """
    normalized = []
    for x, y in polygon:
        norm_x = x / img_width
        norm_y = y / img_height
        normalized.extend([norm_x, norm_y])
    return normalized


def denormalize_polygon(normalized_coords: List[float], img_width: int, img_height: int) -> List[Tuple[int, int]]:
    """
    Denormalize polygon coordinates from YOLO format
    
    Args:
        normalized_coords: Flattened list of normalized coordinates
        img_width: Image width
        img_height: Image height
    
    Returns:
        List of (x, y) tuples
    """
    polygon = []
    for i in range(0, len(normalized_coords), 2):
        x = int(normalized_coords[i] * img_width)
        y = int(normalized_coords[i + 1] * img_height)
        polygon.append((x, y))
    return polygon


def save_yolo_annotation(image_name: str, annotations: List[Dict], output_path: str, img_width: int, img_height: int):
    """
    Save annotations in YOLO format
    
    Args:
        image_name: Name of the image file
        annotations: List of annotation dictionaries with 'class_id' and 'polygon'
        output_path: Path to save the annotation file
        img_width: Image width
        img_height: Image height
    """
    # Create label file name (same as image but .txt extension)
    label_name = Path(image_name).stem + '.txt'
    label_path = os.path.join(output_path, label_name)
    
    with open(label_path, 'w') as f:
        for ann in annotations:
            class_id = ann['class_id']
            polygon = ann['polygon']
            
            # Normalize coordinates
            normalized = normalize_polygon(polygon, img_width, img_height)
            
            # Write line: class_id x1 y1 x2 y2 ... xn yn
            line = f"{class_id} " + " ".join([f"{coord:.6f}" for coord in normalized])
            f.write(line + '\n')


def load_yolo_annotation(label_path: str, img_width: int, img_height: int) -> List[Dict]:
    """
    Load annotations from YOLO format file
    
    Args:
        label_path: Path to the label file
        img_width: Image width
        img_height: Image height
    
    Returns:
        List of annotation dictionaries
    """
    annotations = []
    
    if not os.path.exists(label_path):
        return annotations
    
    with open(label_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 7:  # At least class_id + 3 points (6 coords)
                continue
            
            class_id = int(parts[0])
            coords = [float(x) for x in parts[1:]]
            
            # Denormalize coordinates
            polygon = denormalize_polygon(coords, img_width, img_height)
            
            annotations.append({
                'class_id': class_id,
                'polygon': polygon
            })
    
    return annotations


def create_dataset_yaml(dataset_path: str, class_names: List[str], output_path: str = None):
    """
    Create data.yaml file for YOLO training
    
    Args:
        dataset_path: Path to dataset directory
        class_names: List of class names
        output_path: Path to save data.yaml (default: dataset_path/data.yaml)
    """
    if output_path is None:
        output_path = os.path.join(dataset_path, 'data.yaml')
    
    data_yaml = {
        'path': os.path.abspath(dataset_path),
        'train': 'images/train',
        'val': 'images/val',
        'test': 'images/test',
        'nc': len(class_names),
        'names': class_names
    }
    
    with open(output_path, 'w') as f:
        yaml.dump(data_yaml, f, default_flow_style=False)
    
    return output_path


def split_dataset(source_images_dir: str, source_labels_dir: str, 
                  dest_dataset_dir: str, train_ratio: float = 0.7, 
                  val_ratio: float = 0.2, test_ratio: float = 0.1):
    """
    Split dataset into train/val/test sets
    
    Args:
        source_images_dir: Directory containing all images
        source_labels_dir: Directory containing all labels
        dest_dataset_dir: Destination dataset directory
        train_ratio: Ratio for training set
        val_ratio: Ratio for validation set
        test_ratio: Ratio for test set
    """
    # Get all image files
    image_files = [f for f in os.listdir(source_images_dir) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
    
    # Shuffle images
    np.random.shuffle(image_files)
    
    # Calculate split indices
    n_total = len(image_files)
    n_train = int(n_total * train_ratio)
    n_val = int(n_total * val_ratio)
    
    # Split files
    train_files = image_files[:n_train]
    val_files = image_files[n_train:n_train + n_val]
    test_files = image_files[n_train + n_val:]
    
    # Copy files to respective directories
    for split_name, files in [('train', train_files), ('val', val_files), ('test', test_files)]:
        for img_file in files:
            # Copy image
            src_img = os.path.join(source_images_dir, img_file)
            dst_img = os.path.join(dest_dataset_dir, 'images', split_name, img_file)
            shutil.copy2(src_img, dst_img)
            
            # Copy label if exists
            label_file = Path(img_file).stem + '.txt'
            src_label = os.path.join(source_labels_dir, label_file)
            if os.path.exists(src_label):
                dst_label = os.path.join(dest_dataset_dir, 'labels', split_name, label_file)
                shutil.copy2(src_label, dst_label)
    
    return {
        'train': len(train_files),
        'val': len(val_files),
        'test': len(test_files)
    }


def draw_polygon_on_image(image: np.ndarray, polygon: List[Tuple[int, int]], 
                         color: Tuple[int, int, int], thickness: int = 2, 
                         fill: bool = False, alpha: float = 0.3) -> np.ndarray:
    """
    Draw polygon on image
    
    Args:
        image: Input image (numpy array)
        polygon: List of (x, y) tuples
        color: RGB color tuple
        thickness: Line thickness
        fill: Whether to fill the polygon
        alpha: Transparency for filled polygon
    
    Returns:
        Image with polygon drawn
    """
    img_copy = image.copy()
    pts = np.array(polygon, np.int32).reshape((-1, 1, 2))
    
    if fill:
        overlay = img_copy.copy()
        cv2.fillPoly(overlay, [pts], color)
        cv2.addWeighted(overlay, alpha, img_copy, 1 - alpha, 0, img_copy)
    
    cv2.polylines(img_copy, [pts], True, color, thickness)
    
    return img_copy


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_bgr(rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """Convert RGB to BGR (for OpenCV)"""
    return (rgb[2], rgb[1], rgb[0])


def resize_image_keep_aspect(image: np.ndarray, max_width: int = 800, max_height: int = 600) -> np.ndarray:
    """
    Resize image while keeping aspect ratio
    
    Args:
        image: Input image
        max_width: Maximum width
        max_height: Maximum height
    
    Returns:
        Resized image
    """
    h, w = image.shape[:2]
    
    # Calculate scaling factor
    scale = min(max_width / w, max_height / h)
    
    if scale < 1:
        new_w = int(w * scale)
        new_h = int(h * scale)
        return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    return image


def get_image_dimensions(image_path: str) -> Tuple[int, int]:
    """Get image width and height"""
    img = Image.open(image_path)
    return img.size  # Returns (width, height)


def count_annotations(labels_dir: str) -> int:
    """Count total number of annotations in a directory"""
    total = 0
    for label_file in os.listdir(labels_dir):
        if label_file.endswith('.txt'):
            label_path = os.path.join(labels_dir, label_file)
            with open(label_path, 'r') as f:
                total += len(f.readlines())
    return total


def validate_dataset(dataset_path: str) -> Dict:
    """
    Validate dataset structure and count files
    
    Args:
        dataset_path: Path to dataset directory
    
    Returns:
        Dictionary with validation results
    """
    results = {
        'valid': True,
        'errors': [],
        'train_images': 0,
        'train_labels': 0,
        'val_images': 0,
        'val_labels': 0,
        'test_images': 0,
        'test_labels': 0
    }
    
    # Check directory structure
    required_dirs = [
        'images/train', 'images/val', 'images/test',
        'labels/train', 'labels/val', 'labels/test'
    ]
    
    for dir_path in required_dirs:
        full_path = os.path.join(dataset_path, dir_path)
        if not os.path.exists(full_path):
            results['valid'] = False
            results['errors'].append(f"Missing directory: {dir_path}")
    
    # Count files
    for split in ['train', 'val', 'test']:
        images_dir = os.path.join(dataset_path, 'images', split)
        labels_dir = os.path.join(dataset_path, 'labels', split)
        
        if os.path.exists(images_dir):
            results[f'{split}_images'] = len([f for f in os.listdir(images_dir) 
                                             if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))])
        
        if os.path.exists(labels_dir):
            results[f'{split}_labels'] = len([f for f in os.listdir(labels_dir) 
                                             if f.endswith('.txt')])
    
    return results

