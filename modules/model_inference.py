import os
import requests
import json
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import cv2

from config import GROQ_API_KEY, MODEL_CONFIGS
from modules import preprocessing

def _encode_image_to_base64(image_data):
    """Encodes an image (np.array or PIL.Image) into a base64 string."""
    if isinstance(image_data, np.ndarray):
        is_success, buffer = cv2.imencode(".jpg", image_data)
        if not is_success:
            return None
        image_data = BytesIO(buffer)
    elif isinstance(image_data, Image.Image):
        buffer = BytesIO()
        image_data.save(buffer, format="JPEG")
        image_data = buffer
    
    encoded_string = base64.b64encode(image_data.getvalue()).decode('utf-8')
    return encoded_string

def _simulate_classification_inference(image, sector_name):
    """
    Simulates a classification API call for Crop Health.
    In a real project, this would send a request to a Groq-hosted model.
    """
    labels = ["Healthy", "Nitrogen Deficiency", "Potassium Deficiency"]
    confidence = np.random.uniform(0.75, 0.99)
    predicted_label = np.random.choice(labels)
    
    return {"prediction": predicted_label, "confidence": confidence}

def _simulate_yolo_inference(image):
    """
    Simulates a YOLOv8 object detection API call for Pest Detection.
    Returns a list of dictionaries with bounding boxes and labels.
    """
    detected_pests = []
    labels = ["Aphids", "Whitefly", "Spider Mites", "Mealybugs"]
    num_detections = np.random.randint(0, 3)
    
    img_height, img_width, _ = image.shape
    
    for _ in range(num_detections):
        # Generate random bounding box coordinates
        x_min = np.random.randint(0, int(img_width * 0.8))
        y_min = np.random.randint(0, int(img_height * 0.8))
        width = np.random.randint(50, img_width - x_min)
        height = np.random.randint(50, img_height - y_min)
        
        detected_pests.append({
            "box": [x_min, y_min, x_min + width, y_min + height],
            "label": np.random.choice(labels),
            "confidence": np.random.uniform(0.8, 0.95)
        })
    return {"detections": detected_pests}

def _simulate_segmentation_inference(image):
    """
    Simulates a U-Net segmentation API call for Weed Detection.
    Returns a binary mask.
    """
    # Create a dummy mask with some random shapes to simulate weed patches
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    h, w = mask.shape
    
    num_patches = np.random.randint(1, 4)
    for _ in range(num_patches):
        center_x, center_y = np.random.randint(w), np.random.randint(h)
        size = np.random.randint(50, 200)
        cv2.circle(mask, (center_x, center_y), size, 255, -1)
    
    return {"mask": mask}

def run_inference(image, sector_name):
    """
    Selects the correct inference method based on the sector name.
    
    Args:
        image (np.array): The preprocessed image.
        sector_name (str): The name of the agricultural sector.
        
    Returns:
        dict: The prediction results (labels, bounding boxes, or masks).
    """
    task_type = MODEL_CONFIGS[sector_name]['task']
    
    if task_type == 'classification':
        return _simulate_classification_inference(image, sector_name)
    elif task_type == 'object_detection':
        return _simulate_yolo_inference(image)
    elif task_type == 'segmentation':
        return _simulate_segmentation_inference(image)
    elif task_type == 'analysis':
        # For irrigation, the "inference" is the NDVI calculation itself
        ndvi_image = preprocessing.get_ndvi(image)
        return {"ndvi": ndvi_image}

if __name__ == '__main__':
    print("--- Testing Model Inference Module ---")
    
    # Simulate an uploaded image
    dummy_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
    
    # Test Crop Health inference
    print("\nSimulating Crop Health inference...")
    result = run_inference(dummy_image, "crop_health")
    print(f"Prediction: {result['prediction']}, Confidence: {result['confidence']:.2f}")
    
    # Test Pest Detection inference
    print("\nSimulating Pest Detection inference...")
    result = run_inference(dummy_image, "pest_detection")
    print(f"Detections: {len(result['detections'])}")
    for det in result['detections']:
        print(f" - Label: {det['label']}, Box: {det['box']}")
        
    # Test Weed Detection inference
    print("\nSimulating Weed Detection inference...")
    result = run_inference(dummy_image, "weed_detection")
    print(f"Mask shape: {result['mask'].shape}")
    
    # Test Irrigation Management inference
    print("\nSimulating Irrigation Management inference...")
    # This requires a multispectral image. Using a dummy placeholder.
    dummy_ndvi_image = np.random.randint(0, 255, (640, 640, 4), dtype=np.uint8)
    result = run_inference(dummy_ndvi_image, "irrigation_management")
    print(f"NDVI map generated with shape: {result['ndvi'].shape}")
    
    
    

# Explanation
# This file is the core backend logic for running AI inference. 
# It contains functions that simulate API calls to pre-trained models for each sector, providing structured output like predicted labels, bounding box coordinates, or segmentation masks. 
# While Groq primarily handles LLMs, we are simulating the computer vision model inference to demonstrate a complete system. This allows the Streamlit frontend to receive and visualize results as if a real API endpoint were in use, making the project's pipeline fully functional.