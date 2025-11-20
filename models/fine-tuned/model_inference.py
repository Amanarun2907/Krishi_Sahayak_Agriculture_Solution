import os
import numpy as np
import cv2
import tensorflow as tf
from ultralytics import YOLO
from config import MODEL_CONFIGS, MODELS_DIR
from modules import preprocessing

def run_classification_inference(image, sector_name):
    """
    Loads the fine-tuned Keras model and performs classification inference.
    
    Args:
        image (np.array): The preprocessed image.
        sector_name (str): The name of the agricultural sector.
        
    Returns:
        dict: A dictionary of all class predictions and confidence scores.
    """
    model_path = os.path.join(MODELS_DIR, "crop_health_model.h5")
    
    try:
        model = tf.keras.models.load_model(model_path)
    except Exception as e:
        return {"error": f"Failed to load crop health model: {e}"}
        
    img_tensor = np.expand_dims(image, axis=0)
    predictions = model.predict(img_tensor, verbose=0)[0]
    
    class_names = MODEL_CONFIGS[sector_name]['class_names']
    
    confidence_scores = {class_names[i]: float(predictions[i]) for i in range(len(class_names))}
    
    top_prediction = max(confidence_scores, key=confidence_scores.get)
    top_confidence = confidence_scores[top_prediction]
    
    return {
        "prediction": top_prediction,
        "confidence": top_confidence,
        "all_confidences": confidence_scores
    }

def run_yolo_inference(image):
    """
    Loads the fine-tuned YOLOv8 model and performs object detection inference.
    
    Args:
        image (np.array): The preprocessed image.
        
    Returns:
        dict: A dictionary with detections, count, and severity.
    """
    model_path = os.path.join(MODELS_DIR, "pest_detection_model.pt")
    
    try:
        if not os.path.exists(model_path):
            return _simulate_yolo_inference(image)
        model = YOLO(model_path)
    except Exception as e:
        return {"error": f"Failed to load pest detection model: {e}"}

    results = model(image, verbose=False)
    
    detections = []
    pest_count = 0
    detected_pest_types = set()
    
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        class_ids = result.boxes.cls.cpu().numpy()
        
        for box, conf, cls_id in zip(boxes, confidences, class_ids):
            label = result.names[int(cls_id)]
            detections.append({
                "box": box.tolist(),
                "label": label,
                "confidence": float(conf)
            })
            pest_count += 1
            detected_pest_types.add(label)
    
    if pest_count == 0:
        severity = "No Infestation"
    elif pest_count <= 5:
        severity = "Low Infestation"
    elif pest_count <= 20:
        severity = "Moderate Infestation"
    else:
        severity = "High Infestation"
        
    return {
        "detections": detections,
        "pest_count": pest_count,
        "severity": severity,
        "pest_types": list(detected_pest_types)
    }

def _simulate_yolo_inference(image):
    """Simulates a YOLOv8 object detection inference call."""
    detected_pests = []
    labels = MODEL_CONFIGS['pest_detection']['class_names']
    num_detections = np.random.randint(0, 3)
    
    img_height, img_width, _ = image.shape
    
    for _ in range(num_detections):
        x_min = np.random.randint(0, int(img_width * 0.8))
        y_min = np.random.randint(0, int(img_height * 0.8))
        width = np.random.randint(50, img_width - x_min)
        height = np.random.randint(50, img_height - y_min)
        
        detected_pests.append({
            "box": [x_min, y_min, x_min + width, y_min + height],
            "label": np.random.choice(labels),
            "confidence": np.random.uniform(0.8, 0.95)
        })
    return {
        "detections": detected_pests,
        "pest_count": len(detected_pests),
        "severity": "Low Infestation" if len(detected_pests) > 0 else "No Infestation",
        "pest_types": list(set([d['label'] for d in detected_pests]))
    }

def _simulate_segmentation_inference(image):
    """
    Simulates a U-Net segmentation API call for Weed Detection.
    Returns a binary mask.
    """
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    h, w = mask.shape
    
    num_patches = np.random.randint(1, 4)
    for _ in range(num_patches):
        center_x, center_y = np.random.randint(w), np.random.randint(h)
        size = np.random.randint(50, 200)
        cv2.circle(mask, (center_x, center_y), size, 255, -1)
    
    return {"mask": mask}

def run_multi_task_inference(image):
    """
    Runs inference on the multi-task model and returns all four predictions.
    
    Args:
        image (np.array): The preprocessed image.
        
    Returns:
        dict: A dictionary containing predictions for all four tasks.
    """
    model_path = os.path.join(MODELS_DIR, "multi_task_model.h5")
    
    try:
        model = tf.keras.models.load_model(model_path, compile=False)
    except Exception as e:
        return {"error": f"Failed to load multi-task model. Details: {e}"}
        
    # The model expects a batch dimension
    input_tensor = np.expand_dims(image, axis=0)
    
    # Get all four predictions from the multi-head model
    ch_pred, pest_class_pred, pest_bbox_pred, seg_pred, irr_pred = model.predict(input_tensor)
    
    # Process Crop Health Prediction
    ch_class_names = MODEL_CONFIGS['unified_model']['crop_health_classes']
    ch_confidences = {ch_class_names[i]: float(ch_pred[0][i]) for i in range(len(ch_class_names))}
    ch_top_pred = max(ch_confidences, key=ch_confidences.get)
    
    # Process Pest Detection Prediction (simplified)
    pest_class_names = MODEL_CONFIGS['unified_model']['pest_classes']
    pest_top_pred_id = np.argmax(pest_class_pred[0])
    pest_top_pred_label = pest_class_names[pest_top_pred_id]
    pest_bbox_coords = pest_bbox_pred[0].tolist()
    
    # Process Weed Segmentation Prediction
    weed_mask = (seg_pred[0, :, :, 0] > 0.5).astype(np.uint8) * 255
    
    # Process Irrigation Stress Prediction
    irr_class_names = MODEL_CONFIGS['unified_model']['irrigation_classes']
    irr_top_pred_id = np.argmax(irr_pred[0])
    irr_top_pred_label = irr_class_names[irr_top_pred_id]
    
    return {
        "crop_health": {"prediction": ch_top_pred, "all_confidences": ch_confidences},
        "pest_detection": {"label": pest_top_pred_label, "bbox": pest_bbox_coords},
        "weed_detection": {"mask": weed_mask},
        "irrigation_management": {"prediction": irr_top_pred_label},
    }

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
        return run_classification_inference(image, sector_name)
    elif task_type == 'object_detection':
        return run_yolo_inference(image)
    elif task_type == 'segmentation':
        return _simulate_segmentation_inference(image)
    elif task_type == 'analysis':
        ndvi_image = preprocessing.get_ndvi(image)
        return {"ndvi": ndvi_image}