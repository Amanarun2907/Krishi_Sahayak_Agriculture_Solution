# 🚀 Quick Start Guide - Krishi Sahayak

## ⚡ 5-Minute Setup

### For First-Time Users:

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/krishi-sahayak.git
cd krishi-sahayak

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
copy .env.example .env     # Windows
cp .env.example .env       # Linux/Mac

# 4. Add your API key to .env
# Edit .env and replace 'your_groq_api_key_here' with your actual key
# Get key from: https://console.groq.com/keys

# 5. Run the app
streamlit run app.py
```

---

## 🔑 Get Your API Key

1. Visit: https://console.groq.com/keys
2. Sign up or login
3. Click "Create API Key"
4. Copy the key
5. Paste into `.env` file

---

## 📁 Your .env File Should Look Like:

```
GROQ_API_KEY=gsk_your_actual_key_here_56_characters_long
```

---

## ✅ Verify Setup

```bash
python -c "from config import GROQ_API_KEY; print('✅ Ready!' if GROQ_API_KEY else '❌ Add API key to .env')"
```

---

## 🎯 Features

- 🌿 Crop Health Monitoring
- 🐛 Pest Detection (18+ types)
- 🌱 Weed Segmentation
- 💧 Irrigation Management
- ⭐ Multi-Task Analysis
- 🤖 AI Chatbot (6 specialists)
- 📊 Performance Analytics
- 🔍 Explainable AI (XAI)
- ⚛️ Physics-Informed AI (PINN)

---

## 🆘 Troubleshooting

**Problem:** "API Key missing" error
**Solution:** Check if `.env` file exists and contains your API key

**Problem:** "Module not found"
**Solution:** Run `pip install -r requirements.txt`

**Problem:** Models not loading
**Solution:** Train models using training scripts in project root

---

## 📚 Full Documentation

- `SETUP_GUIDE.md` - Detailed setup instructions
- `GITHUB_SECURITY_CHECKLIST.md` - Security best practices
- `API_KEY_SECURITY_COMPLETE.md` - API key configuration

---

**Built with ❤️ for Indian Farmers | Jai Jawan, Jai Kisan! 🌾**
