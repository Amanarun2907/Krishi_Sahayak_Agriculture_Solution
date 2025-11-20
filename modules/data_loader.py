import os
import glob
import pandas as pd
from PIL import Image
from modules import preprocessing
from config import DATA_DIR, MODEL_CONFIGS

def load_data(sector_name):
    """
    Loads and organizes the dataset for a specific agricultural sector based on the project configuration.
    
    Args:
        sector_name (str): The name of the agricultural sector (e.g., 'crop_health').
        
    Returns:
        list: A list of image paths and corresponding labels/annotations.
        str: The task type (e.g., 'classification', 'segmentation').
    """
    config = MODEL_CONFIGS[sector_name]
    dataset_path = os.path.join(DATA_DIR, config['dataset_name'])
    task_type = config['task']

    data = []

    if sector_name == "crop_health":
        # Handle Longitudinal_Nutrient_Deficiency dataset
        # Assumes a CSV file contains the labels for each field and image
        labels_file = os.path.join(dataset_path, "LongitudinalNutrientDeficiency.csv")
        df = pd.read_csv(labels_file)
        
        # Iterate through fields and images based on the CSV
        for index, row in df.iterrows():
            image_path = os.path.join(dataset_path, "images", row['image_name'])
            label = row['label']
            data.append({"image": image_path, "label": label})
            
    elif sector_name == "pest_detection":
        # Handle OPA_Pest_DIP_AI dataset
        # Assumes a YOLO-format structure with images and labels folders
        split_dirs = ['train', 'valid', 'pest_test']
        for split in split_dirs:
            image_dir = os.path.join(dataset_path, split, 'images')
            label_dir = os.path.join(dataset_path, split, 'labels')
            
            for image_path in glob.glob(os.path.join(image_dir, '*.jpg')):
                image_name = os.path.basename(image_path)
                label_name = os.path.splitext(image_name)[0] + '.txt'
                label_path = os.path.join(label_dir, label_name)
                
                if os.path.exists(label_path):
                    data.append({"image": image_path, "label": label_path})
    
    elif sector_name == "weed_detection":
        # Handle weed_detection_dataset
        # Assumes a YOLO-format structure with images and labels folders
        split_dirs = ['train', 'valid', 'test']
        for split in split_dirs:
            image_dir = os.path.join(dataset_path, split, 'images')
            label_dir = os.path.join(dataset_path, split, 'labels')
            
            for image_path in glob.glob(os.path.join(image_dir, '*.jpg')):
                image_name = os.path.basename(image_path)
                label_name = os.path.splitext(image_name)[0] + '.txt'
                label_path = os.path.join(label_dir, label_name)
                
                if os.path.exists(label_path):
                    data.append({"image": image_path, "label": label_path})

    elif sector_name == "irrigation_management":
        # Handle Agriculture-Vision-2021 dataset
        # Assumes RGB and mask images are in train, val, test splits
        split_dirs = ['train', 'val', 'test']
        for split in split_dirs:
            image_dir = os.path.join(dataset_path, split, 'images')
            mask_dir = os.path.join(dataset_path, split, 'masks')
            
            for image_path in glob.glob(os.path.join(image_dir, '*.tif')):
                image_name = os.path.basename(image_path)
                mask_path = os.path.join(mask_dir, image_name.replace('.tif', '.png'))
                
                if os.path.exists(mask_path):
                    data.append({"image": image_path, "label": mask_path})
    
    return data, task_type

if __name__ == '__main__':
    # Example usage to demonstrate functionality
    # You can run this file directly to check if data loading works
    print("--- Testing Data Loader ---")
    
    # Test Crop Health
    print("\nLoading Crop Health data...")
    crop_health_data, task = load_data("crop_health")
    print(f"Loaded {len(crop_health_data)} items for '{task}' task.")
    
    # Test Pest Detection
    print("\nLoading Pest Detection data...")
    pest_data, task = load_data("pest_detection")
    print(f"Loaded {len(pest_data)} items for '{task}' task.")
    
    # Test Weed Detection
    print("\nLoading Weed Detection data...")
    weed_data, task = load_data("weed_detection")
    print(f"Loaded {len(weed_data)} items for '{task}' task.")
    
    # Test Irrigation Management
    print("\nLoading Irrigation Management data...")
    irrigation_data, task = load_data("irrigation_management")
    print(f"Loaded {len(irrigation_data)} items for '{task}' task.")
    
    
# Explanation
# This code defines the data_loader.py module. It contains a single main function, load_data(), which is responsible for intelligently navigating the unique file structure of each of the four datasets. 
# It uses the configurations defined in config.py to correctly identify the dataset, read image paths and corresponding labels (whether from .csv files, .txt files, or mask directories), and return a standardized list of data for further processing. 
# This is a crucial step that prepares all the raw data for the subsequent preprocessing and model fine-tuning stages.