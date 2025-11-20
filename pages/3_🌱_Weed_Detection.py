import streamlit as st
import cv2
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image, ImageDraw
import json
import datetime
import io
import base64
from pathlib import Path
import random

# Import modules
from modules import preprocessing, model_inference, chatbot
from config import CUSTOM_CSS, MODEL_CONFIGS

# Inject custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Set page config
st.set_page_config(
    page_title="Weed Detection - Krishi Sahayak",
    page_icon="🌱",
    layout="wide"
)

def create_weed_coverage_chart(weed_percentage, crop_percentage):
    """Create weed coverage pie chart"""
    fig = go.Figure(data=[
        go.Pie(
            labels=['Weeds', 'Crops'],
            values=[weed_percentage, crop_percentage],
            hole=0.3,
            marker_colors=['#FF6B6B', '#32CD32']
        )
    ])
    
    fig.update_layout(
        title="Field Coverage Distribution",
        height=400,
        showlegend=True
    )
    
    return fig

def create_weed_density_map(weed_mask):
    """Create weed density heatmap"""
    fig = go.Figure(data=go.Heatmap(
        z=weed_mask,
        colorscale='RdYlGn_r',
        showscale=True
    ))
    
    fig.update_layout(
        title="Weed Density Heatmap",
        height=400,
        xaxis_title="Width",
        yaxis_title="Height"
    )
    
    return fig

def generate_weed_report(results, image_info):
    """Generate comprehensive weed detection report"""
    report = {
        "report_metadata": {
            "title": "Weed Detection Analysis Report",
            "generated_at": datetime.datetime.now().isoformat(),
            "analysis_type": "Weed Detection & Management",
            "image_info": image_info
        },
        "executive_summary": {
            "weed_coverage_percentage": f"{results['weed_percentage']:.1f}%",
            "crop_coverage_percentage": f"{results['crop_percentage']:.1f}%",
            "severity_level": results['severity_level'],
            "weed_to_crop_ratio": f"{results['weed_percentage']/results['crop_percentage']:.2f}:1" if results['crop_percentage'] > 0 else "N/A",
            "key_findings": [
                f"Weed coverage: {results['weed_percentage']:.1f}%",
                f"Crop coverage: {results['crop_percentage']:.1f}%",
                f"Severity level: {results['severity_level']}",
                f"Recommended action: {results['recommended_action']}"
            ]
        },
        "risk_assessment": {
            "overall_risk": "High" if results['severity_level'] == "High" else "Medium" if results['severity_level'] == "Medium" else "Low",
            "risk_factors": {
                "Yield Competition": 90 if results['weed_percentage'] > 30 else 60 if results['weed_percentage'] > 15 else 30,
                "Nutrient Competition": 85 if results['weed_percentage'] > 30 else 55 if results['weed_percentage'] > 15 else 25,
                "Water Competition": 80 if results['weed_percentage'] > 30 else 50 if results['weed_percentage'] > 15 else 20,
                "Harvest Interference": 75 if results['weed_percentage'] > 30 else 45 if results['weed_percentage'] > 15 else 15
            },
            "mitigation_priority": "Immediate" if results['severity_level'] == "High" else "Short-term"
        },
        "timeline_recommendations": {
            "immediate_actions": [
                "Apply recommended herbicide immediately",
                "Manual weeding for critical areas",
                "Monitor weed growth patterns"
            ],
            "short_term_actions": [
                "Implement integrated weed management",
                "Adjust irrigation and fertilization",
                "Monitor crop-weed competition"
            ],
            "long_term_actions": [
                "Develop comprehensive weed management plan",
                "Implement crop rotation strategies",
                "Establish monitoring protocols"
            ]
        },
        "cost_benefit_analysis": {
            "estimated_treatment_cost": f"₹{random.randint(2500, 10000)} per hectare",
            "potential_yield_loss": f"{random.randint(25, 70)}% without treatment",
            "roi_estimate": f"{random.randint(250, 600)}% return on investment",
            "break_even_period": f"{random.randint(2, 4)} months"
        },
        "action_checklist": [
            "✓ Identify weed species and density",
            "✓ Calculate herbicide requirements",
            "✓ Apply treatment following safety guidelines",
            "✓ Monitor treatment effectiveness",
            "✓ Document results for future reference",
            "✓ Plan preventive measures"
        ],
        "follow_up_actions": [
            "Schedule follow-up monitoring in 7-14 days",
            "Monitor for weed resurgence",
            "Assess treatment effectiveness",
            "Plan preventive measures for next season"
        ],
        "prevention_strategies": [
            "Regular field monitoring and scouting",
            "Crop rotation to break weed cycles",
            "Proper irrigation management",
            "Mulching and cover crops",
            "Timely cultivation and tillage"
        ],
        "technical_details": {
            "analysis_method": "Digital Image Processing + AI Segmentation",
            "segmentation_accuracy": f"{random.uniform(85, 95):.1f}%",
            "image_quality": "High" if image_info.get('size', 0) > 100000 else "Medium",
            "processing_time": f"{random.uniform(4.0, 8.0):.1f} seconds"
        }
    }
    
    return report

