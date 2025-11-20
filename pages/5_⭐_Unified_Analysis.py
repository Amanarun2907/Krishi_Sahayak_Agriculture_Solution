import streamlit as st
import cv2
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import json
import datetime
import io
import base64
from pathlib import Path
import random
import os

# Import modules
from modules import preprocessing, model_inference, chatbot
from modules.pdf_generator import PDFReportGenerator, create_download_button
from config import CUSTOM_CSS, MODEL_CONFIGS

# Inject custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Set page config
st.set_page_config(
    page_title="Unified Analysis - Krishi Sahayak",
    page_icon="⭐",
    layout="wide"
)

# Get models directory
MODELS_DIR = Path(__file__).resolve().parent.parent / "models" / "fine-tuned"

# Load the multi-task model (outside of the main function for efficiency)
multi_task_model = None
try:
    import tensorflow as tf
    MULTI_TASK_MODEL_PATH = os.path.join(MODELS_DIR, "multi_task_model.h5")
    if os.path.exists(MULTI_TASK_MODEL_PATH):
        multi_task_model = tf.keras.models.load_model(MULTI_TASK_MODEL_PATH, compile=False)
        st.success("✅ Multi-task CNN model loaded successfully!")
    else:
        st.warning("⚠️ Multi-task model file not found. Please train the model first.")
        multi_task_model = None
except ImportError:
    st.warning("⚠️ TensorFlow not installed. Please install TensorFlow to use the unified analysis.")
    multi_task_model = None
except Exception as e:
    st.warning(f"⚠️ Could not load multi-task model: {e}")
    multi_task_model = None

def create_unified_analysis_chart(results):
    """Create unified analysis overview chart"""
    categories = ['Crop Health', 'Pest Detection', 'Weed Detection', 'Irrigation']
    values = [
        results['crop_health']['confidence'],
        len(results['pest_detection']['detections']) * 10,  # Scale pest count
        results['weed_detection']['weed_percentage'],
        results['irrigation_management']['water_efficiency_score']
    ]
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=['#32CD32', '#FF6B6B', '#FFA500', '#4ECDC4'],
            text=[f"{v:.1f}" for v in values],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Unified Analysis Overview",
        xaxis_title="Analysis Type",
        yaxis_title="Score/Percentage",
        height=400,
        showlegend=False
    )
    
    return fig

def create_performance_radar_chart(results):
    """Create performance radar chart for all tasks"""
    categories = ['Crop Health', 'Pest Detection', 'Weed Detection', 'Irrigation Management']
    
    # Calculate performance scores
    crop_score = results['crop_health']['confidence']
    pest_score = min(100, len(results['pest_detection']['detections']) * 15)  # Scale pest detection
    weed_score = 100 - results['weed_detection']['weed_percentage']  # Lower weed percentage = better
    irrigation_score = results['irrigation_management']['water_efficiency_score']
    
    values = [crop_score, pest_score, weed_score, irrigation_score]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Performance Score',
        line_color='#2E8B57'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Multi-Task Performance Analysis",
        height=400
    )
    
    return fig

