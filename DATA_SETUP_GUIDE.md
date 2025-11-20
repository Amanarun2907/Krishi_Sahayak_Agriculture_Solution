# 📦 Data & Model Setup Guide - Krishi Sahayak

## 🎯 Problem: Large Files (25GB+)

GitHub **cannot** and **should not** store:
- ❌ Large datasets (25GB)
- ❌ Trained models (100MB+ each)
- ❌ Image datasets
- ❌ Video files

**Solution:** Store data separately, provide download instructions.

---

## 📁 Project Structure

```
krishi-sahayak/
├── app.py                    ✅ Push to GitHub
├── config.py                 ✅ Push to GitHub
├── requirements.txt          ✅ Push to GitHub
├── .gitignore               ✅ Push to GitHub
├── .env.example             ✅ Push to GitHub
│
├── pages/                   ✅ Push to GitHub (Python code)
├── modules/                 ✅ Push to GitHub (Python code)
│
├── data/                    ❌ DON'T push (25GB!)
│   ├── Agriculture-Vision-2021/
│   ├── longitudinal_nutrient_deficiency/
│   ├── OPA_Pest_DIP_AI/
│   └── weed_detection_dataset/
│
└── models/                  ❌ DON'T push (large files)
    └── fine-tuned/
        ├── crop_health_model.h5
        ├── pest_detection_model.pt
        └── weed_segmentation_model.h5
```

---

## ✅ What to Push to GitHub

### Push These (Small Files):
- ✅ All Python code (`.py` files)
- ✅ Configuration files (`config.py`, `requirements.txt`)
- ✅ Documentation (`.md` files)
- ✅ `.gitignore` and `.env.example`
- ✅ Training scripts
- ✅ Empty folder structure

### DON'T Push These (Large Files):
- ❌ `data/` folder contents (25GB)
- ❌ `models/fine-tuned/*.h5` (trained models)
- ❌ `models/fine-tuned/*.pt` (PyTorch models)
- ❌ Image files, videos
- ❌ `.env` (API keys)

---

## 🔧 Implementation Steps

### Step 1: Update .gitignore

Your `.gitignore` already excludes data, but let's verify:

```bash
# Check if data is ignored
git check-ignore data/
git check-ignore models/fine-tuned/*.h5
```

### Step 2: Create Empty Folder Structure

```bash
# Create placeholder files to preserve folder structure
echo "# Data folder - Download datasets separately" > data/README.md
echo "# Models folder - Train or download models" > models/fine-tuned/README.md
```

### Step 3: Document Data Sources

Create `DATA_SOURCES.md` with download links.

---

## 📥 Data Download Options

### Option 1: Cloud Storage (Recommended)

**Upload your data to:**
- Google Drive
- Dropbox
- OneDrive
- AWS S3
- Kaggle Datasets

**Then provide download link in README**

### Option 2: Kaggle Datasets

```bash
# Upload to Kaggle
kaggle datasets create -p data/

# Users download with:
kaggle datasets download -d your-username/krishi-sahayak-data
```

### Option 3: Git LFS (Large File Storage)

**For files 100MB - 2GB:**

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.h5"
git lfs track "*.pt"

# Commit and push
git add .gitattributes
git commit -m "Add Git LFS"
git push
```

**Note:** Git LFS has storage limits and costs.

### Option 4: Download Script

Create `download_data.py` to automate downloads.

---

## 🚀 Deployment Without Data

### Your App Can Work Without Data!

**Two Approaches:**

### Approach 1: Demo Mode (Recommended)

```python
# config.py
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
MODELS_DIR = Path(__file__).parent / "models" / "fine-tuned"

# Check if data exists
DATA_AVAILABLE = DATA_DIR.exists() and any(DATA_DIR.iterdir())
MODELS_AVAILABLE = MODELS_DIR.exists() and any(MODELS_DIR.glob("*.h5"))

# Demo mode flag
DEMO_MODE = not (DATA_AVAILABLE and MODELS_AVAILABLE)
```

```python
# In your pages
from config import DEMO_MODE, MODELS_AVAILABLE

if DEMO_MODE:
    st.warning("⚠️ Running in DEMO mode. Upload data or train models for full functionality.")
    # Show demo with sample images
else:
    # Full functionality
    model = load_model()
```

### Approach 2: User Upload Only

```python
# Let users upload their own images
uploaded_file = st.file_uploader("Upload crop image", type=['jpg', 'png'])

if uploaded_file:
    image = Image.open(uploaded_file)
    # Process image
```

**No need for 25GB dataset!** Users bring their own images.

---

## 📝 Update README.md

Add this section to your README:

```markdown
## 📦 Data Setup (Optional)

This project works in two modes:

### 1. Demo Mode (No Data Required)
- Upload your own images through the web interface
- Perfect for testing and evaluation
- No dataset download needed

### 2. Full Mode (With Datasets)
If you want to train models or use pre-trained models:

