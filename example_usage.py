"""
Example usage script for dental segmentation application
This script demonstrates how to use the application programmatically
"""

import os
from pathlib import Path
from ultralytics import YOLO
import cv2
import numpy as np

# Configuration
BASE_DIR = Path(__file__).parent
DATASET_DIR = BASE_DIR / "data" / "dataset"
TRAINED_MODELS_DIR = BASE_DIR / "models" / "trained"
OUTPUT_DIR = BASE_DIR / "outputs" / "example_results"


def example_training():
    """Example: Train a YOLO11 segmentation model"""
    print("=" * 60)
    print("EXAMPLE 1: Training YOLO11 Segmentation Model")
    print("=" * 60)
    
    # Check if dataset exists
    data_yaml = DATASET_DIR / "data.yaml"
    if not data_yaml.exists():
        print("❌ Dataset not found! Please prepare dataset first.")
        print("   Use the Streamlit app to annotate and prepare dataset.")
        return
    
    print("\n📦 Loading YOLO11 Small Segmentation model...")
    model = YOLO("yolo11s-seg.pt")
    
    print("\n🎓 Starting training...")
    print("   - Data:", data_yaml)
    print("   - Epochs: 10 (demo)")
    print("   - Batch Size: 8")
    print("   - Image Size: 640")
    
    try:
        results = model.train(
            data=str(data_yaml),
            epochs=10,  # Small number for demo
            batch=8,
            imgsz=640,
            project=str(BASE_DIR / "outputs" / "training_results"),
            name="example_training",
            exist_ok=True,
            verbose=True
        )
        
        print("\n✅ Training completed!")
        print(f"   Results saved to: outputs/training_results/example_training")
        
    except Exception as e:
        print(f"\n❌ Training failed: {str(e)}")


def example_inference():
    """Example: Run inference with trained model"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Running Inference")
    print("=" * 60)
    
    # Find trained model
    if not TRAINED_MODELS_DIR.exists():
        print("❌ No trained models found!")
        print("   Please train a model first using the Streamlit app.")
        return
    
    model_files = list(TRAINED_MODELS_DIR.glob("*.pt"))
    if not model_files:
        print("❌ No trained models found!")
        return
    
    # Use the latest model
    model_path = sorted(model_files)[-1]
    print(f"\n📥 Loading model: {model_path.name}")
    
    try:
        model = YOLO(str(model_path))
        
        # Find test images
        test_images_dir = DATASET_DIR / "images" / "test"
        if not test_images_dir.exists() or not list(test_images_dir.glob("*.jpg")):
            print("❌ No test images found!")
            print("   Please prepare dataset with test images.")
            return
        
        test_images = list(test_images_dir.glob("*.jpg"))[:3]  # First 3 images
        
        print(f"\n🔍 Running inference on {len(test_images)} images...")
        
        # Create output directory
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        for img_path in test_images:
            print(f"\n   Processing: {img_path.name}")
            
            # Run inference
            results = model.predict(
                str(img_path),
                conf=0.25,
                iou=0.45,
                verbose=False
            )
            
            # Get results
            result = results[0]
            
            if result.masks is not None:
                n_detections = len(result.masks)
                print(f"   ✅ Found {n_detections} detections")
                
                # Save annotated image
                annotated = result.plot()
                output_path = OUTPUT_DIR / f"result_{img_path.name}"
                cv2.imwrite(str(output_path), annotated)
                print(f"   💾 Saved to: {output_path}")
            else:
                print(f"   ⚠️  No detections found")
        
        print(f"\n✅ Inference completed!")
        print(f"   Results saved to: {OUTPUT_DIR}")
        
    except Exception as e:
        print(f"\n❌ Inference failed: {str(e)}")


def example_annotation_format():
    """Example: Show YOLO annotation format"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: YOLO Annotation Format")
    print("=" * 60)
    
    print("\n📝 YOLO segmentation format:")
    print("   Each line: <class_id> <x1> <y1> <x2> <y2> ... <xn> <yn>")
    print("   Coordinates are normalized (0-1 range)")
    
    print("\n📄 Example annotation file (tooth.txt):")
    print("   0 0.1 0.2 0.15 0.2 0.15 0.25 0.1 0.25")
    print("   1 0.5 0.5 0.55 0.5 0.55 0.55 0.5 0.55")
    
    print("\n🎨 Class IDs:")
    classes = [
        "0: tooth (diş)",
        "1: lesion (lezyon)",
        "2: filling (dolgu)",
        "3: crown (kron)",
        "4: implant (implant)",
        "5: root_canal (kanal tedavisi)",
        "6: caries (çürük)"
    ]
    for cls in classes:
        print(f"   {cls}")
    
    print("\n📂 Directory structure:")
    print("   data/dataset/")
    print("   ├── images/")
    print("   │   ├── train/")
    print("   │   ├── val/")
    print("   │   └── test/")
    print("   └── labels/")
    print("       ├── train/")
    print("       ├── val/")
    print("       └── test/")


