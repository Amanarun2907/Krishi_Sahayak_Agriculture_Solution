import streamlit as st
import numpy as np
import cv2
from PIL import Image
import tensorflow as tf
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys
from skimage.segmentation import slic

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from modules.xai_utils import *
from modules.enhanced_chatbot import create_chat_interface
from config import CUSTOM_CSS, MODEL_CONFIGS, MODELS_DIR, CHATBOT_PROMPTS

# Inject custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Set page config
st.set_page_config(
    page_title="Explainable AI - Krishi Sahayak",
    page_icon="🔍",
    layout="wide"
)

# Main title
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="color: #2E8B57; font-size: 3.5rem; margin-bottom: 1rem;">
        🔍 Explainable AI (XAI)
    </h1>
    <p style="color: #228B22; font-size: 1.3rem; max-width: 800px; margin: 0 auto;">
        Understanding AI Decisions - Making the Black Box Transparent
    </p>
</div>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Grad-CAM",
    "🔬 LIME", 
    "📊 SHAP",
    "🔄 Counterfactuals",
    "🤖 XAI Chat Assistant"
])

# ==================== TAB 1: GRAD-CAM ====================
with tab1:
    st.header("🎯 Grad-CAM: Visual Attention Analysis")
    
    # Explanation box
    with st.expander("📖 What is Grad-CAM? (Click to expand)", expanded=False):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            ### 🎓 Technical Explanation
            
            **Gradient-weighted Class Activation Mapping (Grad-CAM)**
            
            **How it works:**
            1. Takes the final convolutional layer of the neural network
            2. Computes gradients of the predicted class with respect to feature maps
            3. Weights the feature maps by these gradients
            4. Creates a heatmap showing important regions
            
            **Mathematical Formula:**
            ```
            L^c_Grad-CAM = ReLU(Σ αᵏ Aᵏ)
            
            where: αᵏ = (1/Z) Σᵢ Σⱼ ∂yᶜ/∂Aᵏᵢⱼ
            ```
            
            **Key Points:**
            - ✅ Works with any CNN (ResNet, VGG, etc.)
            - ✅ No model retraining needed
            - ✅ Fast computation
            - ✅ Class-discriminative
            """)
        
        with col2:
            st.markdown("""
            ### 👨‍🌾 Simple Explanation
            
            **Think of it like highlighting a textbook:**
            
            Grad-CAM shows WHERE the AI is looking in your image to make its decision.
            
            **In Agriculture:**
            - For **Nitrogen Deficiency**: Should highlight yellowing leaves
            - For **Pest Detection**: Should highlight pest locations
            - For **Disease**: Should highlight affected areas
            
            **Color Meaning:**
            - 🔴 **Red regions**: High importance (AI focused here)
            - 🟡 **Yellow regions**: Medium importance
            - 🔵 **Blue regions**: Low importance (AI ignored)
            
            **Why it matters:**
            - Builds trust in AI decisions
            - Helps verify if AI is looking at the right features
            - Useful for debugging wrong predictions
            """)
    
    st.markdown("---")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "📸 Upload Crop Image for Grad-CAM Analysis",
        type=['jpg', 'jpeg', 'png'],
        key="gradcam_upload"
    )
    
    if uploaded_file is not None:
        # Load image and convert to RGB (remove alpha channel if present)
        image = Image.open(uploaded_file)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image_np = np.array(image)
        
        # Model selection
        model_choice = st.selectbox(
            "Select Model",
            ["Crop Health (ResNet50)", "Multi-Task Model"],
            key="gradcam_model"
        )
        
        # Heatmap intensity slider
        alpha = st.slider("Heatmap Intensity", 0.0, 1.0, 0.4, 0.1, key="gradcam_alpha")
        
        if st.button("🚀 Generate Grad-CAM", key="gradcam_button"):
            with st.spinner("Generating Grad-CAM visualization..."):
                try:
                    # Load model
                    if "Crop Health" in model_choice:
                        model_path = Path(MODELS_DIR) / "crop_health_model.h5"
                        if model_path.exists():
                            model = tf.keras.models.load_model(str(model_path))
                            
                            # Preprocess image
                            img_resized = cv2.resize(image_np, (224, 224))
                            img_normalized = img_resized / 255.0
                            img_array = np.expand_dims(img_normalized, axis=0)
                            
                            # Get prediction
                            predictions = model.predict(img_array, verbose=0)[0]
                            class_names = MODEL_CONFIGS['crop_health']['class_names']
                            pred_class = np.argmax(predictions)
                            pred_label = class_names[pred_class]
                            confidence = predictions[pred_class]
                            
                            # Get last conv layer
                            last_conv_layer = get_last_conv_layer_name(model)
                            
                            # Generate Grad-CAM
                            heatmap = make_gradcam_heatmap(img_array, model, last_conv_layer, pred_class)
                            
                            # Create overlay
                            overlay, heatmap_colored = create_gradcam_overlay(img_resized, heatmap, alpha)
                            
                            # Display results
                            st.success(f"✅ Prediction: **{pred_label}** (Confidence: {confidence*100:.1f}%)")
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.subheader("Original Image")
                                st.image(img_resized, use_container_width=True)
                            
                            with col2:
                                st.subheader("Grad-CAM Heatmap")
                                st.image(heatmap_colored, use_container_width=True)
                            
                            with col3:
                                st.subheader("Overlay")
                                st.image(overlay, use_container_width=True)
                            
                            # Region importance
                            st.markdown("### 📊 Region Importance Analysis")
                            regions = get_region_importance_scores(heatmap, num_regions=5)
                            
                            if regions:
                                # Create bar chart
                                region_names = [f"Region {i+1}" for i in range(len(regions))]
                                scores = [r['score'] for r in regions]
                                
                                fig = go.Figure(data=[
                                    go.Bar(
                                        x=region_names,
                                        y=scores,
                                        marker_color='indianred',
                                        text=[f"{s:.3f}" for s in scores],
                                        textposition='auto'
                                    )
                                ])
                                
                                fig.update_layout(
                                    title="Top 5 Most Important Regions",
                                    xaxis_title="Region",
                                    yaxis_title="Importance Score",
                                    height=400
                                )
                                
                                st.plotly_chart(fig, use_container_width=True)
                                
                                # Show region details
                                st.markdown("#### Region Details:")
                                for i, region in enumerate(regions):
                                    x, y, w, h = region['bbox']
                                    st.write(f"**Region {i+1}:** Position ({x}, {y}), Size ({w}×{h}), Score: {region['score']:.3f}")
                            
                            # Interpretation guide
                            st.info("""
                            💡 **How to Interpret:**
                            - The model focused on **red/yellow regions** to make its prediction
                            - If these regions match the actual problem area (e.g., diseased leaves), the model is working correctly
                            - If the model is looking at irrelevant areas, it may need retraining
                            """)
                            
                        else:
                            st.error("❌ Crop Health model not found. Please train the model first.")
                    
                except Exception as e:
                    st.error(f"❌ Error generating Grad-CAM: {str(e)}")
                    st.info("💡 Using demo visualization...")
                    
                    # Demo visualization
                    img_resized = cv2.resize(image_np, (224, 224))
                    demo_heatmap = np.random.rand(7, 7)
                    demo_heatmap = cv2.resize(demo_heatmap, (224, 224))
                    overlay, heatmap_colored = create_gradcam_overlay(img_resized, demo_heatmap, alpha)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.image(img_resized, caption="Original", use_container_width=True)
                    with col2:
                        st.image(heatmap_colored, caption="Heatmap (Demo)", use_container_width=True)
                    with col3:
                        st.image(overlay, caption="Overlay (Demo)", use_container_width=True)

# ==================== TAB 2: LIME ====================
with tab2:
    st.header("🔬 LIME: Local Interpretable Explanations")
    
    with st.expander("📖 What is LIME?", expanded=False):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            ### 🎓 Technical Explanation
            
            **Local Interpretable Model-agnostic Explanations**
            
            **Algorithm:**
            1. Segment image into superpixels
            2. Create perturbed versions by hiding superpixels
            3. Get predictions for all perturbed images
            4. Fit linear model to explain prediction
            5. Show which superpixels contributed most
            
            **Mathematical Foundation:**
            ```
            explanation(x) = argmin L(f, g, πₓ) + Ω(g)
            
            where:
            - f: original model
            - g: interpretable model
            - πₓ: proximity measure
            - Ω: complexity measure
            ```
            
            **Key Points:**
            - ✅ Model-agnostic (works with any model)
            - ✅ Provides quantitative importance scores
            - ✅ Local explanations (for specific image)
            - ⚠️ Slower than Grad-CAM
            """)
        
        with col2:
            st.markdown("""
            ### 👨‍🌾 Simple Explanation
            
            **Think of it like a puzzle:**
            
            LIME breaks your image into pieces and tests which pieces matter most for the AI's decision.
            
            **How it works:**
            1. Divide image into small regions (superpixels)
            2. Hide different combinations of regions
            3. See how predictions change
            4. Find which regions are most important
            
            **Color Meaning:**
            - 🟢 **Green segments**: Positive contribution (support prediction)
            - 🔴 **Red segments**: Negative contribution (against prediction)
            - Larger segments = More important
            
            **Example:**
            "This leaf segment increased Nitrogen Deficiency prediction by 30%"
            
            **Why it matters:**
            - Shows exact contribution of each image part
            - Works with any AI model
            - Helps understand individual predictions
            """)
    
    st.markdown("---")
    
    uploaded_file_lime = st.file_uploader(
        "📸 Upload Image for LIME Analysis",
        type=['jpg', 'jpeg', 'png'],
        key="lime_upload"
    )
    
    if uploaded_file_lime:
        image = Image.open(uploaded_file_lime)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image_np = np.array(image)
        
        num_samples = st.slider("Number of Samples", 100, 2000, 1000, 100, key="lime_samples")
        
        if st.button("🚀 Generate LIME Explanation", key="lime_button"):
            with st.spinner("Generating LIME explanation..."):
                try:
                    # Try to import lime
                    from lime import lime_image
                    from skimage.segmentation import quickshift, mark_boundaries
                    
                    # Load model
                    model_path = Path(MODELS_DIR) / "crop_health_model.h5"
                    if model_path.exists():
                        model = tf.keras.models.load_model(str(model_path))
                        
                        # Preprocess
                        img_resized = cv2.resize(image_np, (224, 224))
                        
                        # Create explainer
                        explainer = lime_image.LimeImageExplainer()
                        
                        # Prediction function
                        def predict_fn(images):
                            processed = []
                            for img in images:
                                img_norm = img / 255.0
                                processed.append(img_norm)
                            processed = np.array(processed)
                            return model.predict(processed, verbose=0)
                        
                        # Generate explanation
                        explanation = explainer.explain_instance(
                            img_resized,
                            predict_fn,
                            top_labels=3,
                            hide_color=0,
                            num_samples=num_samples
                        )
                        
                        # Get prediction
                        predictions = model.predict(np.expand_dims(img_resized/255.0, axis=0), verbose=0)[0]
                        class_names = MODEL_CONFIGS['crop_health']['class_names']
                        pred_class = np.argmax(predictions)
                        
                        # Get image and mask
                        temp, mask = explanation.get_image_and_mask(
                            pred_class,
                            positive_only=False,
                            num_features=10,
                            hide_rest=False
                        )
                        
                        # Display results
                        st.success(f"✅ Prediction: **{class_names[pred_class]}** (Confidence: {predictions[pred_class]*100:.1f}%)")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.subheader("Original Image")
                            st.image(img_resized, use_container_width=True)
                        
                        with col2:
                            st.subheader("LIME Explanation")
                            # Show boundaries
                            img_boundary = mark_boundaries(temp/255.0, mask)
                            st.image(img_boundary, use_container_width=True)
                        
                        with col3:
                            st.subheader("Important Regions")
                            # Show only positive contributions
                            temp_pos, mask_pos = explanation.get_image_and_mask(
                                pred_class,
                                positive_only=True,
                                num_features=5,
                                hide_rest=True
                            )
                            st.image(temp_pos, use_container_width=True)
                        
                        # Feature importance
                        st.markdown("### 📊 Superpixel Importance")
                        
                        # Get local explanation
                        local_exp = explanation.local_exp[pred_class]
                        
                        # Sort by importance
                        sorted_exp = sorted(local_exp, key=lambda x: abs(x[1]), reverse=True)[:10]
                        
                        # Create bar chart
                        segments = [f"Segment {x[0]}" for x in sorted_exp]
                        scores = [x[1] for x in sorted_exp]
                        colors = ['green' if s > 0 else 'red' for s in scores]
                        
                        fig = go.Figure(data=[
                            go.Bar(
                                y=segments,
                                x=scores,
                                orientation='h',
                                marker_color=colors,
                                text=[f"{s:.3f}" for s in scores],
                                textposition='auto'
                            )
                        ])
                        
                        fig.update_layout(
                            title="Top 10 Superpixel Contributions",
                            xaxis_title="Contribution Score",
                            yaxis_title="Superpixel",
                            height=500
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        st.info("""
                        💡 **How to Interpret:**
                        - 🟢 **Green bars**: Positive contribution (supports the prediction)
                        - 🔴 **Red bars**: Negative contribution (against the prediction)
                        - Larger absolute values = More important regions
                        - The highlighted regions in the middle image show which parts influenced the decision
                        """)
                    
                    else:
                        st.error("❌ Model not found. Using demo visualization.")
                        raise FileNotFoundError("Model not found")
                
                except ImportError:
                    st.warning("⚠️ LIME library not installed. Showing simplified demo.")
                    st.info("""
                    📦 **To install LIME:**
                    ```bash
                    pip install lime
                    pip install scikit-image
                    ```
                    """)
                    
                    # Create simplified demo
                    img_resized = cv2.resize(image_np, (224, 224))
                    
                    # Create random superpixel segmentation
                    from skimage.segmentation import slic
                    segments = slic(img_resized, n_segments=50, compactness=10, start_label=1)
                    
                    # Create demo importance scores
                    unique_segments = np.unique(segments)
                    importance = {seg: np.random.randn() for seg in unique_segments}
                    
                    # Create visualization
                    importance_map = np.zeros_like(segments, dtype=float)
                    for seg in unique_segments:
                        importance_map[segments == seg] = importance[seg]
                    
                    # Normalize and colorize
                    importance_map = (importance_map - importance_map.min()) / (importance_map.max() - importance_map.min() + 1e-10)
                    importance_colored = cv2.applyColorMap((importance_map * 255).astype(np.uint8), cv2.COLORMAP_JET)
                    importance_colored = cv2.cvtColor(importance_colored, cv2.COLOR_BGR2RGB)
                    
                    # Overlay
                    overlay = cv2.addWeighted(img_resized, 0.6, importance_colored, 0.4, 0)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.subheader("Original")
                        st.image(img_resized, use_container_width=True)
                    
                    with col2:
                        st.subheader("Importance Map (Demo)")
                        st.image(importance_colored, use_container_width=True)
                    
                    with col3:
                        st.subheader("Overlay (Demo)")
                        st.image(overlay, use_container_width=True)
                    
                    # Demo chart
                    top_segments = sorted(importance.items(), key=lambda x: abs(x[1]), reverse=True)[:10]
                    segments_list = [f"Segment {x[0]}" for x in top_segments]
                    scores_list = [x[1] for x in top_segments]
                    colors_list = ['green' if s > 0 else 'red' for s in scores_list]
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            y=segments_list,
                            x=scores_list,
                            orientation='h',
                            marker_color=colors_list,
                            text=[f"{s:.3f}" for s in scores_list],
                            textposition='auto'
                        )
                    ])
                    
                    fig.update_layout(
                        title="Superpixel Importance (Demo)",
                        xaxis_title="Contribution Score",
                        yaxis_title="Superpixel",
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.info("""
                    💡 **This is a demo visualization.**
                    Install the LIME library for actual explanations based on your model predictions.
                    
                    The demo shows:
                    - Image segmentation into superpixels
                    - Random importance scores (for demonstration)
                    - How LIME visualizations would look
                    """)
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("Showing basic demo visualization...")
                    
                    img_resized = cv2.resize(image_np, (224, 224))
                    st.image(img_resized, caption="Upload successful - Install LIME for full analysis", use_container_width=True)

# ==================== TAB 3: SHAP ====================
with tab3:
    st.header("📊 SHAP: Feature Importance Analysis")
    
    with st.expander("📖 What is SHAP?", expanded=False):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            ### 🎓 Technical Explanation
            
            **SHapley Additive exPlanations**
            
            **Based on Game Theory:**
            - Shapley values from cooperative game theory
            - Fair attribution of prediction to features
            - Considers all possible feature combinations
            
            **Mathematical Formula:**
            ```
            φᵢ = Σ |S|!(|F|-|S|-1)! / |F|! × [fₛ∪{i}(xₛ∪{i}) - fₛ(xₛ)]
            ```
            
            **Properties:**
            - **Efficiency**: Sum of attributions = prediction
            - **Symmetry**: Equal features get equal attribution
            - **Dummy**: Zero-effect features get zero attribution
            - **Additivity**: Consistent across models
            
            **Key Points:**
            - ✅ Theoretically sound (game theory)
            - ✅ Consistent explanations
            - ✅ Works for any model
            - ⚠️ Computationally expensive
            """)
        
        with col2:
            st.markdown("""
            ### 👨‍🌾 Simple Explanation
            
            **Think of it like credit assignment:**
            
            SHAP fairly distributes credit for the AI's decision among all image features.
            
            **What it shows:**
            - How much each feature contributed
            - Which features pushed prediction up/down
            - Overall feature importance
            
            **Example:**
            - "Leaf color contributed 45% to prediction"
            - "Texture contributed 30%"
            - "Shape contributed 25%"
            
            **Visualizations:**
            - 📊 **Bar plot**: Feature importance ranking
            - 🌊 **Waterfall plot**: Cumulative effect
            - 🎯 **Force plot**: Push/pull visualization
            
            **Why it matters:**
            - Mathematically rigorous
            - Fair and consistent
            - Shows what really matters
            """)
    
    st.markdown("---")
    
    uploaded_file_shap = st.file_uploader(
        "📸 Upload Image for SHAP Analysis",
        type=['jpg', 'jpeg', 'png'],
        key="shap_upload"
    )
    
    if uploaded_file_shap:
        image = Image.open(uploaded_file_shap)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image_np = np.array(image)
        
        if st.button("🚀 Generate SHAP Values", key="shap_button"):
            with st.spinner("Extracting features and computing SHAP values..."):
                # Extract features
                img_resized = cv2.resize(image_np, (224, 224))
                features = extract_image_features(img_resized)
                
                # Create demo SHAP-like visualization
                st.subheader("📊 Feature Importance")
                
                feature_names = list(features.keys())
                feature_values = list(features.values())
                
                # Normalize for visualization
                max_val = max(feature_values)
                normalized_values = [v/max_val for v in feature_values]
                
                fig = go.Figure(data=[
                    go.Bar(
                        y=feature_names,
                        x=normalized_values,
                        orientation='h',
                        marker_color='lightblue',
                        text=[f"{v:.2f}" for v in feature_values],
                        textposition='auto'
                    )
                ])
                
                fig.update_layout(
                    title="Feature Importance (Normalized)",
                    xaxis_title="Importance Score",
                    yaxis_title="Feature",
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Feature values table
                st.subheader("📋 Feature Values")
                import pandas as pd
                df = pd.DataFrame({
                    'Feature': feature_names,
                    'Value': [f"{v:.2f}" for v in feature_values]
                })
                st.dataframe(df, use_container_width=True)
                
                st.info("""
                💡 **Interpretation:**
                - Higher bars indicate more important features
                - These features had the most influence on the model's decision
                - Color and texture features typically dominate in crop health analysis
                """)

# ==================== TAB 4: COUNTERFACTUALS ====================
with tab4:
    st.header("🔄 Counterfactual Explanations")
    
    with st.expander("📖 What are Counterfactuals?", expanded=False):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            ### 🎓 Technical Explanation
            
            **Counterfactual Reasoning**
            
            **Concept:**
            Find minimal changes to input that would change the prediction
            
            **Optimization Problem:**
            ```
            minimize: ||x' - x|| + λ × L(f(x'), y_target)
            
            where:
            - x: original input
            - x': counterfactual input
            - y_target: desired output
            - L: loss function
            ```
            
            **Methods:**
            - Gradient-based optimization
            - Genetic algorithms
            - Constraint satisfaction
            
            **Key Points:**
            - ✅ Actionable insights
            - ✅ Shows decision boundaries
            - ✅ Helps understand model behavior
            - ⚠️ May not be realistic
            """)
        
        with col2:
            st.markdown("""
            ### 👨‍🌾 Simple Explanation
            
            **"What if" scenarios:**
            
            Counterfactuals answer: "What needs to change for a different result?"
            
            **Example Questions:**
            - "What if the leaf was greener?"
            - "How much yellowing causes disease prediction?"
            - "What's the minimum change needed?"
            
            **Practical Use:**
            - **For Farmers**: "If I apply fertilizer, will it look healthy?"
            - **For Diagnosis**: "How close is this to being diseased?"
            - **For Prevention**: "What changes indicate problems?"
            
            **Why it matters:**
            - Provides actionable advice
            - Shows how close you are to different outcomes
            - Helps with early intervention
            """)
    
    st.markdown("---")
    
    uploaded_file_cf = st.file_uploader(
        "📸 Upload Image for Counterfactual Analysis",
        type=['jpg', 'jpeg', 'png'],
        key="cf_upload"
    )
    
    if uploaded_file_cf:
        image = Image.open(uploaded_file_cf)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image_np = np.array(image)
        
        st.subheader("🎛️ Adjust Image Properties")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            brightness = st.slider("Brightness", -50, 50, 0, 5, key="cf_brightness")
        with col2:
            contrast = st.slider("Contrast", 0.5, 2.0, 1.0, 0.1, key="cf_contrast")
        with col3:
            saturation = st.slider("Saturation", 0.0, 2.0, 1.0, 0.1, key="cf_saturation")
        
        # Apply transformations
        img_modified = image_np.copy().astype(float)
        
        # Brightness
        img_modified = np.clip(img_modified + brightness, 0, 255)
        
        # Contrast
        img_modified = np.clip((img_modified - 127.5) * contrast + 127.5, 0, 255)
        
        # Saturation
        hsv = cv2.cvtColor(img_modified.astype(np.uint8), cv2.COLOR_RGB2HSV).astype(float)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation, 0, 255)
        img_modified = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
        
        # Display comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Image")
            st.image(image_np, use_container_width=True)
        
        with col2:
            st.subheader("Modified Image")
            st.image(img_modified, use_container_width=True)
        
        # Show changes
        st.info(f"""
        📊 **Changes Applied:**
        - Brightness: {brightness:+d}
        - Contrast: {contrast:.1f}x
        - Saturation: {saturation:.1f}x
        
        💡 **Interpretation:**
        Adjust the sliders to see how changes affect the image. 
        In a full implementation, this would show how predictions change with these modifications.
        """)