**Download Datasets:**
1. Agriculture-Vision-2021: [Link]
2. Longitudinal Nutrient Deficiency: [Link]
3. OPA Pest Detection: [Link]
4. Weed Detection: [Link]

**Extract to:**
```
data/
├── Agriculture-Vision-2021/
├── longitudinal_nutrient_deficiency/
├── OPA_Pest_DIP_AI/
└── weed_detection_dataset/
```

**Download Pre-trained Models:**
- Crop Health Model: [Google Drive Link]
- Pest Detection Model: [Google Drive Link]
- Weed Segmentation Model: [Google Drive Link]

**Extract to:**
```
models/fine-tuned/
├── crop_health_model.h5
├── pest_detection_model.pt
└── weed_segmentation_model.h5
```

### 3. Train Your Own Models
```bash
python train_crop_health_model.py
python train_pest_detection_model.py
python train_weed_segmentation_model.py
```
```

---

## 🎯 Recommended Approach

### For GitHub:

1. **Push only code** (Python files, configs, docs)
2. **Add data placeholders** (empty folders with README)
3. **Document data sources** (where to get datasets)
4. **Provide download links** (Google Drive, Kaggle, etc.)

### For Users:

**Option A: Demo Mode**
```bash
git clone https://github.com/YOUR_USERNAME/krishi-sahayak.git
cd krishi-sahayak
pip install -r requirements.txt
streamlit run app.py
# Upload images through web interface
```

**Option B: Full Setup**
```bash
git clone https://github.com/YOUR_USERNAME/krishi-sahayak.git
cd krishi-sahayak
pip install -r requirements.txt

# Download data (from provided links)
# Extract to data/ folder

# Download models (from provided links)
# Extract to models/fine-tuned/

streamlit run app.py
```

---

## 🌐 Deployment Options

### 1. Streamlit Cloud (Free)

**Limitations:**
- 1GB storage limit
- No large datasets
- No large models

**Solution:**
- Deploy in **demo mode**
- Users upload their own images
- Or use small sample models

### 2. Heroku (Free Tier)

**Limitations:**
- 500MB slug size
- No persistent storage

**Solution:**
- Demo mode only
- Download models on startup (from cloud storage)

### 3. AWS/GCP/Azure (Paid)

**No limitations:**
- Upload full datasets
- Store large models
- Full functionality

**Setup:**
```bash
# Upload data to S3/GCS
aws s3 sync data/ s3://your-bucket/data/

# Download in app
aws s3 sync s3://your-bucket/data/ data/
```

### 4. Docker Container

```dockerfile
# Dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Download data on container start
RUN python download_data.py

CMD ["streamlit", "run", "app.py"]
```

---

## 📊 File Size Breakdown

### What You're Pushing (~50MB):
```
Python code:           ~5MB
Documentation:         ~2MB
Configuration:         ~1MB
Empty folders:         ~1KB
Total:                 ~8MB ✅
```

### What You're NOT Pushing (~25GB):
```
Datasets:              ~20GB ❌
Trained models:        ~5GB ❌
Logs:                  ~100MB ❌
Cache:                 ~50MB ❌
Total:                 ~25GB (EXCLUDED)
```

---

## ✅ Verification Checklist

Before pushing to GitHub:

```bash
# 1. Check what will be committed
git status

# 2. Check file sizes
git ls-files | xargs du -h | sort -h | tail -20

# 3. Verify data is ignored
git check-ignore data/
git check-ignore models/fine-tuned/*.h5

# 4. Check total size
du -sh .git/

# Should be < 100MB
```

---

## 🎯 Summary

### ✅ DO:
- ✅ Push all Python code
- ✅ Push documentation
- ✅ Push empty folder structure
- ✅ Provide data download links
- ✅ Support demo mode (user uploads)

### ❌ DON'T:
- ❌ Push 25GB datasets
- ❌ Push large model files
- ❌ Push training logs
- ❌ Push cache files

### 🚀 Result:
- **GitHub repo:** ~10MB (fast clone)
- **Full setup:** Users download data separately
- **Demo mode:** Works without data
- **Deployment:** Flexible options

---

## 📞 For Users

When someone clones your repo:

**Quick Start (Demo Mode):**
```bash
git clone https://github.com/YOUR_USERNAME/krishi-sahayak.git
cd krishi-sahayak
pip install -r requirements.txt
streamlit run app.py
# Upload images through web interface ✅
```

**Full Setup (With Data):**
```bash
git clone https://github.com/YOUR_USERNAME/krishi-sahayak.git
cd krishi-sahayak
pip install -r requirements.txt

# Download data from provided links
# Extract to data/ and models/ folders

streamlit run app.py
# Full functionality ✅
```

---

**Your project will work perfectly without pushing 25GB to GitHub!** 🎉

The code is on GitHub, data is downloaded separately. This is the **industry standard** for ML projects.
