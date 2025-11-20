# 🔍 Explainable AI - Demo Mode Implementation

## Issues Fixed

### 1. Missing Dependencies
**Problem:** `cv2` (OpenCV) and `reportlab` modules were missing from requirements.txt

**Solution:**
- Changed `opencv-python` to `opencv-python-headless` (better for server environments)
- Added `reportlab>=4.0.0` for PDF generation

### 2. Model Files Not Available on Streamlit Cloud
**Problem:** Model files (`.h5`, `.pt`, `.pth`) are too large for GitHub (100+ MB each) and are excluded via `.gitignore`

**Solution:** Implemented intelligent fallback system:
- ✅ Checks if model exists locally
- ✅ Loads model with `compile=False` to avoid custom object issues
- ✅ Falls back to demo mode when models unavailable
- ✅ Provides clear user feedback about model status

### 3. Grad-CAM Error Handling
**Problem:** Error message "Crop Health model not found" was confusing and didn't explain why

**Solution:**
- Better error messages explaining model files are not on Streamlit Cloud
- Instructions for users on how to use real models (cloud storage, Git LFS)
- Graceful degradation to demo mode

## Demo Mode Features

### What Works in Demo Mode:
1. **Realistic Heatmap Generation**
   - Uses edge detection (Canny) to identify important regions
   - Applies Gaussian blur for smooth attention maps
   - Adds randomness to simulate neural network attention
   - Creates visually accurate Grad-CAM-style visualizations

2. **Simulated Predictions**
   - Random class selection from actual class names
   - Realistic confidence scores (75-95%)
   - Clear labeling as "Demo" to avoid confusion

3. **Region Importance Analysis**
   - Generates 5 demo regions with bounding boxes
   - Importance scores and visualizations
   - Interactive Plotly charts

4. **Educational Value**
   - Shows how Grad-CAM works conceptually
   - Demonstrates attention mechanism visualization
   - Perfect for presentations and learning

### What Requires Real Models:
- Actual AI predictions based on learned features
- True gradient-based attention maps
- Model-specific layer activations
- Accurate confidence scores

## File Changes

### 1. `requirements.txt`
```diff
- opencv-python>=4.8.0
+ opencv-python-headless>=4.8.0
+ reportlab>=4.0.0
```

### 2. `pages/8_🔍_Explainable_AI.py`
- Added `model_available` flag for state tracking
- Improved model loading with `compile=False`
- Enhanced error messages with explanations
- Implemented realistic demo heatmap generation using edge detection
- Added demo region importance analysis
- Clear labeling of demo vs real results

### 3. `models/fine-tuned/README.md`
- Updated to mention Explainable AI demo mode
- Added information about demo features

## Usage

### On Streamlit Cloud (Demo Mode):
1. Navigate to "🔍 Explainable AI" page
2. Upload a crop image
3. Click "🚀 Generate Grad-CAM"
4. See demo visualization with educational explanations
5. Understand how Grad-CAM works conceptually

### With Local Models:
1. Download or train models (see `models/fine-tuned/README.md`)
2. Place models in `models/fine-tuned/` directory
3. Run locally: `streamlit run app.py`
4. Get real AI-powered Grad-CAM visualizations

## Technical Details

### Demo Heatmap Algorithm:
```python
# 1. Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# 2. Detect edges (important features)
edges = cv2.Canny(gray, 50, 150)

# 3. Blur to create attention-like map
heatmap = cv2.GaussianBlur(edges / 255.0, (21, 21), 0)

# 4. Add randomness to simulate neural attention
heatmap = heatmap * 0.7 + random * 0.3

# 5. Normalize to [0, 1]
heatmap = (heatmap - min) / (max - min)
```

This creates realistic-looking attention maps that:
- Focus on edges and textures (like CNNs do)
- Have smooth gradients (like Grad-CAM)
- Show varied attention patterns (like real models)

## Benefits

### For Users:
- ✅ App works on Streamlit Cloud without model files
- ✅ Can learn about XAI concepts without training models
- ✅ Clear feedback about what's demo vs real
- ✅ No confusing error messages

### For Developers:
- ✅ Graceful degradation pattern
- ✅ Easy to extend to other XAI methods
- ✅ Clean separation of demo vs production code
- ✅ Educational value for presentations

### For Deployment:
- ✅ Smaller repository size (no large model files)
- ✅ Faster deployment to Streamlit Cloud
- ✅ No Git LFS required
- ✅ Works out of the box

## Future Enhancements

1. **Model Download at Runtime**
   ```python
   @st.cache_resource
   def download_model():
       # Download from Google Drive/S3
       # Cache for reuse
   ```

2. **Multiple Model Support**
   - Allow users to select different model architectures
   - Compare Grad-CAM across models

3. **Interactive Heatmap Adjustment**
   - Let users adjust threshold
   - Toggle different layers
   - Compare multiple classes

4. **Export Functionality**
   - Save heatmaps as images
   - Generate PDF reports
   - Export region coordinates

## Conclusion

The Explainable AI page now works seamlessly in both demo and production modes:
- **Demo Mode:** Educational, works everywhere, no setup required
- **Production Mode:** Real predictions, accurate attention maps, requires model files

This implementation provides the best of both worlds: accessibility for learning and power for real-world use.

---

**Status:** ✅ Complete and deployed
**Last Updated:** November 20, 2025


## Update: LIME Section Fixed

### Additional Issue Resolved:

**LIME "model not found" error** - Implemented similar fallback system as Grad-CAM:
- Checks for both model availability and LIME library installation
- Provides clear feedback about what's missing
- Falls back to demo mode with superpixel segmentation
- Shows educational visualization of how LIME works

### LIME Demo Features:

1. **Superpixel Segmentation**
   - Uses SLIC algorithm to divide image into regions
   - Shows segmentation boundaries
   - 50 superpixels by default

2. **Importance Scoring**
   - Random scores for demonstration
   - Positive (green) and negative (red) contributions
   - Top 10 most important superpixels displayed

3. **Visualizations**
   - Original image
   - Superpixel segmentation with boundaries
   - Importance heatmap
   - Interactive bar chart of contributions

4. **Educational Value**
   - Shows how LIME divides images
   - Demonstrates superpixel-based explanations
   - Explains positive vs negative contributions

### Code Pattern:

Both Grad-CAM and LIME now follow the same pattern:
```python
model_available = False
lime_available = False

# Check dependencies
try:
    from lime import lime_image
    lime_available = True
except ImportError:
    lime_available = False

# Check model
if model_path.exists() and lime_available:
    # Real analysis
    model_available = True
else:
    # Demo mode
    model_available = False

# Demo visualization
if not model_available or not lime_available:
    # Show educational demo
```

This ensures consistent user experience across all XAI methods.

---

**All XAI sections now work in demo mode on Streamlit Cloud!**