def example_batch_processing():
    """Example: Batch process multiple images"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Batch Processing")
    print("=" * 60)
    
    # Find trained model
    if not TRAINED_MODELS_DIR.exists():
        print("❌ No trained models found!")
        return
    
    model_files = list(TRAINED_MODELS_DIR.glob("*.pt"))
    if not model_files:
        print("❌ No trained models found!")
        return
    
    model_path = sorted(model_files)[-1]
    print(f"\n📥 Loading model: {model_path.name}")
    
    try:
        model = YOLO(str(model_path))
        
        # Find all test images
        test_images_dir = DATASET_DIR / "images" / "test"
        if not test_images_dir.exists():
            print("❌ No test images directory found!")
            return
        
        test_images = list(test_images_dir.glob("*.jpg")) + list(test_images_dir.glob("*.png"))
        
        if not test_images:
            print("❌ No test images found!")
            return
        
        print(f"\n🔄 Batch processing {len(test_images)} images...")
        
        # Create output directory
        batch_output_dir = OUTPUT_DIR / "batch_results"
        batch_output_dir.mkdir(parents=True, exist_ok=True)
        
        total_detections = 0
        
        for idx, img_path in enumerate(test_images, 1):
            print(f"\n   [{idx}/{len(test_images)}] {img_path.name}")
            
            # Run inference
            results = model.predict(
                str(img_path),
                conf=0.25,
                save=False,
                verbose=False
            )
            
            result = results[0]
            
            if result.masks is not None:
                n_detections = len(result.masks)
                total_detections += n_detections
                print(f"       ✅ {n_detections} detections")
                
                # Save result
                annotated = result.plot()
                output_path = batch_output_dir / f"result_{img_path.name}"
                cv2.imwrite(str(output_path), annotated)
            else:
                print(f"       ⚠️  No detections")
        
        print(f"\n✅ Batch processing completed!")
        print(f"   Total images: {len(test_images)}")
        print(f"   Total detections: {total_detections}")
        print(f"   Average: {total_detections / len(test_images):.1f} detections/image")
        print(f"   Results saved to: {batch_output_dir}")
        
    except Exception as e:
        print(f"\n❌ Batch processing failed: {str(e)}")


def main():
    """Main function"""
    print("\n" + "=" * 60)
    print("DENTAL SEGMENTATION - EXAMPLE USAGE")
    print("=" * 60)
    
    print("\nThis script demonstrates various usage examples.")
    print("Make sure you have:")
    print("  1. Annotated images")
    print("  2. Prepared dataset (via Streamlit app)")
    print("  3. Trained model (optional for some examples)")
    
    print("\n" + "=" * 60)
    print("Available Examples:")
    print("=" * 60)
    print("1. Training")
    print("2. Inference")
    print("3. Annotation Format")
    print("4. Batch Processing")
    print("0. Run All")
    
    try:
        choice = input("\nSelect example (0-4): ").strip()
        
        if choice == "1":
            example_training()
        elif choice == "2":
            example_inference()
        elif choice == "3":
            example_annotation_format()
        elif choice == "4":
            example_batch_processing()
        elif choice == "0":
            example_annotation_format()
            example_training()
            example_inference()
            example_batch_processing()
        else:
            print("Invalid choice!")
    
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

