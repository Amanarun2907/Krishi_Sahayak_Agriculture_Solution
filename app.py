import streamlit as st
import os
from pathlib import Path
import base64
from PIL import Image
import numpy as np

# Import configuration
from config import PROJECT_NAME, PAGES, CUSTOM_CSS

# Set page config
st.set_page_config(
    page_title="Krishi Sahayak - AI-Powered Agriculture Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def get_base64_of_bin_file(png_file):
    """
    Convert image to base64 for embedding in HTML
    """
    with open(png_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def add_bg_from_local(image_file):
    """
    Add background image from local file
    """
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    # Main title and hero section
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #2E8B57; font-size: 4rem; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            🌾 Krishi Sahayak
        </h1>
        <h2 style="color: #228B22; font-size: 1.8rem; margin-bottom: 2rem; font-weight: 300;">
            AI-Powered Agriculture Assistant for Indian Farmers
        </h2>
        <p style="color: #006400; font-size: 1.2rem; max-width: 800px; margin: 0 auto 3rem auto; line-height: 1.6;">
            Empowering Indian farmers with cutting-edge AI technology for crop health monitoring, 
            pest detection, weed management, and irrigation optimization. 
            <strong>Jai Jawan, Jai Kisan!</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Features showcase
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 3rem; border-radius: 15px; margin: 2rem 0;">
        <h2 style="text-align: center; color: #2E8B57; margin-bottom: 2rem;">🚀 Key Features</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
    """, unsafe_allow_html=True)

    features = [
        {
            "icon": "🌿",
            "title": "Crop Health & Monitoring",
            "description": "Advanced AI-powered analysis of crop health with detailed nutrient deficiency detection and confidence scoring."
        },
        {
            "icon": "🐛",
            "title": "Pest Detection",
            "description": "Real-time pest identification with bounding box visualization and integrated pest management strategies."
        },
        {
            "icon": "🌱",
            "title": "Weed Detection",
            "description": "Pixel-level weed segmentation for precision farming and targeted herbicide application."
        },
        {
            "icon": "💧",
            "title": "Irrigation Management",
            "description": "NDVI-based water stress analysis with heatmaps and smart irrigation recommendations."
        },
        {
            "icon": "⭐",
            "title": "Multi-head CNN Analysis",
            "description": "Comprehensive single-model analysis covering all agricultural aspects without pretrained models."
        },
        {
            "icon": "🤖",
            "title": "AI Chatbot Assistant",
            "description": "Intelligent chatbot providing expert agricultural advice without requiring API keys."
        },
        {
            "icon": "📊",
            "title": "Performance Analytics",
            "description": "Detailed model performance metrics with statistical analysis and visualization."
        },
        {
            "icon": "🔍",
            "title": "Explainable AI (XAI)",
            "description": "Understand AI decisions with Grad-CAM, LIME, SHAP, and counterfactual explanations."
        },
        {
            "icon": "⚛️",
            "title": "Physics-Informed AI",
            "description": "Combine agricultural physics with AI for accurate crop growth and pest predictions."
        }
    ]

    for feature in features:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">{feature['icon']}</div>
            <h3 style="color: #2E8B57; margin-bottom: 1rem;">{feature['title']}</h3>
            <p style="color: #666; line-height: 1.5;">{feature['description']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # Navigation section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 3rem; border-radius: 15px; margin: 2rem 0;">
        <h2 style="text-align: center; color: white; margin-bottom: 2rem;">🎯 Choose Your Analysis</h2>
        <p style="text-align: center; color: white; font-size: 1.1rem; margin-bottom: 2rem;">
            Select any of the following modules to get started with AI-powered agricultural analysis
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Create navigation buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🌿 Crop Health & Monitoring", use_container_width=True, key="crop_health_btn"):
            st.switch_page("pages/1_🌿_Crop_Health.py")
        
        if st.button("🐛 Pest Detection", use_container_width=True, key="pest_detection_btn"):
            st.switch_page("pages/2_🐛_Pest_Detection.py")
        
        if st.button("🌱 Weed Detection", use_container_width=True, key="weed_detection_btn"):
            st.switch_page("pages/3_🌱_Weed_Detection.py")
    
    with col2:
        if st.button("💧 Irrigation Management", use_container_width=True, key="irrigation_btn"):
            st.switch_page("pages/4_💧_Irrigation.py")
        
        if st.button("⭐ Multi-head CNN Analysis", use_container_width=True, key="unified_btn"):
            st.switch_page("pages/5_⭐_Unified_Analysis.py")
        
        if st.button("🤖 AI Chatbot Assistant", use_container_width=True, key="chatbot_btn"):
            st.switch_page("pages/6_🤖_AI_Chatbot.py")
    
    with col3:
        if st.button("📊 Performance Analytics", use_container_width=True, key="performance_btn"):
            st.switch_page("pages/7_📊_Performance_Analytics.py")
        
        if st.button("🔍 Explainable AI (XAI)", use_container_width=True, key="xai_btn"):
            st.switch_page("pages/8_🔍_Explainable_AI.py")
        
        if st.button("⚛️ Physics-Informed AI", use_container_width=True, key="pinn_btn"):
            st.switch_page("pages/9_⚛️_Physics_Informed_AI.py")

    # Statistics section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 3rem; border-radius: 15px; margin: 2rem 0;">
        <h2 style="text-align: center; color: #8B4513; margin-bottom: 2rem;">📈 Project Impact</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; text-align: center;">
            <div>
                <h3 style="color: #8B4513; font-size: 2.5rem; margin: 0;">9</h3>
                <p style="color: #8B4513; font-weight: bold;">AI Modules</p>
            </div>
            <div>
                <h3 style="color: #8B4513; font-size: 2.5rem; margin: 0;">4</h3>
                <p style="color: #8B4513; font-weight: bold;">Datasets</p>
            </div>
            <div>
                <h3 style="color: #8B4513; font-size: 2.5rem; margin: 0;">18+</h3>
                <p style="color: #8B4513; font-weight: bold;">Pest Types</p>
            </div>
            <div>
                <h3 style="color: #8B4513; font-size: 2.5rem; margin: 0;">100%</h3>
                <p style="color: #8B4513; font-weight: bold;">Indian Focus</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Technology stack
    st.markdown("""
    <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 3rem; border-radius: 15px; margin: 2rem 0;">
        <h2 style="text-align: center; color: #2E8B57; margin-bottom: 2rem;">🛠️ Technology Stack</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; text-align: center;">
            <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #2E8B57; margin: 0;">TensorFlow</h4>
            </div>
            <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #2E8B57; margin: 0;">PyTorch</h4>
            </div>
            <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #2E8B57; margin: 0;">YOLOv8</h4>
            </div>
            <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #2E8B57; margin: 0;">U-Net</h4>
            </div>
            <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #2E8B57; margin: 0;">OpenCV</h4>
            </div>
            <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #2E8B57; margin: 0;">Streamlit</h4>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: #2E8B57; color: white; border-radius: 10px; margin-top: 3rem;">
        <h3 style="margin-bottom: 1rem;">🌾 Krishi Sahayak</h3>
        <p style="margin-bottom: 1rem;">Empowering Indian Agriculture with AI Technology</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">
            Built with ❤️ for Indian Farmers | Jai Jawan, Jai Kisan!
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()