import streamlit as st
import numpy as np
import cv2
import json
import datetime
import io
import base64
from PIL import Image
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from modules import preprocessing, chatbot
from modules.pdf_generator import PDFReportGenerator, create_download_button
from config import MODEL_CONFIGS, CUSTOM_CSS

# Inject custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Set page config
st.set_page_config(
    page_title="Irrigation Management - Krishi Sahayak",
    page_icon="💧",
    layout="wide"
)

def create_ndvi_heatmap(ndvi_map):
    """Create an interactive NDVI heatmap"""
    fig = go.Figure(data=go.Heatmap(
        z=ndvi_map,
        colorscale='RdYlGn',
        showscale=True,
        colorbar=dict(
            title=dict(
                text="NDVI Value",
                side="right"
            ),
            tickmode="array",
            tickvals=[-1, -0.5, 0, 0.2, 0.4, 0.6, 0.8, 1],
            ticktext=["Water", "Soil", "Bare", "Sparse", "Moderate", "Dense", "Very Dense", "Maximum"]
        )
    ))
    
    fig.update_layout(
        title="NDVI Water Stress Analysis",
        title_x=0.5,
        height=500,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    
    return fig

def create_stress_distribution_chart(stress_zones):
    """Create a pie chart showing water stress distribution"""
    labels = list(stress_zones.keys())
    values = list(stress_zones.values())
    colors = ['#FF4444', '#FFA500', '#32CD32', '#228B22']  # Red, Orange, Green, Dark Green
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker_colors=colors[:len(labels)],
        textinfo='label+percent',
        textfont_size=14
    )])
    
    fig.update_layout(
        title="Water Stress Zone Distribution",
        title_x=0.5,
        showlegend=True,
        height=400,
        font=dict(size=12)
    )
    
    return fig

def create_irrigation_recommendations_chart(recommendations):
    """Create a bar chart showing irrigation recommendations"""
    zones = list(recommendations.keys())
    water_needs = [rec.get('water_needed', 0) for rec in recommendations.values()]
    
    fig = go.Figure(data=[go.Bar(
        x=zones,
        y=water_needs,
        marker_color=['#FF4444', '#FFA500', '#32CD32', '#228B22'][:len(zones)],
        text=water_needs,
        textposition='auto',
    )])
    
    fig.update_layout(
        title="Water Requirements by Zone",
        title_x=0.5,
        xaxis_title="Stress Zones",
        yaxis_title="Water Needed (mm)",
        height=400
    )
    
    return fig

def generate_irrigation_report(analysis_results, image_info):
    """Generate comprehensive irrigation management report"""
    report = {
        "report_metadata": {
            "generated_at": datetime.datetime.now().isoformat(),
            "report_type": "Irrigation Management Analysis",
            "version": "1.0",
            "image_info": image_info
        },
        "executive_summary": {
            "overall_stress_level": analysis_results.get('overall_stress_level', 'Low'),
            "water_efficiency_score": analysis_results.get('water_efficiency_score', 85),
            "irrigation_priority": analysis_results.get('irrigation_priority', 'Low'),
            "recommended_action": analysis_results.get('recommended_action', 'Monitor')
        },
        "risk_assessment": {
            "water_stress_severity": analysis_results.get('water_stress_severity', 'Low'),
            "crop_health_impact": analysis_results.get('crop_health_impact', 'Minimal'),
            "yield_potential": analysis_results.get('yield_potential', 'High'),
            "drought_risk": analysis_results.get('drought_risk', 'Low')
        },
        "timeline_recommendations": {
            "immediate_actions": analysis_results.get('immediate_actions', []),
            "short_term_1_2_weeks": analysis_results.get('short_term_actions', []),
            "long_term_1_3_months": analysis_results.get('long_term_actions', [])
        },
        "cost_benefit_analysis": {
            "irrigation_cost": analysis_results.get('irrigation_cost', 0),
            "water_savings_potential": analysis_results.get('water_savings', 0),
            "yield_protection": analysis_results.get('yield_protection', 0),
            "roi_estimate": analysis_results.get('roi', 0)
        },
        "action_checklist": analysis_results.get('action_checklist', []),
        "follow_up_actions": analysis_results.get('follow_up_actions', []),
        "prevention_strategies": analysis_results.get('prevention_strategies', [])
    }
    
    return report