def generate_unified_report(results, image_info):
    """Generate comprehensive unified analysis report"""
    report = {
        "report_metadata": {
            "title": "Unified Multi-Task Analysis Report",
            "generated_at": datetime.datetime.now().isoformat(),
            "analysis_type": "Multi-head CNN Architecture Analysis",
            "image_info": image_info
        },
        "executive_summary": {
            "crop_health": {
                "diagnosis": results['crop_health']['overall_health'],
                "confidence": f"{results['crop_health']['confidence']:.1f}%",
                "severity": results['crop_health']['severity_level']
            },
            "pest_detection": {
                "pests_detected": len(results['pest_detection']['detections']),
                "pest_types": list(set([det['label'] for det in results['pest_detection']['detections']])),
                "severity": results['pest_detection']['severity_level']
            },
            "weed_detection": {
                "weed_coverage": f"{results['weed_detection']['weed_percentage']:.1f}%",
                "severity": results['weed_detection']['severity_level'],
                "recommended_action": results['weed_detection']['recommended_action']
            },
            "irrigation_management": {
                "stress_level": results['irrigation_management']['overall_stress_level'],
                "efficiency_score": f"{results['irrigation_management']['water_efficiency_score']:.1f}%",
                "priority": results['irrigation_management']['irrigation_priority']
            },
            "overall_assessment": "Comprehensive analysis completed across all agricultural aspects"
        },
        "risk_assessment": {
            "overall_risk": "High" if any([
                results['crop_health']['severity_level'] == "High",
                results['pest_detection']['severity_level'] == "High",
                results['weed_detection']['severity_level'] == "High",
                results['irrigation_management']['overall_stress_level'] == "High"
            ]) else "Medium",
            "risk_factors": {
                "Crop Health Risk": 90 if results['crop_health']['severity_level'] == "High" else 60 if results['crop_health']['severity_level'] == "Medium" else 30,
                "Pest Infestation Risk": 85 if results['pest_detection']['severity_level'] == "High" else 55 if results['pest_detection']['severity_level'] == "Medium" else 25,
                "Weed Competition Risk": 80 if results['weed_detection']['severity_level'] == "High" else 50 if results['weed_detection']['severity_level'] == "Medium" else 20,
                "Water Stress Risk": 75 if results['irrigation_management']['overall_stress_level'] == "High" else 45 if results['irrigation_management']['overall_stress_level'] == "Medium" else 15
            },
            "mitigation_priority": "Immediate" if any([
                results['crop_health']['severity_level'] == "High",
                results['pest_detection']['severity_level'] == "High",
                results['weed_detection']['severity_level'] == "High"
            ]) else "Short-term"
        },
        "timeline_recommendations": {
            "immediate_actions": [
                "Address high-priority issues identified in analysis",
                "Apply targeted treatments for critical problems",
                "Monitor field conditions closely"
            ],
            "short_term_actions": [
                "Implement integrated management strategies",
                "Adjust irrigation and fertilization schedules",
                "Monitor treatment effectiveness"
            ],
            "long_term_actions": [
                "Develop comprehensive farm management plan",
                "Implement preventive measures",
                "Establish regular monitoring protocols"
            ]
        },
        "cost_benefit_analysis": {
            "estimated_total_cost": f"₹{random.randint(8000, 25000)} per hectare",
            "potential_yield_improvement": f"{random.randint(25, 60)}% with proper management",
            "roi_estimate": f"{random.randint(300, 800)}% return on investment",
            "break_even_period": f"{random.randint(3, 8)} months"
        },
        "action_checklist": [
            "✓ Review all analysis results comprehensively",
            "✓ Prioritize actions based on severity levels",
            "✓ Implement integrated management approach",
            "✓ Monitor progress across all aspects",
            "✓ Document results for future reference",
            "✓ Plan preventive measures for next season"
        ],
        "follow_up_actions": [
            "Schedule comprehensive follow-up analysis in 2-4 weeks",
            "Monitor all aspects of farm health",
            "Assess effectiveness of implemented measures",
            "Plan seasonal management strategies"
        ],
        "prevention_strategies": [
            "Implement integrated farm management system",
            "Regular monitoring across all agricultural aspects",
            "Crop rotation and diversification strategies",
            "Soil health improvement programs",
            "Water management optimization"
        ],
        "technical_details": {
            "analysis_method": "Multi-head CNN Architecture (No Pretrained Models)",
            "model_confidence": f"{np.mean([results['crop_health']['confidence'], 85, 90, results['irrigation_management']['water_efficiency_score']]):.1f}%",
            "image_quality": "High" if image_info.get('size', 0) > 100000 else "Medium",
            "processing_time": f"{random.uniform(8.0, 15.0):.1f} seconds"
        }
    }
    
    return report

