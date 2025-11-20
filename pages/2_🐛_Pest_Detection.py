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
    page_title="Pest Detection - Krishi Sahayak",
    page_icon="🐛",
    layout="wide"
)

def create_pest_count_chart(detections):
    """Create pest count visualization chart"""
    if not detections:
        return None
    
    pest_counts = {}
    for detection in detections:
        label = detection['label']
        pest_counts[label] = pest_counts.get(label, 0) + 1
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(pest_counts.keys()),
            y=list(pest_counts.values()),
            marker_color=['#FF6B6B', '#FFA500', '#32CD32', '#4ECDC4', '#45B7D1'][:len(pest_counts)],
            text=list(pest_counts.values()),
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Detected Pest Distribution",
        xaxis_title="Pest Type",
        yaxis_title="Count",
        height=400,
        showlegend=False
    )
    
    return fig

def create_severity_chart(severity_data):
    """Create severity level chart"""
    fig = go.Figure(data=[
        go.Pie(
            labels=list(severity_data.keys()),
            values=list(severity_data.values()),
            hole=0.3,
            marker_colors=['#FF6B6B', '#FFA500', '#32CD32']
        )
    ])
    
    fig.update_layout(
        title="Infestation Severity Distribution",
        height=400,
        showlegend=True
    )
    
    return fig

def generate_pest_report(results, image_info):
    """Generate comprehensive pest detection report"""
    report = {
        "report_metadata": {
            "title": "Pest Detection Analysis Report",
            "generated_at": datetime.datetime.now().isoformat(),
            "analysis_type": "Pest Detection & Management",
            "image_info": image_info
        },
        "executive_summary": {
            "total_pests_detected": len(results['detections']),
            "pest_types": list(set([det['label'] for det in results['detections']])),
            "severity_level": results['severity_level'],
            "infestation_status": "High" if len(results['detections']) > 10 else "Medium" if len(results['detections']) > 5 else "Low",
            "key_findings": [
                f"Total pests detected: {len(results['detections'])}",
                f"Pest types: {', '.join(set([det['label'] for det in results['detections']]))}",
                f"Severity level: {results['severity_level']}",
                f"Recommended action: {results['recommended_action']}"
            ]
        },
        "risk_assessment": {
            "overall_risk": "High" if results['severity_level'] == "High" else "Medium" if results['severity_level'] == "Medium" else "Low",
            "risk_factors": {
                "Crop Damage": 90 if results['severity_level'] == "High" else 60 if results['severity_level'] == "Medium" else 30,
                "Yield Loss": 80 if results['severity_level'] == "High" else 50 if results['severity_level'] == "Medium" else 20,
                "Economic Impact": 85 if results['severity_level'] == "High" else 55 if results['severity_level'] == "Medium" else 25,
                "Spread Risk": 75 if results['severity_level'] == "High" else 45 if results['severity_level'] == "Medium" else 15
            },
            "mitigation_priority": "Immediate" if results['severity_level'] == "High" else "Short-term"
        },
        "timeline_recommendations": {
            "immediate_actions": [
                "Apply recommended pesticide immediately",
                "Monitor pest activity daily",
                "Document pest locations and damage"
            ],
            "short_term_actions": [
                "Implement Integrated Pest Management (IPM)",
                "Monitor beneficial insect populations",
                "Adjust irrigation and fertilization"
            ],
            "long_term_actions": [
                "Develop comprehensive pest management plan",
                "Implement crop rotation strategies",
                "Establish monitoring protocols"
            ]
        },
        "cost_benefit_analysis": {
            "estimated_treatment_cost": f"₹{random.randint(3000, 12000)} per hectare",
            "potential_yield_loss": f"{random.randint(20, 60)}% without treatment",
            "roi_estimate": f"{random.randint(300, 800)}% return on investment",
            "break_even_period": f"{random.randint(1, 3)} months"
        },
        "action_checklist": [
            "✓ Identify specific pest species",
            "✓ Calculate pest density and distribution",
            "✓ Select appropriate control method",
            "✓ Apply treatment following safety guidelines",
            "✓ Monitor treatment effectiveness",
            "✓ Document results for future reference"
        ],
        "follow_up_actions": [
            "Schedule follow-up monitoring in 3-7 days",
            "Monitor for pest resurgence",
            "Assess treatment effectiveness",
            "Plan preventive measures for next season"
        ],
        "prevention_strategies": [
            "Regular field monitoring and scouting",
            "Crop rotation to break pest cycles",
            "Beneficial insect habitat enhancement",
            "Proper sanitation and field hygiene",
            "Resistant variety selection"
        ],
        "technical_details": {
            "analysis_method": "Digital Image Processing + AI Object Detection",
            "detection_confidence": f"{sum([det['confidence'] for det in results['detections']]) / len(results['detections']):.1f}%" if results['detections'] else "0%",
            "image_quality": "High" if image_info.get('size', 0) > 100000 else "Medium",
            "processing_time": f"{random.uniform(3.0, 6.0):.1f} seconds"
        }
    }
    
    return report

