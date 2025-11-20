"""
XAI Utilities for Explainable AI
Provides Grad-CAM, LIME, SHAP implementations for agricultural models
"""

import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image
import streamlit as st

def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    """
    Generate Grad-CAM heatmap for a given image and model
    
    Args:
        img_array: Preprocessed image array (1, H, W, 3)
        model: Keras model
        last_conv_layer_name: Name of last convolutional layer
        pred_index: Index of class to visualize (None = predicted class)
    
    Returns:
        heatmap: Grad-CAM heatmap (H, W)
    """
    # Create a model that maps input to activations and output
    grad_model = Model(
        inputs=[model.inputs],
        outputs=[model.get_layer(last_conv_layer_name).output, model.output]
    )
    
    # Compute gradient of top predicted class
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(predictions[0])
        class_channel = predictions[:, pred_index]
    
    # Gradient of output with respect to conv layer
    grads = tape.gradient(class_channel, conv_outputs)
    
    # Mean intensity of gradient over specific feature map channel
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    
    # Multiply each channel by importance
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    
    # Normalize heatmap
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()


def create_gradcam_overlay(img, heatmap, alpha=0.4, colormap=cv2.COLORMAP_JET):
    """
    Create overlay of Grad-CAM heatmap on original image
    
    Args:
        img: Original image (H, W, 3)
        heatmap: Grad-CAM heatmap (H, W)
        alpha: Transparency of overlay
        colormap: OpenCV colormap
    
    Returns:
        overlay: Image with heatmap overlay
    """
    # Resize heatmap to match image size
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    
    # Convert heatmap to RGB
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, colormap)
    
    # Convert BGR to RGB
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
    
    # Ensure img is uint8
    if img.dtype != np.uint8:
        img = np.uint8(255 * img)
    
    # Create overlay
    overlay = cv2.addWeighted(img, 1 - alpha, heatmap, alpha, 0)
    
    return overlay, heatmap