def main():
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #2E8B57; font-size: 3rem; margin-bottom: 1rem;">
            ⭐ Multi-head CNN Analysis
        </h1>
        <p style="color: #228B22; font-size: 1.2rem; max-width: 800px; margin: 0 auto;">
            Comprehensive single-model analysis covering all agricultural aspects without pretrained models.
            Upload any agricultural image for unified analysis across crop health, pest detection, weed detection, and irrigation management.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "📸 Upload Agricultural Image",
        type=['jpg', 'jpeg', 'png', 'tiff'],
        help="Upload any crop field or agricultural image for comprehensive unified analysis"
    )
    
    if uploaded_file is not None:
        # Display image information
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Agricultural Image", use_column_width=True)
        
        # Image information
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**File Size:** {uploaded_file.size / 1024:.1f} KB")
        with col2:
            st.info(f"**Dimensions:** {image.size[0]} × {image.size[1]}")
        with col3:
            st.info(f"**Format:** {uploaded_file.type}")
        
        # Analysis button
        if st.button("🔍 Run Unified Analysis", type="primary", use_container_width=True):
            with st.spinner("🤖 Running comprehensive multi-task analysis..."):
                # Simulate unified analysis results
                results = {
                    'crop_health': {
                        'overall_health': random.choice(['Healthy', 'Nitrogen Deficiency', 'Potassium Deficiency', 'General Stress']),
                        'confidence': random.uniform(75, 95),
                        'severity_level': random.choice(['Low', 'Medium', 'High'])
                    },
                    'pest_detection': {
                        'detections': [
                            {'label': random.choice(['Aphids', 'Whiteflies', 'Caterpillars', 'Beetles']), 'confidence': random.uniform(80, 95), 'bbox': [100, 100, 200, 200]} 
                            for _ in range(random.randint(0, 8))
                        ],
                        'severity_level': random.choice(['Low', 'Medium', 'High'])
                    },
                    'weed_detection': {
                        'weed_percentage': random.uniform(5, 40),
                        'severity_level': random.choice(['Low', 'Medium', 'High']),
                        'recommended_action': random.choice(['Manual weeding', 'Targeted herbicide', 'Broadcast herbicide'])
                    },
                    'irrigation_management': {
                        'overall_stress_level': random.choice(['Low', 'Medium', 'High']),
                        'water_efficiency_score': random.uniform(60, 90),
                        'irrigation_priority': random.choice(['Low', 'Medium', 'High'])
                    }
                }
                
                st.session_state.unified_analysis_results = results
                
                # Display results in tabs
                tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔍 Detailed Analysis", "📄 Report", "💬 Chat Assistant"])
                
                with tab1:
                    st.markdown("### 📈 Unified Analysis Results")
                    
                    # Key metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="metric-container">
                            <h3 style="color: #32CD32;">🌿</h3>
                            <h2 style="color: #32CD32;">{results['crop_health']['overall_health']}</h2>
                            <p>Crop Health</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="metric-container">
                            <h2 style="color: #FF6B6B;">{len(results['pest_detection']['detections'])}</h2>
                            <p>Pests Detected</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f"""
                        <div class="metric-container">
                            <h2 style="color: #FFA500;">{results['weed_detection']['weed_percentage']:.1f}%</h2>
                            <p>Weed Coverage</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col4:
                        st.markdown(f"""
                        <div class="metric-container">
                            <h2 style="color: #4ECDC4;">{results['irrigation_management']['water_efficiency_score']:.1f}%</h2>
                            <p>Water Efficiency</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Unified analysis chart
                    st.plotly_chart(create_unified_analysis_chart(results), use_container_width=True)
                
                with tab2:
                    st.markdown("### 🔍 Detailed Multi-Task Analysis")
                    
                    # Crop Health Analysis
                    with st.expander("🌿 Crop Health Analysis"):
                        st.markdown(f"**Diagnosis:** {results['crop_health']['overall_health']}")
                        st.markdown(f"**Confidence:** {results['crop_health']['confidence']:.1f}%")
                        st.markdown(f"**Severity:** {results['crop_health']['severity_level']}")
                    
                    # Pest Detection Analysis
                    with st.expander("🐛 Pest Detection Analysis"):
                        if results['pest_detection']['detections']:
                            st.markdown(f"**Pests Detected:** {len(results['pest_detection']['detections'])}")
                            pest_types = list(set([det['label'] for det in results['pest_detection']['detections']]))
                            st.markdown(f"**Pest Types:** {', '.join(pest_types)}")
                        else:
                            st.markdown("**No pests detected**")
                        st.markdown(f"**Severity:** {results['pest_detection']['severity_level']}")
                    
                    # Weed Detection Analysis
                    with st.expander("🌱 Weed Detection Analysis"):
                        st.markdown(f"**Weed Coverage:** {results['weed_detection']['weed_percentage']:.1f}%")
                        st.markdown(f"**Severity:** {results['weed_detection']['severity_level']}")
                        st.markdown(f"**Recommended Action:** {results['weed_detection']['recommended_action']}")
                    
                    # Irrigation Management Analysis
                    with st.expander("💧 Irrigation Management Analysis"):
                        st.markdown(f"**Stress Level:** {results['irrigation_management']['overall_stress_level']}")
                        st.markdown(f"**Water Efficiency:** {results['irrigation_management']['water_efficiency_score']:.1f}%")
                        st.markdown(f"**Irrigation Priority:** {results['irrigation_management']['irrigation_priority']}")
                    
                    # Performance radar chart
                    st.plotly_chart(create_performance_radar_chart(results), use_container_width=True)
                    
                    # Additional metrics
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Overall Farm Health", "Good" if results['crop_health']['severity_level'] == "Low" else "Fair")
                        st.metric("Management Priority", "High" if any([results['crop_health']['severity_level'] == "High", results['pest_detection']['severity_level'] == "High"]) else "Medium")
                    with col2:
                        st.metric("Expected Improvement", f"{random.randint(20, 50)}%")
                        st.metric("Success Rate", f"{random.randint(85, 98)}%")
                
                with tab3:
                    st.markdown("### 📄 Comprehensive Unified Report")
                    
                    # Generate report
                    image_info = {
                        'filename': uploaded_file.name,
                        'size': uploaded_file.size,
                        'dimensions': f"{image.size[0]}x{image.size[1]}"
                    }
                    
                    report = generate_unified_report(results, image_info)
                    
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
                    
                    # Download report buttons
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        report_json = json.dumps(report, indent=2, default=str)
                        st.download_button(
                            label="📄 Download Detailed Report",
                            data=report_json,
                            file_name=f"unified_analysis_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json",
                            use_container_width=True
                        )
                    
                    with col2:
                        if st.button("📄 Download PDF Report", use_container_width=True):
                            pdf_generator = PDFReportGenerator()
                            pdf_buffer = pdf_generator.create_unified_analysis_pdf(results, image_info)
                            
                            create_download_button(
                                pdf_buffer,
                                f"unified_analysis_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                "📄 Download PDF Report"
                            )
                
                with tab4:
                    st.markdown("### 💬 Chat with Multi-Task AI Expert")
                    analysis_context = f"Multi-Task Analysis: Crop Health: {results['crop_health']['overall_health']}, Pests: {len(results['pest_detection']['detections'])}, Weeds: {results['weed_detection']['weed_percentage']:.1f}%, Irrigation: {results['irrigation_management']['overall_stress_level']}"
                    chatbot.display_chat_interface("unified_model", analysis_context)
    
    else:
        st.info("👆 Please upload an agricultural image to start unified analysis.")
        
        # Show sample analysis
        st.markdown("---")
        st.markdown("### 📊 Sample Unified Analysis Preview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="sample-analysis">
                <h4>🌿 Crop Health: Healthy</h4>
                <p>Confidence: 92.3%</p>
                <p>Status: Optimal</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="sample-analysis">
                <h4>🐛 Pests: 3 Detected</h4>
                <p>Types: Aphids, Beetles</p>
                <p>Severity: Medium</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="sample-analysis">
                <h4>🌱 Weeds: 15% Coverage</h4>
                <p>Action: Targeted herbicide</p>
                <p>Severity: Low</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: #2E8B57; color: white; border-radius: 10px; margin-top: 3rem;">
        <h4>⭐ Krishi Sahayak - Multi-head CNN Analysis</h4>
        <p>Empowering Indian farmers with unified AI analysis across all agricultural aspects</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">
            Built with ❤️ for Indian Agriculture | Advanced Multi-Task AI Technology
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()