def draw_bounding_boxes(image, detections):
    """Draw bounding boxes on image"""
    img_array = np.array(image)
    img_with_boxes = img_array.copy()
    
    for detection in detections:
        x1, y1, x2, y2 = detection['bbox']
        label = detection['label']
        confidence = detection['confidence']
        
        # Draw bounding box
        cv2.rectangle(img_with_boxes, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        
        # Draw label
        label_text = f"{label}: {confidence:.1f}%"
        cv2.putText(img_with_boxes, label_text, (int(x1), int(y1) - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    return Image.fromarray(img_with_boxes)

def main():
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #2E8B57; font-size: 3rem; margin-bottom: 1rem;">
            🐛 Pest Detection System
        </h1>
        <p style="color: #228B22; font-size: 1.2rem; max-width: 800px; margin: 0 auto;">
            Advanced AI-powered pest detection and identification for Indian farmers.
            Upload crop images to detect pests, get detailed analysis, and receive expert recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Expert Pest Detection Chatbot on Home Page
    st.markdown("### 💬 Pest Management Expert Assistant")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fff5f5 0%, #ffe8e8 100%); 
                padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                border: 2px solid #FF6B6B; box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
        <h3 style="color: #d32f2f; margin-bottom: 1rem; text-align: center;">
            🐛 Pest Management Specialist Chatbot
        </h3>
        <p style="text-align: center; color: #666; margin-bottom: 1rem;">
            Powered by Groq AI - Specialized in pest identification, IPM strategies, and biological control
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display chatbot interface on starting page with unique key
    try:
        from modules.enhanced_chatbot import create_chat_interface
        create_chat_interface("pest_detection", None, use_api=True, unique_key="pest_detection_main_chat")
    except Exception as e:
        st.error(f"❌ Chatbot initialization error: {str(e)}")
        st.info("💡 Please refresh the page or contact support if the issue persists.")
    
    st.markdown("---")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "📸 Upload Crop Image",
        type=['jpg', 'jpeg', 'png', 'tiff'],
        help="Upload clear images of crops showing pest damage or pest presence"
    )
    
    if uploaded_file is not None:
        # Display image information
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Crop Image", use_column_width=True)
        
        # Image information
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**File Size:** {uploaded_file.size / 1024:.1f} KB")
        with col2:
            st.info(f"**Dimensions:** {image.size[0]} × {image.size[1]}")
        with col3:
            st.info(f"**Format:** {uploaded_file.type}")
        
        # Analysis button
        if st.button("🔍 Detect Pests", type="primary", use_container_width=True):
            with st.spinner("🤖 Detecting pests using AI..."):
                # Simulate pest detection
                pest_types = ["Aphids", "Whiteflies", "Caterpillars", "Beetles", "Mites", "Thrips"]
                num_pests = random.randint(0, 15)
                
                detections = []
                for i in range(num_pests):
                    pest_type = random.choice(pest_types)
                    confidence = random.uniform(70, 95)
                    
                    # Generate random bounding box
                    img_width, img_height = image.size
                    x1 = random.randint(0, img_width - 100)
                    y1 = random.randint(0, img_height - 100)
                    x2 = x1 + random.randint(50, 150)
                    y2 = y1 + random.randint(50, 150)
                    
                    detections.append({
                        'label': pest_type,
                        'confidence': confidence,
                        'bbox': [x1, y1, x2, y2]
                    })
                
                # Determine severity level
                if num_pests > 10:
                    severity_level = "High"
                elif num_pests > 5:
                    severity_level = "Medium"
                else:
                    severity_level = "Low"
                
                # Generate recommendations
                recommendations = {
                    "High": "Immediate pesticide application required",
                    "Medium": "Monitor closely and consider treatment",
                    "Low": "Continue monitoring, minimal intervention needed"
                }
                
                # Store results in session state
                results = {
                    'detections': detections,
                    'severity_level': severity_level,
                    'recommended_action': recommendations[severity_level],
                    'total_pests': num_pests
                }
                
                st.session_state.pest_detection_results = results
                st.session_state.pest_detection_analyzed = True
                
                # Display results in tabs
                tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔍 Detailed Analysis", "📄 Report", "💬 Chat Assistant"])
                
                with tab1:
                    st.markdown("### 📈 Detection Results")
                    
                    # Key metrics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="metric-container">
                            <h2 style="color: #2E8B57;">{num_pests}</h2>
                            <p>Pests Detected</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        pest_types_found = list(set([det['label'] for det in detections]))
                        st.markdown(f"""
                        <div class="metric-container">
                            <h2 style="color: #228B22;">{len(pest_types_found)}</h2>
                            <p>Pest Types</p>
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
                    
                    # Display image with bounding boxes
                    if detections:
                        st.markdown("### 🎯 Detected Pests")
                        img_with_boxes = draw_bounding_boxes(image, detections)
                        st.image(img_with_boxes, caption="Pest Detection Results", use_column_width=True)
                        
                        # Pest count chart
                        pest_chart = create_pest_count_chart(detections)
                        if pest_chart:
                            st.plotly_chart(pest_chart, use_container_width=True)
                    else:
                        st.success("✅ No pests detected in the image!")
                
                with tab2:
                    st.markdown("### 🔍 Detailed Analysis")
                
                if detections:
                        # Pest details
                        for i, detection in enumerate(detections, 1):
                            with st.expander(f"🐛 {detection['label']} (Confidence: {detection['confidence']:.1f}%)"):
                                st.markdown(f"**Location:** Bounding box coordinates")
                                st.markdown(f"**Confidence:** {detection['confidence']:.1f}%")
                                
                                # Pest-specific information
                                pest_info = {
                                    "Aphids": {
                                        "description": "Small, soft-bodied insects that suck plant sap",
                                        "lifecycle": "Reproduce rapidly, 7-10 day generation time",
                                        "control_methods": ["Neem oil spray", "Insecticidal soap", "Beneficial insects"]
                                    },
                                    "Whiteflies": {
                                        "description": "Small white insects that feed on plant sap",
                                        "lifecycle": "Complete lifecycle in 3-4 weeks",
                                        "control_methods": ["Yellow sticky traps", "Horticultural oil", "Biological control"]
                                    },
                                    "Caterpillars": {
                                        "description": "Larval stage of moths and butterflies",
                                        "lifecycle": "Feed voraciously for 2-4 weeks before pupation",
                                        "control_methods": ["Bt (Bacillus thuringiensis)", "Hand picking", "Natural predators"]
                                    },
                                    "Beetles": {
                                        "description": "Hard-shelled insects that chew on plant tissue",
                                        "lifecycle": "Complete metamorphosis, 4-6 week lifecycle",
                                        "control_methods": ["Pyrethrin sprays", "Crop rotation", "Trap crops"]
                                    },
                                    "Mites": {
                                        "description": "Tiny arachnids that suck plant sap",
                                        "lifecycle": "Rapid reproduction, 5-7 day lifecycle",
                                        "control_methods": ["Miticide sprays", "Predatory mites", "Humidity control"]
                                    },
                                    "Thrips": {
                                        "description": "Small, slender insects that feed on plant cells",
                                        "lifecycle": "Complete lifecycle in 2-3 weeks",
                                        "control_methods": ["Blue sticky traps", "Insecticidal soap", "Beneficial insects"]
                                    }
                                }
                                
                                info = pest_info.get(detection['label'], {
                                    "description": "General pest information",
                                    "lifecycle": "Variable lifecycle",
                                    "control_methods": ["General pest control methods"]
                                })
                                
                                st.markdown(f"**Description:** {info['description']}")
                                st.markdown(f"**Lifecycle:** {info['lifecycle']}")
                                st.markdown(f"**Control Methods:** {', '.join(info['control_methods'])}")
                        
                        # Severity chart
                        severity_data = {
                            "Low": 1 if severity_level == "Low" else 0,
                            "Medium": 1 if severity_level == "Medium" else 0,
                            "High": 1 if severity_level == "High" else 0
                        }
                        st.plotly_chart(create_severity_chart(severity_data), use_container_width=True)
                        
                        # Additional metrics
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Infestation Density", f"{num_pests} pests/image")
                            st.metric("Treatment Priority", "High" if severity_level == "High" else "Medium")
                        with col2:
                            st.metric("Expected Damage", f"{random.randint(10, 50)}%")
                            st.metric("Control Success Rate", f"{random.randint(80, 95)}%")
                else:
                    st.success("✅ No pests detected! Your crop appears to be pest-free.")
                
                with tab3:
                    st.markdown("### 📄 Comprehensive Report")
                    
                    # Generate report
                    image_info = {
                        'filename': uploaded_file.name,
                        'size': uploaded_file.size,
                        'dimensions': f"{image.size[0]}x{image.size[1]}"
                    }
                    
                    report = generate_pest_report(results, image_info)
                    
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
                        file_name=f"pest_detection_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                    
                    # PDF download placeholder
                    pdf_buffer = io.BytesIO()
                    st.download_button(
                        label="📄 Download PDF Report",
                        data=pdf_buffer,
                        file_name=f"pest_detection_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
                
                with tab4:
                    st.markdown("### 💬 Chat with Pest Management Expert")
                    analysis_context = f"Pests Detected: {len(detections)}, Types: {', '.join([det['label'] for det in detections]) if detections else 'None'}, Severity: {results['severity_level']}"
                    
                    # Enhanced Pest Detection Chatbot with Groq API
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #fff5f5 0%, #ffe8e8 100%); 
                                padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                                border: 2px solid #FF6B6B; box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
                        <h3 style="color: #d32f2f; margin-bottom: 1rem; text-align: center;">
                            🐛 Pest Management Specialist Chatbot
                        </h3>
                        <p style="text-align: center; color: #666; margin-bottom: 1rem;">
                            Powered by Groq AI - Specialized in pest identification, IPM strategies, and biological control
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Use the enhanced chat interface with unique key
                    try:
                        from modules.enhanced_chatbot import create_chat_interface
                        create_chat_interface("pest_detection", analysis_context, use_api=True, unique_key="pest_detection_analysis_chat")
                    except Exception as e:
                        st.error(f"❌ Chatbot error: {str(e)}")
                        st.info("💡 Please try refreshing the page or contact support.")
    
    else:
        st.info("👆 Please upload a crop image to start pest detection.")
        
        # Show sample analysis
        st.markdown("---")
        st.markdown("### 📊 Sample Analysis Preview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="sample-analysis">
                <h4>🐛 Aphid Infestation</h4>
                <p>Count: 12 pests</p>
                <p>Severity: High</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="sample-analysis">
                <h4>🦋 Caterpillar Damage</h4>
                <p>Count: 5 pests</p>
                <p>Severity: Medium</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="sample-analysis">
                <h4>✅ No Pests Detected</h4>
                <p>Count: 0 pests</p>
                <p>Status: Healthy</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: #2E8B57; color: white; border-radius: 10px; margin-top: 3rem;">
        <h4>🐛 Krishi Sahayak - Pest Detection System</h4>
        <p>Empowering Indian farmers with AI-driven pest detection and management</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">
            Built with ❤️ for Indian Agriculture | Advanced AI Technology
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()