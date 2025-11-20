# 📊 Datasets Documentation - Krishi Sahayak

Complete guide to datasets used in the Krishi Sahayak AI Agriculture Assistant project.

---

## 📦 Overview

| Dataset | Size | Images | Classes | Task | Download Link |
|---------|------|--------|---------|------|---------------|
| Crop Health | ~3GB | 5,000+ | 4 | Classification | [ResearchGate](https://www.researchgate.net/publication/347442139_Detection_and_Prediction_of_Nutrient_Deficiency_Stress_using_Longitudinal_Aerial_Imagery) |
| Pest Detection | ~8GB | 10,000+ | 18 | Object Detection | [Roboflow](https://universe.roboflow.com/opa-gangnam-style/opa-2.00.2-dataset-2-v2/dataset/2/download) |
| Weed Detection | ~4GB | 3,000+ | 2 | Segmentation | [Roboflow](https://universe.roboflow.com/loki-orzgg/weed-detection-de08c) |
| Irrigation | ~5GB | 20,000+ | - | NDVI Analysis | [Agriculture-Vision](https://www.agriculture-vision.com/agriculture-vision-2020/dataset) |
| **Total** | **~20GB** | **38,000+** | **24** | **Multi-task** | - |

---

## 1. 🌿 Crop Health & Nutrient Deficiency Dataset

### Overview
Longitudinal dataset for detecting and predicting nutrient deficiency stress in crops using aerial imagery.

### Details
- **Name**: Longitudinal Nutrient Deficiency Dataset
- **Size**: ~3GB
- **Images**: 5,000+ high-resolution crop images
- **Resolution**: Variable (typically 1024×1024 to 2048×2048)
- **Format**: PNG/JPG with JSON annotations

### Classes (4)
1. **Healthy** - Normal, healthy crop appearance
2. **Nitrogen Deficiency** - Yellowing of older leaves, stunted growth
3. **Potassium Deficiency** - Leaf margin scorching, brown spots
4. **General Stress** - Multiple stress factors, unclear deficiency

### Download
- **Source**: [ResearchGate Publication](https://www.researchgate.net/publication/347442139_Detection_and_Prediction_of_Nutrient_Deficiency_Stress_using_Longitudinal_Aerial_Imagery)
- **Citation**: 
  ```
  Detection and Prediction of Nutrient Deficiency Stress using Longitudinal Aerial Imagery
  ResearchGate, 2020
  ```

### Folder Structure
```
data/longitudinal_nutrient_deficiency/
├── Longitudinal_Nutrient_Deficiency/
│   ├── field_001/
│   │   ├── image_i0.png
│   │   ├── image_i1.png
│   │   └── ...
│   ├── field_002/
│   └── ...
├── labels/
│   └── annotations.json
└── README.txt
```

### Usage in Project
- **Model**: ResNet50-based CNN
- **Task**: Multi-class classification
- **Training Script**: `train_crop_health_model.py`
- **Page**: `pages/1_🌿_Crop_Health.py`

---

## 2. 🐛 Pest Detection Dataset (OPA v2.00.2)

### Overview
Comprehensive dataset for detecting various agricultural pests in crop images.

### Details
- **Name**: OPA Pest Detection Dataset v2.00.2
- **Size**: ~8GB
- **Images**: 10,000+ annotated pest images
- **Resolution**: 640×640 (YOLO format)
- **Format**: JPG with YOLO txt annotations

### Classes (18)
1. **Atlas-moth** - Large moth species
2. **Black-Grass-Caterpillar** - Nocturnal caterpillar
3. **Coconut-black-headed-caterpillar** - Coconut palm pest
4. **Common cutworm** - Soil-dwelling larvae
5. **Cricket** - Grasshopper family
6. **Diamondback-moth** - Crucifer pest
7. **Fall-Armyworm** - Major crop pest
8. **Grasshopper** - Generalist herbivore
9. **Green-weevil** - Beetle pest
10. **Leaf-eating-caterpillar** - Foliage feeder
11. **Oriental-Mole-Cricket** - Underground pest
12. **Oriental-fruit-fly** - Fruit damaging pest
13. **Oryctes-rhinoceros** - Coconut rhinoceros beetle
14. **Red cotton steiner** - Cotton pest
15. **Rice-Bug** - Rice crop pest
16. **Stem-borer** - Internal stem feeder
17. **The-Plain-Tiger** - Butterfly species
18. **White-grub** - Beetle larvae

### Download
- **Source**: [Roboflow Universe - OPA Dataset](https://universe.roboflow.com/opa-gangnam-style/opa-2.00.2-dataset-2-v2/dataset/2/download)
- **Format**: YOLO v8 format
- **License**: Public Domain (check Roboflow for updates)

### Folder Structure
```
data/OPA_Pest_DIP_AI/
├── OPA_train/
│   ├── images/
│   │   ├── image_001.jpg
│   │   ├── image_002.jpg
│   │   └── ...
│   └── labels/
│       ├── image_001.txt
│       ├── image_002.txt
│       └── ...
├── OPA_valid/
│   ├── images/
│   └── labels/
├── OPA_test/
│   ├── images/
│   └── labels/
└── data.yaml
```

### Usage in Project
- **Model**: YOLOv8 (Ultralytics)
- **Task**: Object detection with bounding boxes
- **Training Script**: `train_pest_detection_model.py`
- **Page**: `pages/2_🐛_Pest_Detection.py`

---

## 3. 🌱 Weed Detection Dataset

### Overview
Semantic segmentation dataset for identifying weeds in agricultural fields.

### Details
- **Name**: Weed Detection Dataset
- **Size**: ~4GB
- **Images**: 3,000+ field images with pixel-level annotations
- **Resolution**: 512×512 to 1024×1024
- **Format**: JPG images with PNG masks

### Classes (2)
1. **Weed** - Unwanted plant species
2. **Background** - Crop and soil

### Download
- **Source**: [Roboflow Universe - Weed Detection](https://universe.roboflow.com/loki-orzgg/weed-detection-de08c)
- **Format**: Semantic segmentation masks
- **License**: Public Domain (check Roboflow for updates)

### Folder Structure
```
data/weed_detection_dataset/
├── weed_detection_dataset/
│   ├── train/
│   │   ├── images/
│   │   │   ├── img_001.jpg
│   │   │   └── ...
│   │   └── masks/
│   │       ├── img_001.png
│   │       └── ...
│   ├── valid/
│   │   ├── images/
│   │   └── masks/
│   └── test/
│       ├── images/
│       └── masks/
└── README.roboflow.txt
```

### Usage in Project
- **Model**: U-Net architecture
- **Task**: Semantic segmentation
- **Training Script**: `train_weed_segmentation_model.py`
- **Page**: `pages/3_🌱_Weed_Detection.py`

---

## 4. 💧 Irrigation Management Dataset (Agriculture-Vision-2021)

### Overview
Large-scale aerial imagery dataset for agricultural pattern recognition and irrigation management.

### Details
- **Name**: Agriculture-Vision-2021
- **Size**: ~5GB
- **Images**: 20,000+ aerial/satellite images
- **Resolution**: 512×512 patches
- **Format**: RGB + NIR (4-channel TIFF)

### Tasks
- NDVI (Normalized Difference Vegetation Index) calculation
- Water stress detection
- Irrigation zone mapping
- Crop health monitoring

### Download
- **Source**: [Agriculture-Vision Challenge 2020](https://www.agriculture-vision.com/agriculture-vision-2020/dataset)
- **Competition**: CVPR 2020 Workshop
- **License**: Academic use (check website for commercial use)

### Folder Structure
```
data/Agriculture-Vision-2021/
├── Agriculture-Vision-2021/
│   ├── train/
│   │   ├── images/
│   │   │   ├── rgb/
│   │   │   └── nir/
│   │   └── labels/
│   ├── val/
│   │   ├── images/
│   │   └── labels/
│   └── test/
│       └── images/
└── README.txt
```

### Usage in Project
- **Model**: Custom NDVI processing + CNN
- **Task**: Water stress analysis, irrigation recommendations
- **Training Script**: `train_agriculture_vision_segmentation.py`
- **Page**: `pages/4_💧_Irrigation.py`

---

## 📥 Download Instructions

### Step 1: Create Data Folder
```bash
mkdir -p data
cd data
```

### Step 2: Download Each Dataset

#### Crop Health Dataset
1. Visit: https://www.researchgate.net/publication/347442139
2. Click "Download" or request access
3. Extract to: `data/longitudinal_nutrient_deficiency/`

#### Pest Detection Dataset
1. Visit: https://universe.roboflow.com/opa-gangnam-style/opa-2.00.2-dataset-2-v2/dataset/2/download
2. Select format: "YOLO v8"
3. Download and extract to: `data/OPA_Pest_DIP_AI/`

#### Weed Detection Dataset
1. Visit: https://universe.roboflow.com/loki-orzgg/weed-detection-de08c
2. Select format: "Semantic Segmentation Masks"
3. Download and extract to: `data/weed_detection_dataset/`

#### Irrigation Dataset
1. Visit: https://www.agriculture-vision.com/agriculture-vision-2020/dataset
2. Register for the challenge (if required)
3. Download dataset
4. Extract to: `data/Agriculture-Vision-2021/`

### Step 3: Verify Structure
```bash
python -c "
import os
datasets = [
    'longitudinal_nutrient_deficiency',
    'OPA_Pest_DIP_AI',
    'weed_detection_dataset',
    'Agriculture-Vision-2021'
]
for ds in datasets:
    path = f'data/{ds}'
    exists = '✅' if os.path.exists(path) else '❌'
    print(f'{exists} {ds}')
"
```

---

## 🔧 Data Preprocessing

### Crop Health
```python
# Resize to 224×224 for ResNet50
# Normalize: mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
# Augmentation: rotation, flip, brightness
```

### Pest Detection
```python
# Resize to 640×640 for YOLOv8
# Normalize: 0-1 range
# Augmentation: mosaic, mixup, HSV adjustment
```

### Weed Detection
```python
# Resize to 512×512 for U-Net
# Normalize: 0-1 range
# Augmentation: rotation, flip, elastic transform
```

### Irrigation
```python
# Calculate NDVI: (NIR - Red) / (NIR + Red)
# Normalize: -1 to 1 range
# Threshold for water stress zones
```

---

## 📊 Dataset Statistics

### Crop Health
- **Training**: 4,000 images
- **Validation**: 500 images
- **Testing**: 500 images
- **Class Distribution**: Balanced

### Pest Detection
- **Training**: 8,000 images
- **Validation**: 1,000 images
- **Testing**: 1,000 images
- **Annotations**: 50,000+ bounding boxes

### Weed Detection
- **Training**: 2,400 images
- **Validation**: 300 images
- **Testing**: 300 images
- **Pixel Accuracy**: 91%

### Irrigation
- **Training**: 16,000 images
- **Validation**: 2,000 images
- **Testing**: 2,000 images
- **Coverage**: Multiple crop types and seasons

---

## 📝 Citations

If you use these datasets in your research, please cite:

### Crop Health Dataset
```bibtex
@article{nutrient_deficiency_2020,
  title={Detection and Prediction of Nutrient Deficiency Stress using Longitudinal Aerial Imagery},
  author={[Authors]},
  journal={ResearchGate},
  year={2020}
}
```

### Agriculture-Vision Dataset
```bibtex
@inproceedings{agriculture_vision_2020,
  title={Agriculture-Vision: A Large Aerial Image Database for Agricultural Pattern Analysis},
  booktitle={CVPR Workshops},
  year={2020}
}
```

---

## 🆘 Troubleshooting

### Issue: Download links not working
**Solution**: Datasets may require registration or have moved. Check the original sources or open a GitHub issue.

### Issue: Insufficient disk space
**Solution**: Download only the datasets you need. Each can be used independently.

### Issue: Extraction errors
**Solution**: Ensure you have the correct extraction tools (7zip, tar, unzip) and sufficient permissions.

---

## 📞 Support

For dataset-related questions:
- Check dataset source websites
- Open an issue on GitHub
- Contact dataset authors directly

---

**Last Updated**: November 2024

**Total Dataset Size**: ~20GB

**Total Images**: 38,000+

**Ready for Training**: ✅
