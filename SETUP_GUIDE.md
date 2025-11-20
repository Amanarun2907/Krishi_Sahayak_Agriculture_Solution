# 🚀 Krishi Sahayak - Setup Guide

## 🔒 Security First: API Key Configuration

### ⚠️ IMPORTANT: Never Commit API Keys to GitHub!

This project uses environment variables to keep API keys secure.

---

## 📋 Step-by-Step Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/krishi-sahayak.git
cd krishi-sahayak
```

---

### 2️⃣ Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Streamlit (Web interface)
- Groq (AI chatbot)
- TensorFlow (Deep learning)
- PyTorch (Neural networks)
- OpenCV (Image processing)
- And all other required packages

---

### 4️⃣ Configure API Keys (CRITICAL!)

#### Option A: Using .env File (Recommended)

1. **Copy the example file:**
   ```bash
   copy .env.example .env     # Windows
   cp .env.example .env       # Linux/Mac
   ```

2. **Edit `.env` file and add your API key:**
   ```
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

3. **Get your Groq API key:**
   - Visit: https://console.groq.com/keys
   - Sign up/Login
   - Create a new API key
   - Copy and paste it into `.env`

#### Option B: Using Environment Variables

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="your_actual_groq_api_key_here"
```

**Windows (CMD):**
```cmd
set GROQ_API_KEY=your_actual_groq_api_key_here
```

**Linux/Mac:**
```bash
export GROQ_API_KEY="your_actual_groq_api_key_here"
```

---

### 5️⃣ Verify Configuration

```bash
python -c "from config import GROQ_API_KEY; print('✅ API Key loaded!' if GROQ_API_KEY else '❌ API Key missing!')"
```

Expected output: `✅ API Key loaded!`

---

### 6️⃣ Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at: `http://localhost:8501`

---

## 📁 Project Structure

```
krishi-sahayak/
├── app.py                          # Main application
├── config.py                       # Configuration (loads .env)
├── requirements.txt                # Python dependencies
├── .env                           # YOUR API KEYS (NOT in Git)
├── .env.example                   # Template for .env
├── .gitignore                     # Excludes sensitive files
│
├── pages/                         # Streamlit pages
│   ├── 1_🌿_Crop_Health.py
│   ├── 2_🐛_Pest_Detection.py
│   ├── 3_🌱_Weed_Detection.py
│   ├── 4_💧_Irrigation.py
│   ├── 5_⭐_Unified_Analysis.py
│   ├── 6_🤖_AI_Chatbot.py
│   ├── 7_📊_Performance_Analytics.py
│   ├── 8_🔍_Explainable_AI.py
│   └── 9_⚛️_Physics_Informed_AI.py
│
├── modules/                       # Core modules
│   ├── chatbot.py
│   ├── enhanced_chatbot.py
│   ├── data_loader.py
│   ├── model_inference.py
│   ├── preprocessing.py
│   ├── visualization.py
│   ├── xai_utils.py
│   ├── pinn_models.py
│   └── pdf_generator.py
│
├── models/                        # Trained models
│   ├── fine-tuned/               # Model files (.h5, .pt)
│   └── logs/                     # Training logs
│
└── data/                         # Datasets
    ├── Agriculture-Vision-2021/
    ├── longitudinal_nutrient_deficiency/
    ├── OPA_Pest_DIP_AI/
    └── weed_detection_dataset/
```

---

## 🔒 Security Best Practices

### ✅ DO:
- ✅ Use `.env` file for API keys
- ✅ Add `.env` to `.gitignore`
- ✅ Share `.env.example` (without actual keys)
- ✅ Use environment variables in production
- ✅ Rotate API keys regularly
- ✅ Use different keys for dev/prod

### ❌ DON'T:
- ❌ Commit `.env` to Git
- ❌ Hardcode API keys in code
- ❌ Share API keys in chat/email
- ❌ Push keys to public repositories
- ❌ Use production keys in development

---

## 🐛 Troubleshooting

### Issue: "API Key missing" error

**Solution:**
1. Check if `.env` file exists
2. Verify `GROQ_API_KEY` is set in `.env`
3. Restart the application
4. Check for typos in variable name

### Issue: "Module not found" error

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Models not loading

**Solution:**
1. Check if model files exist in `models/fine-tuned/`
2. Train models using training scripts:
   ```bash
   python train_crop_health_model.py
   python train_pest_detection_model.py
   python train_weed_segmentation_model.py
   ```

### Issue: Data not found

**Solution:**
1. Download datasets and place in `data/` folder
2. Check folder structure matches expected paths
3. Update paths in `config.py` if needed

---

## 📦 Deployment

### Deploy to Streamlit Cloud

1. **Push to GitHub** (API keys are safe now!)
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Go to Streamlit Cloud:**
   - Visit: https://streamlit.io/cloud
   - Connect your GitHub repository
   - Select `app.py` as main file

3. **Add Secrets in Streamlit Cloud:**
   - Go to App Settings → Secrets
   - Add:
     ```toml
     GROQ_API_KEY = "your_actual_key_here"
     ```

4. **Deploy!**

### Deploy to Heroku

1. **Create `Procfile`:**
   ```
   web: streamlit run app.py --server.port=$PORT
   ```

2. **Set environment variables:**
   ```bash
   heroku config:set GROQ_API_KEY=your_actual_key_here
   ```

3. **Deploy:**
   ```bash
   git push heroku main
   ```

---

## 🎓 Features

### 🌿 Crop Health Monitoring
- Nutrient deficiency detection
- Confidence scoring
- Treatment recommendations

### 🐛 Pest Detection
- 18+ pest types identification
- Bounding box visualization
- IPM strategies

### 🌱 Weed Detection
- Pixel-level segmentation
- Precision farming support
- Herbicide optimization

### 💧 Irrigation Management
- NDVI-based analysis
- Water stress detection
- Smart irrigation scheduling

### ⭐ Multi-Task Analysis
- Unified CNN model
- All-in-one analysis
- Comprehensive insights

### 🤖 AI Chatbot
- Expert agricultural advice
- Context-aware responses
- Multiple specialists

### 📊 Performance Analytics
- Model metrics
- Statistical analysis
- Visualization

### 🔍 Explainable AI (XAI)
- Grad-CAM heatmaps
- LIME explanations
- SHAP values
- Counterfactuals

### ⚛️ Physics-Informed AI (PINN)
- Crop growth simulation
- Pest population dynamics
- Water transport modeling
- Nutrient uptake optimization

---

## 📞 Support

### Issues?
- Open an issue on GitHub
- Check existing issues first
- Provide error messages and logs

### Contributing?
- Fork the repository
- Create a feature branch
- Submit a pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- Indian farmers for inspiration
- Open-source community
- Agricultural research institutions
- AI/ML community

---

**Built with ❤️ for Indian Agriculture | Jai Jawan, Jai Kisan! 🌾**