def get_region_importance_scores(heatmap, num_regions=5):
    """
    Extract top N most important regions from heatmap
    
    Args:
        heatmap: Grad-CAM heatmap (H, W)
        num_regions: Number of top regions to extract
    
    Returns:
        regions: List of (x, y, w, h, score) tuples
    """
    # Threshold heatmap
    threshold = np.percentile(heatmap, 90)
    binary_map = (heatmap > threshold).astype(np.uint8)
    
    # Find contours
    contours, _ = cv2.findContours(binary_map, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Extract regions with scores
    regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        region_score = np.mean(heatmap[y:y+h, x:x+w])
        regions.append({
            'bbox': (x, y, w, h),
            'score': float(region_score),
            'area': w * h
        })
    
    # Sort by score and return top N
    regions = sorted(regions, key=lambda x: x['score'], reverse=True)[:num_regions]
    
    return regions


def generate_lime_explanation(image, model, num_samples=1000, num_features=10):
    """
    Generate LIME explanation for image classification
    
    Args:
        image: Input image (H, W, 3)
        model: Prediction model
        num_samples: Number of perturbed samples
        num_features: Number of superpixels
    
    Returns:
        explanation: LIME explanation object
    """
    try:
        from lime import lime_image
        from skimage.segmentation import mark_boundaries
        
        # Create LIME explainer
        explainer = lime_image.LimeImageExplainer()
        
        # Define prediction function
        def predict_fn(images):
            # Preprocess images
            processed = []
            for img in images:
                img_resized = cv2.resize(img, (224, 224))
                img_normalized = img_resized / 255.0
                processed.append(img_normalized)
            
            processed = np.array(processed)
            predictions = model.predict(processed, verbose=0)
            return predictions
        
        # Generate explanation
        explanation = explainer.explain_instance(
            image,
            predict_fn,
            top_labels=5,
            hide_color=0,
            num_samples=num_samples,
            segmentation_fn=None
        )
        
        return explanation
    
    except ImportError:
        st.error("LIME library not installed. Install with: pip install lime")
        return None


def generate_shap_values(image, model, background_samples=50):
    """
    Generate SHAP values for image
    
    Args:
        image: Input image (H, W, 3)
        model: Prediction model
        background_samples: Number of background samples
    
    Returns:
        shap_values: SHAP values array
    """
    try:
        import shap
        
        # Create background dataset (simplified)
        background = np.random.rand(background_samples, 224, 224, 3)
        
        # Create explainer
        explainer = shap.DeepExplainer(model, background)
        
        # Compute SHAP values
        img_expanded = np.expand_dims(image, axis=0)
        shap_values = explainer.shap_values(img_expanded)
        
        return shap_values
    
    except ImportError:
        st.error("SHAP library not installed. Install with: pip install shap")
        return None


def extract_image_features(image):
    """
    Extract interpretable features from image
    
    Args:
        image: Input image (H, W, 3)
    
    Returns:
        features: Dictionary of feature values
    """
    # Convert to different color spaces
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    
    # Color features
    mean_rgb = np.mean(image, axis=(0, 1))
    std_rgb = np.std(image, axis=(0, 1))
    mean_hsv = np.mean(hsv, axis=(0, 1))
    
    # Texture features (simplified)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(edges > 0) / edges.size
    
    # Compute gradient magnitude
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    texture_strength = np.mean(np.sqrt(gx**2 + gy**2))
    
    features = {
        'Mean Red': float(mean_rgb[0]),
        'Mean Green': float(mean_rgb[1]),
        'Mean Blue': float(mean_rgb[2]),
        'Std Red': float(std_rgb[0]),
        'Std Green': float(std_rgb[1]),
        'Std Blue': float(std_rgb[2]),
        'Mean Hue': float(mean_hsv[0]),
        'Mean Saturation': float(mean_hsv[1]),
        'Mean Value': float(mean_hsv[2]),
        'Edge Density': float(edge_density),
        'Texture Strength': float(texture_strength)
    }
    
    return features


def create_counterfactual(image, model, target_class, max_iterations=100, learning_rate=1.0):
    """
    Generate counterfactual explanation
    
    Args:
        image: Original image
        model: Prediction model
        target_class: Desired target class
        max_iterations: Maximum optimization iterations
        learning_rate: Step size for optimization
    
    Returns:
        counterfactual_image: Modified image
        changes: Dictionary of changes made
    """
    # Convert to tensor
    img_tensor = tf.Variable(image, dtype=tf.float32)
    
    # Optimization loop
    for i in range(max_iterations):
        with tf.GradientTape() as tape:
            predictions = model(tf.expand_dims(img_tensor, 0))
            loss = -predictions[0, target_class]  # Maximize target class probability
        
        # Compute gradients
        gradients = tape.gradient(loss, img_tensor)
        
        # Update image
        img_tensor.assign_add(learning_rate * tf.sign(gradients))
        
        # Clip to valid range
        img_tensor.assign(tf.clip_by_value(img_tensor, 0, 1))
        
        # Check if target reached
        current_pred = model(tf.expand_dims(img_tensor, 0))
        if tf.argmax(current_pred[0]) == target_class:
            break
    
    counterfactual_image = img_tensor.numpy()
    
    # Calculate changes
    changes = {
        'brightness_change': float(np.mean(counterfactual_image) - np.mean(image)),
        'color_shift': float(np.linalg.norm(np.mean(counterfactual_image, axis=(0,1)) - np.mean(image, axis=(0,1)))),
        'total_change': float(np.mean(np.abs(counterfactual_image - image)))
    }
    
    return counterfactual_image, changes


def get_last_conv_layer_name(model):
    """
    Automatically detect last convolutional layer name
    
    Args:
        model: Keras model
    
    Returns:
        layer_name: Name of last conv layer
    """
    for layer in reversed(model.layers):
        if 'conv' in layer.name.lower():
            return layer.name
    
    # Fallback
    return model.layers[-4].name


def visualize_attention_regions(image, regions, title="Attention Regions"):
    """
    Visualize bounding boxes of important regions
    
    Args:
        image: Original image
        regions: List of region dictionaries
        title: Plot title
    
    Returns:
        fig: Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(image)
    
    colors = plt.cm.hot(np.linspace(0.3, 1, len(regions)))
    
    for i, region in enumerate(regions):
        x, y, w, h = region['bbox']
        score = region['score']
        
        rect = plt.Rectangle((x, y), w, h, fill=False, 
                            edgecolor=colors[i], linewidth=3)
        ax.add_patch(rect)
        
        ax.text(x, y-5, f"Score: {score:.2f}", 
               bbox=dict(boxstyle='round', facecolor=colors[i], alpha=0.7),
               fontsize=10, color='white', weight='bold')
    
    ax.set_title(title, fontsize=16, weight='bold')
    ax.axis('off')
    
    return fig


def calculate_model_confidence_metrics(predictions):
    """
    Calculate confidence metrics from model predictions
    
    Args:
        predictions: Model prediction probabilities
    
    Returns:
        metrics: Dictionary of confidence metrics
    """
    top_prob = np.max(predictions)
    top_class = np.argmax(predictions)
    
    # Entropy (uncertainty measure)
    entropy = -np.sum(predictions * np.log(predictions + 1e-10))
    max_entropy = -np.log(1.0 / len(predictions))
    normalized_entropy = entropy / max_entropy
    
    # Margin (difference between top 2 predictions)
    sorted_probs = np.sort(predictions)[::-1]
    margin = sorted_probs[0] - sorted_probs[1] if len(sorted_probs) > 1 else sorted_probs[0]
    
    metrics = {
        'top_probability': float(top_prob),
        'top_class': int(top_class),
        'entropy': float(entropy),
        'normalized_entropy': float(normalized_entropy),
        'margin': float(margin),
        'confidence_level': 'High' if top_prob > 0.8 else 'Medium' if top_prob > 0.6 else 'Low'
    }
    
    return metrics
