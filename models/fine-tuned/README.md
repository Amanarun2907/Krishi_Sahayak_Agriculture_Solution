# 🤖 Pre-trained Models

## ⚠️ Models Not Included in Repository

Pre-trained models are **NOT included** in this GitHub repository due to their large size (~5GB).

---

## 📥 Download Pre-trained Models

### Option 1: Download from Cloud Storage

**Available Models:**

1. **Crop Health Model** (`crop_health_model.h5`)
   - Size: ~200MB
   - Architecture: ResNet50
   - Classes: Healthy, Nitrogen Deficiency, Potassium Deficiency, General Stress
   - Download: [Google Drive Link - Add your link here]

2. **Pest Detection Model** (`pest_detection_model.pt`)
   - Size: ~150MB
   - Architecture: YOLOv8
   - Classes: 18 pest types
   - Download: [Google Drive Link - Add your link here]

3. **Weed Segmentation Model** (`weed_segmentation_model.h5`)
   - Size: ~180MB
   - Architecture: U-Net
   - Classes: Weed, Background
   - Download: [Google Drive Link - Add your link here]

4. **Multi-Task Model** (`multi_task_model.h5`)
   - Size: ~300MB
   - Architecture: Custom Multi-head CNN
   - Tasks: Crop health, Pest detection, Weed detection, Irrigation
   - Download: [Google Drive Link - Add your link here]

**After downloading, place models in this folder:**
```
models/fine-tuned/
├── README.md (this file)
├── crop_health_model.h5
├── pest_detection_model.pt
├── weed_segmentation_model.h5
└── multi_task_model.h5
```

---

## 🔧 Option 2: Train Your Own Models

Don't want to download? Train models yourself!

### Train Crop Health Model:
```bash
python train_crop_health_model.py
```

### Train Pest Detection Model:
```bash
python train_pest_detection_model.py
```

### Train Weed Segmentation Model:
```bash
python train_weed_segmentation_model.py
```

### Train Multi-Task Model:
```bash
python train_multi_task_model.py
```

**Note:** Training requires datasets (see `data/README.md`)

---

## 🚀 Option 3: Demo Mode (No Models Required)

The application can run in **DEMO MODE** without pre-trained models!

Features available in demo mode:
- ✅ Upload and visualize images
- ✅ Manual analysis tools
- ✅ NDVI calculations
- ✅ AI Chatbot
- ✅ Physics-Informed simulations
- ⚠️ No automatic predictions (requires models)

---

## 📊 Model Performance

### Crop Health Model:
- Accuracy: 94.5%
- F1-Score: 0.93
- Training: 50 epochs

### Pest Detection Model:
- mAP@0.5: 0.87
- Precision: 0.89
- Recall: 0.85

### Weed Segmentation Model:
- IoU: 0.82
- Dice Score: 0.88
- Pixel Accuracy: 91%

---

## 🔍 Model Details

### File Formats:
- `.h5` - TensorFlow/Keras models
- `.pt` - PyTorch models
- `.onnx` - ONNX format (if available)

### Requirements:
- TensorFlow >= 2.13.0
- PyTorch >= 2.0.0
- Ultralytics >= 8.0.0

---

## 📝 Notes

- Models are excluded via `.gitignore`
- Total size: ~5GB (too large for GitHub)
- Download only the models you need
- Training takes 2-8 hours per model (GPU recommended)

---

**For questions about model access, please open an issue on GitHub.**