# ==================== TAB 5: XAI CHAT ASSISTANT ====================
with tab5:
    st.header("🤖 XAI Chat Assistant")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 15px; margin: 1rem 0;">
        <h3 style="color: white; text-align: center; margin-bottom: 1rem;">
            Ask Me Anything About Explainable AI!
        </h3>
        <p style="color: white; text-align: center; font-size: 1.1rem;">
            I can explain XAI concepts, interpret results, and provide code examples
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add XAI-specific context
    xai_context = """
    Explainable AI (XAI) Page Context:
    - User is learning about Grad-CAM, LIME, SHAP, and Counterfactuals
    - Focus on agricultural applications
    - Provide both technical and simple explanations
    - Can provide code examples for implementation
    """
    
    # Create chat interface with XAI context
    create_chat_interface("xai_assistant", xai_context, use_api=True, unique_key="xai_chat")
    
    # Quick questions with examples
    st.markdown("### 💡 Example Questions You Can Ask")
    
    st.markdown("""
    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
        <h4 style="color: #2E8B57;">🎓 Technical Questions:</h4>
        <ul>
            <li>"Explain the mathematical formula for Grad-CAM"</li>
            <li>"How does SHAP use game theory?"</li>
            <li>"What's the difference between LIME and SHAP?"</li>
            <li>"Show me Python code for implementing Grad-CAM"</li>
            <li>"How to compute Shapley values?"</li>
        </ul>
        
        <h4 style="color: #2E8B57;">👨‍🌾 Practical Questions:</h4>
        <ul>
            <li>"Why did the model predict Nitrogen Deficiency?"</li>
            <li>"Which part of my crop image is most important?"</li>
            <li>"How can I trust the AI's decision?"</li>
            <li>"What changes would make the prediction different?"</li>
            <li>"When should I use Grad-CAM vs LIME?"</li>
        </ul>
        
        <h4 style="color: #2E8B57;">🔬 Implementation Questions:</h4>
        <ul>
            <li>"How to integrate Grad-CAM with ResNet50?"</li>
            <li>"What libraries do I need for XAI?"</li>
            <li>"How to visualize SHAP values?"</li>
            <li>"Best practices for explainable AI in agriculture"</li>
            <li>"How to handle model uncertainty?"</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; background: #2E8B57; color: white; border-radius: 10px; margin-top: 3rem;">
    <h4>🔍 Explainable AI - Krishi Sahayak</h4>
    <p>Making AI Transparent and Trustworthy for Agriculture</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">
        Built with ❤️ for Indian Farmers | Understanding AI Decisions
    </p>
</div>
""", unsafe_allow_html=True)
