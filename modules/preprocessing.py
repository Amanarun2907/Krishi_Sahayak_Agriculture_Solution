import cv2
import numpy as np
from PIL import Image

def calculate_ndvi(nir_band, red_band):
    """
    Calculates the Normalized Difference Vegetation Index (NDVI) from 
    Near-Infrared (NIR) and Red band images.
    
    Args:
        nir_band (np.array): A grayscale image array of the NIR channel.
        red_band (np.array): A grayscale image array of the Red channel.
        
    Returns:
        np.array: A float32 array representing the NDVI values,
                  scaled from -1.0 to 1.0.
    """
    # Convert bands to float for precise calculation
    nir_band = nir_band.astype(float)
    red_band = red_band.astype(float)

    # Prevent division by zero
    denominator = nir_band + red_band
    denominator[denominator == 0] = 1e-6 # Add a small value to avoid errors
    
    ndvi = (nir_band - red_band) / denominator
    
    return ndvi

def colorize_ndvi(ndvi_map):
    """
    Creates a colorized heatmap from an NDVI map.
    
    Args:
        ndvi_map (np.array): The NDVI values array (float32).
        
    Returns:
        np.array: A colorized image (BGR format).
    """
    # Normalize the NDVI values to the 0-255 range
    ndvi_normalized = ((ndvi_map + 1) / 2) * 255
    ndvi_normalized = np.uint8(ndvi_normalized)
    
    # Apply a color map (e.g., JET for a blue-to-red gradient)
    ndvi_colorized = cv2.applyColorMap(ndvi_normalized, cv2.COLORMAP_JET)
    
    return ndvi_colorized

def classify_ndvi_zones(ndvi_map):
    """
    Classifies the field into water stress zones based on NDVI values.
    
    Args:
        ndvi_map (np.array): The float32 array of NDVI values.
        
    Returns:
        dict: A dictionary with the percentage of the field in each zone.
    """
    total_pixels = ndvi_map.size
    
    # Define NDVI ranges for different stress levels
    zones = {
        "Severe Stress (Water Scarcity)": (-1.0, 0.2),
        "Moderate Stress": (0.2, 0.4),
        "Healthy Vegetation": (0.4, 0.7),
        "Over-watered/Dense Vegetation": (0.7, 1.0)
    }
    
    stress_counts = {}
    for zone, (min_val, max_val) in zones.items():
        count = np.sum((ndvi_map >= min_val) & (ndvi_map < max_val))
        stress_counts[zone] = (count / total_pixels) * 100
        
    return stress_counts

def create_segmentation_mask(label_path, image_size=(512, 512)):
    """
    Converts YOLO-format bounding box labels to a binary segmentation mask.
    This is necessary for the Weed Detection U-Net model.
    
    Args:
        label_path (str): Path to the YOLO .txt label file.
        image_size (tuple): The size of the output mask (width, height).
        
    Returns:
        np.array: A binary segmentation mask.
    """
    mask = np.zeros(image_size, dtype=np.uint8)
    
    try:
        with open(label_path, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            class_id, x_center, y_center, width, height = map(float, line.strip().split())
            
            # Convert from normalized to pixel coordinates
            x1 = int((x_center - width / 2) * image_size[0])
            y1 = int((y_center - height / 2) * image_size[1])
            x2 = int((x_center + width / 2) * image_size[0])
            y2 = int((y_center + height / 2) * image_size[1])
            
            # Draw the bounding box filled on the mask
            cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1) 
            
    except FileNotFoundError:
        print(f"Label file not found: {label_path}. Returning empty mask.")
    except Exception as e:
        print(f"Error processing label file: {e}. Returning empty mask.")

    return mask

def preprocess_image(image, task_type):
    """
    Applies a standard DIP pipeline to a single image based on the task type.
    
    Args:
        image (PIL.Image.Image or np.array): The image to preprocess.
        task_type (str): The type of task ('classification', 'object_detection', 'segmentation').
        
    Returns:
        np.array: The preprocessed image ready for model inference.
    """
    if isinstance(image, Image.Image):
        image = np.array(image.convert("RGB"))

    # Noise Removal (Gaussian Filter)
    preprocessed_img = cv2.GaussianBlur(image, (5, 5), 0)

    # Normalization (Standardize brightness/contrast)
    preprocessed_img = cv2.normalize(preprocessed_img, None, 0, 255, cv2.NORM_MINMAX)

    if task_type == 'classification':
        preprocessed_img = cv2.resize(preprocessed_img, (224, 224))
    elif task_type == 'object_detection':
        preprocessed_img = cv2.resize(preprocessed_img, (640, 640))
    elif task_type == 'segmentation':
        preprocessed_img = cv2.resize(preprocessed_img, (512, 512))

    return preprocessed_img

if __name__ == '__main__':
    # This block is for testing the functions directly
    print("--- Testing Preprocessing Module ---")
    
    # Simulate a multispectral image for NDVI
    # Create dummy NIR and Red bands
    dummy_nir = np.random.randint(50, 200, (256, 256), dtype=np.uint8)
    dummy_red = np.random.randint(30, 150, (256, 256), dtype=np.uint8)
    
    # Calculate and colorize NDVI
    ndvi_map = calculate_ndvi(dummy_nir, dummy_red)
    ndvi_colorized = colorize_ndvi(ndvi_map)
    
    print(f"\nNDVI map calculated with shape: {ndvi_map.shape}")
    print(f"NDVI heatmap created with shape: {ndvi_colorized.shape}")
    
    # Classify stress zones
    stress_zones = classify_ndvi_zones(ndvi_map)
    print("\nSimulated Stress Zones:")
    for zone, percent in stress_zones.items():
        print(f"- {zone}: {percent:.2f}%")
        
    # Simulate a single-band image for other tasks
    dummy_rgb_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
    
    # Test for Crop Health (Classification)
    preprocessed_health = preprocess_image(dummy_rgb_image, 'classification')
    print(f"\nClassification image preprocessed to shape: {preprocessed_health.shape}")

    # Test for Pest Detection (Object Detection)
    preprocessed_pest = preprocess_image(dummy_rgb_image, 'object_detection')
    print(f"Object Detection image preprocessed to shape: {preprocessed_pest.shape}")

    # Test for Weed Detection (Segmentation)
    preprocessed_weed = preprocess_image(dummy_rgb_image, 'segmentation')
    print(f"Segmentation image preprocessed to shape: {preprocessed_weed.shape}")