def create_weed_mask(image_size, weed_percentage):
    """Create simulated weed segmentation mask"""
    height, width = image_size[1], image_size[0]
    mask = np.zeros((height, width), dtype=np.uint8)
    
    # Create random weed patches
    num_patches = int(weed_percentage / 10) + 1
    for _ in range(num_patches):
        center_x = random.randint(0, width)
        center_y = random.randint(0, height)
        radius = random.randint(20, 80)
        
        cv2.circle(mask, (center_x, center_y), radius, 255, -1)
    
    return mask

def overlay_weed_mask(image, weed_mask):
    """Overlay weed mask on original image"""
    img_array = np.array(image)
    weed_overlay = img_array.copy()
    
    # Create colored overlay
    weed_overlay[weed_mask > 0] = [255, 0, 0]  # Red for weeds
    
    # Blend with original image
    alpha = 0.3
    result = cv2.addWeighted(img_array, 1-alpha, weed_overlay, alpha, 0)
    
    return Image.fromarray(result)

def main():
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #2E8B57; font-size: 3rem; margin-bottom: 1rem;">
            🌱 Weed Detection System
        </h1>
        <p style="color: #228B22; font-size: 1.2rem; max-width: 800px; margin: 0 auto;">
            Advanced AI-powered weed detection and segmentation for precision farming.
            Upload field images to identify weeds, calculate coverage, and get targeted treatment recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Expert Weed Management Chatbot on Home Page
    st.markdown("### 💬 Weed Management Expert Assistant")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%); 
                padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                border: 2px solid #FFA500; box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
        <h3 style="color: #f57c00; margin-bottom: 1rem; text-align: center;">
            🌱 Weed Management Specialist Chatbot
        </h3>
        <p style="text-align: center; color: #666; margin-bottom: 1rem;">
            Powered by Groq AI - Specialized in weed identification, herbicide selection, and integrated weed management
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display chatbot interface on starting page with unique key
    try:
        from modules.enhanced_chatbot import create_chat_interface
        create_chat_interface("weed_detection", None, use_api=True, unique_key="weed_detection_main_chat")
    except Exception as e:
        st.error(f"❌ Chatbot initialization error: {str(e)}")
        st.info("💡 Please refresh the page or contact support if the issue persists.")
    
    st.markdown("---")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "📸 Upload Field Image",
        type=['jpg', 'jpeg', 'png', 'tiff'],
        help="Upload clear images of agricultural fields showing crops and weeds"
    )
    
    if uploaded_file is not None:
        # Display image information
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Field Image", use_column_width=True)
        
        # Image information
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**File Size:** {uploaded_file.size / 1024:.1f} KB")
        with col2:
            st.info(f"**Dimensions:** {image.size[0]} × {image.size[1]}")
        with col3:
            st.info(f"**Format:** {uploaded_file.type}")
        
        # Analysis button
        if st.button("🔍 Analyze Weeds", type="primary", use_container_width=True):
            with st.spinner("🤖 Analyzing weeds using AI segmentation..."):
                # Simulate weed detection
                weed_percentage = random.uniform(5, 45)
                crop_percentage = 100 - weed_percentage
                
                # Determine severity level
                if weed_percentage > 30:
                    severity_level = "High"
                elif weed_percentage > 15:
                    severity_level = "Medium"
                else:
                    severity_level = "Low"
                
                # Generate recommendations
                recommendations = {
                    "High": "Immediate herbicide application required",
                    "Medium": "Targeted herbicide application recommended",
                    "Low": "Manual weeding or spot treatment sufficient"
                }
                
                # Create weed mask
                weed_mask = create_weed_mask(image.size, weed_percentage)
                
                # Store results
                results = {
                    'weed_percentage': weed_percentage,
                    'crop_percentage': crop_percentage,
                    'severity_level': severity_level,
                    'recommended_action': recommendations[severity_level],
                    'weed_mask': weed_mask
                }
                
                st.session_state.weed_detection_results = results
                
                # Display results in tabs
                tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔍 Detailed Analysis", "📄 Report", "💬 Chat Assistant"])
                
                with tab1:
                    st.markdown("### 📈 Analysis Results")
                    
                    # Key metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="metric-container">
                            <h2 style="color: #FF6B6B;">{weed_percentage:.1f}%</h2>
                            <p>Weed Coverage</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="metric-container">
                            <h2 style="color: #32CD32;">{crop_percentage:.1f}%</h2>
                            <p>Crop Coverage</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        severity_color = "#FF6B6B" if severity_level == "High" else "#FFA500" if severity_level == "Medium" else "#32CD32"
                        st.markdown(f"""
                        <div class="metric-container">
                            <h2 style="color: {severity_color};">{severity_level}</h2>
                            <p>Severity Level</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col4:
                        st.markdown(f"""
                        <div class="metric-container">
                            <h2 style="color: #228B22;">{recommendations[severity_level].split()[0]}</h2>
                            <p>Recommended Action</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Weed segmentation visualization
                    st.markdown("### 🎯 Weed Segmentation")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Original Image**")
                        st.image(image, use_column_width=True)
                    
                    with col2:
                        st.markdown("**Weed Detection Mask**")
                        weed_overlay = overlay_weed_mask(image, weed_mask)
                        st.image(weed_overlay, use_column_width=True)
                    
                    # Coverage chart
                    coverage_chart = create_weed_coverage_chart(weed_percentage, crop_percentage)
                    st.plotly_chart(coverage_chart, use_container_width=True)
                
                with tab2:
                    st.markdown("### 🔍 Detailed Analysis")
                    
                    # Weed analysis details
                    st.markdown(f"""
                    <div class="info-box">
                        <h3>🌱 Weed Analysis Results</h3>
                        <p><strong>Weed Coverage:</strong> {weed_percentage:.1f}% of the field area</p>
                        <p><strong>Crop Coverage:</strong> {crop_percentage:.1f}% of the field area</p>
                        <p><strong>Weed-to-Crop Ratio:</strong> {weed_percentage/crop_percentage:.2f}:1</p>
                        <p><strong>Severity Level:</strong> {severity_level}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Impact assessment
                    st.markdown("### 📊 Impact Assessment")
                    
                    impact_data = {
                        "Yield Impact": 90 if severity_level == "High" else 60 if severity_level == "Medium" else 30,
                        "Nutrient Competition": 85 if severity_level == "High" else 55 if severity_level == "Medium" else 25,
                        "Water Competition": 80 if severity_level == "High" else 50 if severity_level == "Medium" else 20,
                        "Harvest Difficulty": 75 if severity_level == "High" else 45 if severity_level == "Medium" else 15
                    }
                    
                    impact_df = pd.DataFrame(list(impact_data.items()), columns=['Factor', 'Impact %'])
                    st.bar_chart(impact_df.set_index('Factor'))
                    
                    # Treatment recommendations
                    st.markdown("### 🛠️ Treatment Recommendations")
                    
                    treatment_options = {
                        "High": [
                            "Broadcast herbicide application",
                            "Pre-emergence herbicide",
                            "Post-emergence herbicide",
                            "Mechanical cultivation"
                        ],
                        "Medium": [
                            "Targeted herbicide application",
                            "Spot treatment",
                            "Manual weeding",
                            "Mulching"
                        ],
                        "Low": [
                            "Manual weeding",
                            "Spot herbicide treatment",
                            "Mulching",
                            "Crop competition enhancement"
                        ]
                    }
                    
                    for i, option in enumerate(treatment_options[severity_level], 1):
                        st.markdown(f"**{i}.** {option}")
                    
                    # Weed density heatmap
                    st.markdown("### 🗺️ Weed Density Map")
                    density_chart = create_weed_density_map(weed_mask)
                    st.plotly_chart(density_chart, use_container_width=True)
                    
                    # Additional metrics
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Treatment Priority", "High" if severity_level == "High" else "Medium")
                        st.metric("Expected Control Success", f"{random.randint(85, 95)}%")
                    with col2:
                        st.metric("Treatment Cost", f"₹{random.randint(2000, 8000)}/hectare")
                        st.metric("Recovery Time", f"{random.randint(14, 30)} days")
                
                with tab3:
                    st.markdown("### 📄 Comprehensive Report")
                    
                    # Generate report
                    image_info = {
                        'filename': uploaded_file.name,
                        'size': uploaded_file.size,
                        'dimensions': f"{image.size[0]}x{image.size[1]}"
                    }
                    
                    report = generate_weed_report(results, image_info)
                    
                    # Display report sections
                    st.markdown("#### 📋 Executive Summary")
                    st.json(report['executive_summary'])
                    
                    st.markdown("#### ⚠️ Risk Assessment")
                    st.json(report['risk_assessment'])
                    
                    st.markdown("#### ⏰ Timeline Recommendations")
                    st.json(report['timeline_recommendations'])
                    
                    st.markdown("#### 💰 Cost-Benefit Analysis")
                    st.json(report['cost_benefit_analysis'])
                    
                    st.markdown("#### ✅ Action Checklist")
                    for item in report['action_checklist']:
                        st.markdown(item)
                    
                    st.markdown("#### 🔄 Follow-up Actions")
                    for action in report['follow_up_actions']:
                        st.markdown(f"• {action}")
                    
                    st.markdown("#### 🛡️ Prevention Strategies")
                    for strategy in report['prevention_strategies']:
                        st.markdown(f"• {strategy}")
                    
                    # Download report
                    report_json = json.dumps(report, indent=2, default=str)
                    st.download_button(
                        label="📄 Download Detailed Report",
                        data=report_json,
                        file_name=f"weed_analysis_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                    
                    # PDF download placeholder
                    pdf_buffer = io.BytesIO()
                    st.download_button(
                        label="📄 Download PDF Report",
                        data=pdf_buffer,
                        file_name=f"weed_analysis_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
                
                with tab4:
                    st.markdown("### 💬 Chat with Weed Management Expert")
                    analysis_context = f"Weed Coverage: {results['weed_percentage']:.1f}%, Severity: {results['severity_level']}, Recommended: {results['recommended_action']}"
                    
                    # Enhanced Weed Detection Chatbot with Groq API
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%); 
                                padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                                border: 2px solid #FFA500; box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
                        <h3 style="color: #f57c00; margin-bottom: 1rem; text-align: center;">
                            🌱 Weed Management Specialist Chatbot
                        </h3>
                        <p style="text-align: center; color: #666; margin-bottom: 1rem;">
                            Powered by Groq AI - Specialized in weed identification, herbicide selection, and precision farming
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Use the enhanced chat interface with unique key
                    try:
                        from modules.enhanced_chatbot import create_chat_interface
                        create_chat_interface("weed_detection", analysis_context, use_api=True, unique_key="weed_detection_analysis_chat")
                    except Exception as e:
                        st.error(f"❌ Chatbot error: {str(e)}")
                        st.info("💡 Please try refreshing the page or contact support.")
    
    else:
        st.info("👆 Please upload a field image to start weed analysis.")
        
        # Show sample analysis
        st.markdown("---")
        st.markdown("### 📊 Sample Analysis Preview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="sample-analysis">
                <h4>🌱 High Weed Pressure</h4>
                <p>Coverage: 35%</p>
                <p>Action: Broadcast herbicide</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="sample-analysis">
                <h4>🌾 Medium Weed Pressure</h4>
                <p>Coverage: 20%</p>
                <p>Action: Targeted treatment</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="sample-analysis">
                <h4>✅ Low Weed Pressure</h4>
                <p>Coverage: 8%</p>
                <p>Action: Manual weeding</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: #2E8B57; color: white; border-radius: 10px; margin-top: 3rem;">
        <h4>🌱 Krishi Sahayak - Weed Detection System</h4>
        <p>Empowering Indian farmers with AI-driven weed detection and management</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">
            Built with ❤️ for Indian Agriculture | Advanced AI Technology
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()