def main():
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #2E8B57; font-size: 3rem; margin-bottom: 1rem;">
            💧 Irrigation Management
        </h1>
        <p style="color: #228B22; font-size: 1.2rem; max-width: 600px; margin: 0 auto;">
            Advanced NDVI-based water stress analysis for smart irrigation and water conservation
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📸 Upload Multispectral Images")
    st.info("""
    **For accurate NDVI analysis, please upload:**
    - Multispectral images with NIR (Near-Infrared) and Red bands
    - Supported formats: .TIF, .TIFF (multispectral) or separate .JPG/.PNG files
    - For separate files, name them with 'NIR' and 'Red' in the filename
    """)
    
    uploaded_files = st.file_uploader(
        "Choose multispectral images...", 
        type=["jpg", "jpeg", "png", "tif", "tiff"], 
        accept_multiple_files=True,
        help="Upload multispectral images for NDVI water stress analysis"
    )
    
    nir_image = None
    red_image = None
    original_image = None
    
    if uploaded_files:
        st.info("🔍 Analyzing uploaded files for NIR and Red channels...")
        
        # Check for TIF/TIFF file (multispectral)
        for file in uploaded_files:
            if file.name.lower().endswith(('.tif', '.tiff')):
                try:
                    tif_image = Image.open(file)
                    bands = tif_image.split()
                    if len(bands) >= 4:
                        red_image = np.array(bands[0])
                        nir_image = np.array(bands[3])
                        original_image = np.array(tif_image.convert('RGB'))
                        st.success("✅ NIR and Red channels found in multispectral .TIF file")
                        break
                    else:
                        st.error("❌ The .TIF file doesn't have required 4 bands (RGB + NIR)")
                except Exception as e:
                    st.error(f"❌ Error processing .TIF file: {e}")
                    
        # Check for separate files
        if nir_image is None and len(uploaded_files) >= 2:
            st.warning("🔍 Checking for separate NIR and Red channel files...")
            
            for file in uploaded_files:
                file_name_lower = file.name.lower()
                if 'nir' in file_name_lower:
                    nir_image = np.array(Image.open(file).convert('L'))
                elif 'red' in file_name_lower:
                    red_image = np.array(Image.open(file).convert('L'))
                elif original_image is None:
                    original_image = np.array(Image.open(file).convert('RGB'))
            
            if nir_image is not None and red_image is not None:
                st.success("✅ NIR and Red channels found from separate files")
            else:
                st.error("❌ Required NIR and Red channels not found in uploaded files")
                st.info("💡 Please ensure files contain 'NIR' and 'Red' in their names")
    
    if uploaded_files and nir_image is not None and red_image is not None:
        # Display image information
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if original_image is not None:
                st.image(original_image, caption="Original Multispectral Image", use_container_width=True)
            else:
                st.info("📷 Multispectral image loaded successfully")
        
        with col2:
            st.markdown("### 📋 Image Information")
            st.info(f"**Files:** {len(uploaded_files)} uploaded")
            st.info(f"**NIR Channel:** {'✅ Found' if nir_image is not None else '❌ Missing'}")
            st.info(f"**Red Channel:** {'✅ Found' if red_image is not None else '❌ Missing'}")
            st.info(f"**Analysis Ready:** {'✅ Yes' if nir_image is not None and red_image is not None else '❌ No'}")

        # Analysis button
        if st.button("🔍 Analyze Water Stress", use_container_width=True):
            with st.spinner("🤖 Performing advanced multi-method water stress analysis..."):
                try:
                    # Validate images before processing
                    if nir_image is None or red_image is None:
                        st.error("❌ Missing NIR or Red channel data")
                        return
                    
                    # Check if images have valid dimensions
                    if nir_image.size == 0 or red_image.size == 0:
                        st.error("❌ Invalid image data - empty arrays detected")
                        return
                    
                    # Resize images for consistent analysis with proper validation
                    try:
                        nir_resized = cv2.resize(nir_image, (512, 512))
                        red_resized = cv2.resize(red_image, (512, 512))
                    except cv2.error as e:
                        st.error(f"❌ Image resize error: {e}")
                        st.info("💡 Please try uploading different images")
                        return
                    
                    # Calculate multiple vegetation indices
                    ndvi_map = preprocessing.calculate_ndvi(nir_resized, red_resized)
                    
                    # Additional vegetation indices for comprehensive analysis
                    # Enhanced Vegetation Index (EVI)
                    evi_map = (2.5 * (nir_resized - red_resized)) / (nir_resized + 6 * red_resized - 7.5 * np.mean(red_resized) + 1)
                    
                    # Normalized Difference Water Index (NDWI)
                    ndwi_map = (nir_resized - red_resized) / (nir_resized + red_resized)
                    
                    # Soil Adjusted Vegetation Index (SAVI)
                    savi_map = ((nir_resized - red_resized) / (nir_resized + red_resized + 0.5)) * 1.5
                    
                    # Green Normalized Difference Vegetation Index (GNDVI)
                    if original_image is not None:
                        try:
                            green_channel = cv2.cvtColor(cv2.resize(original_image, (512, 512)), cv2.COLOR_RGB2GRAY)
                            gndvi_map = (nir_resized - green_channel) / (nir_resized + green_channel)
                        except cv2.error:
                            # Fallback if green channel extraction fails
                            gndvi_map = np.zeros_like(ndvi_map)
                    else:
                        gndvi_map = np.zeros_like(ndvi_map)
                    
                    # Classify stress zones using multiple indices
                    stress_zones = preprocessing.classify_ndvi_zones(ndvi_map)
                    
                    # Enhanced stress analysis using multiple indices
                    evi_stress_zones = preprocessing.classify_ndvi_zones(evi_map)
                    ndwi_stress_zones = preprocessing.classify_ndvi_zones(ndwi_map)
                    savi_stress_zones = preprocessing.classify_ndvi_zones(savi_map)
                    
                    # Generate colorized maps
                    ndvi_colorized = preprocessing.colorize_ndvi(ndvi_map)
                    evi_colorized = preprocessing.colorize_ndvi(evi_map)
                    ndwi_colorized = preprocessing.colorize_ndvi(ndwi_map)
                    savi_colorized = preprocessing.colorize_ndvi(savi_map)
                    
                    # Enhanced analysis results using multiple indices
                    # Calculate composite stress score
                    ndvi_stress_score = stress_zones.get('High Stress', 0) + stress_zones.get('Moderate Stress', 0) * 0.5
                    evi_stress_score = evi_stress_zones.get('High Stress', 0) + evi_stress_zones.get('Moderate Stress', 0) * 0.5
                    ndwi_stress_score = ndwi_stress_zones.get('High Stress', 0) + ndwi_stress_zones.get('Moderate Stress', 0) * 0.5
                    savi_stress_score = savi_stress_zones.get('High Stress', 0) + savi_stress_zones.get('Moderate Stress', 0) * 0.5
                    
                    # Weighted composite stress score
                    composite_stress_score = (ndvi_stress_score * 0.4 + evi_stress_score * 0.3 + ndwi_stress_score * 0.2 + savi_stress_score * 0.1)
                    
                    overall_stress = "High" if composite_stress_score > 30 else "Moderate" if composite_stress_score > 15 else "Low"
                    
                    analysis_results = {
                        'stress_zones': stress_zones,
                        'evi_stress_zones': evi_stress_zones,
                        'ndwi_stress_zones': ndwi_stress_zones,
                        'savi_stress_zones': savi_stress_zones,
                        'ndvi_map': ndvi_map,
                        'evi_map': evi_map,
                        'ndwi_map': ndwi_map,
                        'savi_map': savi_map,
                        'composite_stress_score': composite_stress_score,
                        'overall_stress_level': overall_stress,
                        'water_efficiency_score': max(0, 100 - (composite_stress_score * 2)),
                        'irrigation_priority': 'High' if overall_stress == 'High' else 'Medium' if overall_stress == 'Moderate' else 'Low',
                        'recommended_action': 'Immediate Irrigation' if overall_stress == 'High' else 'Schedule Irrigation' if overall_stress == 'Moderate' else 'Monitor',
                        'water_stress_severity': overall_stress,
                        'crop_health_impact': 'Severe' if overall_stress == 'High' else 'Moderate' if overall_stress == 'Moderate' else 'Minimal',
                        'yield_potential': 'At Risk' if overall_stress == 'High' else 'Moderate Risk' if overall_stress == 'Moderate' else 'High',
                        'drought_risk': 'High' if overall_stress == 'High' else 'Medium' if overall_stress == 'Moderate' else 'Low',
                        'immediate_actions': [
                            f"Focus irrigation on {composite_stress_score:.1f}% composite high-stress areas",
                            "Monitor soil moisture levels using multiple indices",
                            "Check irrigation system efficiency",
                            f"NDVI shows {stress_zones.get('High Stress', 0):.1f}% high stress",
                            f"EVI indicates {evi_stress_zones.get('High Stress', 0):.1f}% stress zones",
                            f"NDWI reveals {ndwi_stress_zones.get('High Stress', 0):.1f}% water stress"
                        ],
                        'short_term_actions': [
                            "Implement variable rate irrigation based on composite analysis",
                            "Adjust irrigation schedule using NDVI, EVI, NDWI, and SAVI zones",
                            "Evaluate water distribution uniformity",
                            "Cross-validate results using multiple vegetation indices"
                        ],
                        'long_term_actions': [
                            "Install multi-spectral soil moisture sensors",
                            "Implement precision irrigation system with composite mapping",
                            "Develop water conservation strategies using multiple indices",
                            "Establish baseline monitoring with all vegetation indices"
                        ],
                        'irrigation_cost': composite_stress_score * 80 + stress_zones.get('Moderate Stress', 0) * 40,
                        'water_savings': max(0, 25 - composite_stress_score * 0.4),
                        'yield_protection': composite_stress_score * 0.25,
                        'roi': max(0, (composite_stress_score * 0.25 * 2000) - (composite_stress_score * 80)),
                        'action_checklist': [
                            "✓ Analyze NDVI, EVI, NDWI, and SAVI stress zones",
                            "✓ Calculate composite stress score",
                            "✓ Identify high-priority irrigation areas",
                            "✓ Cross-validate using multiple indices",
                            "✓ Check irrigation system status",
                            "✓ Plan irrigation schedule based on composite analysis",
                            "✓ Monitor weather conditions",
                            "✓ Apply targeted irrigation",
                            "✓ Document irrigation effectiveness",
                            "✓ Update irrigation strategy with multi-index approach"
                        ],
                        'follow_up_actions': [
                            "Re-analyze all vegetation indices after irrigation",
                            "Monitor crop response using composite analysis",
                            "Adjust irrigation timing based on multi-index validation",
                            "Update irrigation management plan with composite mapping",
                            "Compare NDVI, EVI, NDWI, and SAVI trends over time"
                        ],
                        'prevention_strategies': [
                            "Implement multi-spectral soil moisture monitoring",
                            "Use weather-based irrigation scheduling with composite analysis",
                            "Practice deficit irrigation techniques validated by multiple indices",
                            "Install efficient irrigation systems with precision mapping",
                            "Maintain proper soil organic matter for water retention",
                            "Implement crop rotation for water efficiency",
                            "Establish baseline monitoring using NDVI, EVI, NDWI, and SAVI"
                        ]
                    }
                    
                    # Store results
                    st.session_state['irrigation_analysis_results'] = analysis_results
                    st.session_state['ndvi_colorized'] = ndvi_colorized
                    st.session_state['evi_colorized'] = evi_colorized
                    st.session_state['ndwi_colorized'] = ndwi_colorized
                    st.session_state['savi_colorized'] = savi_colorized
                    st.session_state['irrigation_image_info'] = {
                        "files_uploaded": len(uploaded_files),
                        "analysis_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "image_type": "Multispectral",
                        "analysis_methods": "NDVI, EVI, NDWI, SAVI Composite Analysis"
                    }
                
                except Exception as e:
                    st.error(f"❌ Analysis error: {e}")
                    st.info("💡 Please try uploading different images or contact support if the issue persists.")

        if 'irrigation_analysis_results' in st.session_state:
            results = st.session_state['irrigation_analysis_results']
            ndvi_colorized = st.session_state['ndvi_colorized']
            evi_colorized = st.session_state['evi_colorized']
            ndwi_colorized = st.session_state['ndwi_colorized']
            savi_colorized = st.session_state['savi_colorized']
            image_info = st.session_state['irrigation_image_info']
            
            st.success("✅ Water Stress Analysis Complete!")
            st.markdown("### 🎯 Analysis Results")
            
            # Create tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔍 Detailed Analysis", "📋 Report", "💬 Chat Assistant"])
            
            with tab1:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-container">
                        <h2 style="color: #FF6B6B;">{results['overall_stress_level']}</h2>
                        <p>Overall Stress Level</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-container">
                        <h2 style="color: #32CD32;">{results['water_efficiency_score']:.0f}%</h2>
                        <p>Water Efficiency Score</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-container">
                        <h2 style="color: #FFA500;">{results['irrigation_priority']}</h2>
                        <p>Irrigation Priority</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="metric-container">
                        <h2 style="color: #228B22;">{results['recommended_action']}</h2>
                        <p>Recommended Action</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Multi-Method Water Stress Analysis
                st.markdown("### 💧 Multi-Method Water Stress Analysis")
                
                # Show all vegetation indices
                st.markdown("#### 📊 Vegetation Indices Comparison")
                col1, col2 = st.columns(2)
                with col1:
                    st.image(ndvi_colorized, caption="NDVI - Normalized Difference Vegetation Index", use_container_width=True)
                    st.image(evi_colorized, caption="EVI - Enhanced Vegetation Index", use_container_width=True)
                with col2:
                    st.image(ndwi_colorized, caption="NDWI - Normalized Difference Water Index", use_container_width=True)
                    st.image(savi_colorized, caption="SAVI - Soil Adjusted Vegetation Index", use_container_width=True)
                
                # Interactive composite analysis
                st.markdown("#### 🎯 Composite Stress Analysis")
                fig_ndvi = create_ndvi_heatmap(results['ndvi_map'])
                st.plotly_chart(fig_ndvi, use_container_width=True)
                
                # Composite stress distribution
                st.markdown(f"**Composite Stress Score:** {results['composite_stress_score']:.1f}")
                fig_stress = create_stress_distribution_chart(results['stress_zones'])
                st.plotly_chart(fig_stress, use_container_width=True)
            
            with tab2:
                st.markdown("### 🔍 Detailed Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 💧 Multi-Index Water Stress Zones")
                    
                    st.markdown("**NDVI Analysis:**")
                    for zone, percentage in results['stress_zones'].items():
                        if percentage > 0:
                            color = "#FF4444" if "High" in zone else "#FFA500" if "Moderate" in zone else "#32CD32"
                            st.markdown(f"**{zone}:** <span style='color: {color}'>{percentage:.1f}%</span>", unsafe_allow_html=True)
                    
                    st.markdown("**EVI Analysis:**")
                    for zone, percentage in results['evi_stress_zones'].items():
                        if percentage > 0:
                            color = "#FF4444" if "High" in zone else "#FFA500" if "Moderate" in zone else "#32CD32"
                            st.markdown(f"**{zone}:** <span style='color: {color}'>{percentage:.1f}%</span>", unsafe_allow_html=True)
                    
                    st.markdown("**NDWI Analysis:**")
                    for zone, percentage in results['ndwi_stress_zones'].items():
                        if percentage > 0:
                            color = "#FF4444" if "High" in zone else "#FFA500" if "Moderate" in zone else "#32CD32"
                            st.markdown(f"**{zone}:** <span style='color: {color}'>{percentage:.1f}%</span>", unsafe_allow_html=True)
                    
                    st.markdown("#### 📊 Composite Impact Assessment")
                    st.metric("Composite Stress Score", f"{results['composite_stress_score']:.1f}")
                    st.metric("Crop Health Impact", results['crop_health_impact'])
                    st.metric("Yield Potential", results['yield_potential'])
                    st.metric("Drought Risk", results['drought_risk'])
                
                with col2:
                    st.markdown("#### 🎯 Irrigation Recommendations")
                    st.markdown("**Immediate Actions:**")
                    for action in results['immediate_actions']:
                        st.markdown(f"• {action}")
                    
                    st.markdown("**Short-term (1-2 weeks):**")
                    for action in results['short_term_actions']:
                        st.markdown(f"• {action}")
                    
                    # Irrigation recommendations chart
                    recommendations = {
                        zone: {'water_needed': percentage * 2} for zone, percentage in results['stress_zones'].items() if percentage > 0
                    }
                    fig_rec = create_irrigation_recommendations_chart(recommendations)
                    st.plotly_chart(fig_rec, use_container_width=True)
            
            with tab3:
                st.markdown("### 📋 Comprehensive Report")
                
                # Executive Summary
                st.markdown("#### 📊 Executive Summary")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Stress Level", results['overall_stress_level'])
                with col2:
                    st.metric("Efficiency Score", f"{results['water_efficiency_score']:.0f}%")
                with col3:
                    st.metric("Irrigation Cost", f"₹{results['irrigation_cost']:.0f}")
                with col4:
                    st.metric("ROI Estimate", f"₹{results['roi']:.0f}")
                
                # Risk Assessment
                st.markdown("#### ⚠️ Risk Assessment")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Water Stress Analysis:**")
                    st.info(f"**Severity:** {results['water_stress_severity']}")
                    st.info(f"**Crop Impact:** {results['crop_health_impact']}")
                    st.info(f"**Yield Risk:** {results['yield_potential']}")
                
                with col2:
                    st.markdown("**Irrigation Planning:**")
                    st.warning(f"**Priority:** {results['irrigation_priority']}")
                    st.warning(f"**Action:** {results['recommended_action']}")
                    st.warning(f"**Drought Risk:** {results['drought_risk']}")
                
                # Timeline Recommendations
                st.markdown("#### ⏰ Timeline Recommendations")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("**Immediate (0-3 days):**")
                    for action in results['immediate_actions']:
                        st.markdown(f"• {action}")
                
                with col2:
                    st.markdown("**Short-term (1-2 weeks):**")
                    for action in results['short_term_actions']:
                        st.markdown(f"• {action}")
                
                with col3:
                    st.markdown("**Long-term (1-3 months):**")
                    for action in results['long_term_actions']:
                        st.markdown(f"• {action}")
                
                # Cost-Benefit Analysis
                st.markdown("#### 💰 Cost-Benefit Analysis")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Irrigation Cost", f"₹{results['irrigation_cost']:.0f}")
                with col2:
                    st.metric("Water Savings", f"{results['water_savings']:.1f}%")
                with col3:
                    st.metric("Yield Protection", f"{results['yield_protection']:.1f}%")
                with col4:
                    st.metric("ROI", f"₹{results['roi']:.0f}")
                
                # Action Checklist
                st.markdown("#### ✅ Action Checklist")
                for item in results['action_checklist']:
                    st.markdown(item)
                
                # Prevention Strategies
                st.markdown("#### 🛡️ Prevention Strategies")
                for strategy in results['prevention_strategies']:
                    st.markdown(f"• {strategy}")
                
                # Download report button
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📥 Download Detailed Report", use_container_width=True):
                        detailed_report = generate_irrigation_report(results, image_info)
                        report_json = json.dumps(detailed_report, indent=2, default=str)
                        
                        st.download_button(
                            label="📄 Download JSON Report",
                            data=report_json,
                            file_name=f"irrigation_analysis_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json",
                            use_container_width=True
                        )
                
                with col2:
                    if st.button("📄 Download PDF Report", use_container_width=True):
                        try:
                            pdf_generator = PDFReportGenerator()
                            pdf_buffer = pdf_generator.create_irrigation_pdf(results, image_info)
                            
                            create_download_button(
                                pdf_buffer,
                                f"irrigation_analysis_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                "📄 Download PDF Report"
                            )
                        except Exception as e:
                            st.error(f"❌ PDF generation error: {e}")
                            st.info("💡 Please try again or contact support if the issue persists.")
            
            with tab4:
                st.markdown("### 💬 Chat with Irrigation Expert")
                analysis_context = f"Water Stress: {results['overall_stress_level']}, Efficiency: {results['water_efficiency_score']:.1f}%, Priority: {results['irrigation_priority']}"
                
                # Enhanced Irrigation Management Chatbot with Groq API
                st.markdown("""
                <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                            padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                            border: 2px solid #2196f3; box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
                    <h3 style="color: #1976d2; margin-bottom: 1rem; text-align: center;">
                        💧 Irrigation Management Specialist Chatbot
                    </h3>
                    <p style="text-align: center; color: #666; margin-bottom: 1rem;">
                        Powered by Groq AI - Specialized in water management, irrigation scheduling, and drought management
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                chatbot.display_chat_interface("irrigation_management", analysis_context)
    
    else:
        st.info("👆 Please upload multispectral images to start water stress analysis.")
        
        # Show sample analysis
        st.markdown("### 🔍 Sample Irrigation Analysis Preview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="custom-card">
                <h4>💧 Low Water Stress</h4>
                <p>NDVI: 0.6-0.8</p>
                <p>Efficiency: 90%</p>
                <p>Action: Monitor</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="custom-card">
                <h4>🌡️ Moderate Stress</h4>
                <p>NDVI: 0.3-0.6</p>
                <p>Efficiency: 75%</p>
                <p>Action: Schedule Irrigation</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="custom-card">
                <h4>🔥 High Water Stress</h4>
                <p>NDVI: 0.0-0.3</p>
                <p>Efficiency: 60%</p>
                <p>Action: Immediate Irrigation</p>
            </div>
            """, unsafe_allow_html=True)
        
        chatbot.display_chat_interface("irrigation_management")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: #2E8B57; color: white; border-radius: 10px; margin-top: 3rem;">
        <h4>💧 Krishi Sahayak - Irrigation Management</h4>
        <p>Smart water management for sustainable agriculture</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">
            Built with ❤️ for Indian Agriculture | Jai Jawan, Jai Kisan!
        </p>
    </div>
    """, unsafe_allow_html=True)
        
if __name__ == "__main__":
    main()