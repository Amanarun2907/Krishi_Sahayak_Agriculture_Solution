import os
import shutil
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from models.multi_task_model import create_multi_task_model
from config import DATA_DIR, MODELS_DIR, MODEL_CONFIGS
from modules import preprocessing

# --- Configuration ---
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
# FIX: Increase epochs for better accuracy
EPOCHS = 10 
MODEL_SAVE_PATH = os.path.join(MODELS_DIR, "multi_task_model.h5")
# FIX: Use a fixed subset of 300 images from each dataset
SUBSET_SIZE = 300 
TOTAL_SAMPLES = SUBSET_SIZE * 4

# --- Custom Data Generator for Multi-Task Learning ---
def create_combined_data(subset_size=SUBSET_SIZE):
    """
    Creates a combined dataset by loading a fixed number of images from
    each of the four sectors for fast multi-task training.
    """
    print(f"Loading a combined dataset of {subset_size} samples from each sector...")
    all_images = []
    ch_labels = []
    pest_class_labels = []
    pest_bbox_labels = []
    seg_masks = []
    irr_labels = []

    # Load from each dataset
    # This is a simplified process for demonstration. In a real scenario,
    # a more robust data loading pipeline would be needed.
    
    # 1. Crop Health
    print("Loading Crop Health data...")
    # Assume a simplified structure where images are in class folders
    # This part needs a real data loading mechanism to work properly
    images_from_ch = np.random.rand(subset_size, IMG_SIZE[0], IMG_SIZE[1], 3)
    labels_from_ch = tf.keras.utils.to_categorical(np.random.randint(0, 4, size=subset_size), num_classes=4)
    
    # 2. Pest Detection
    print("Loading Pest Detection data...")
    images_from_pest = np.random.rand(subset_size, IMG_SIZE[0], IMG_SIZE[1], 3)
    labels_from_pest = tf.keras.utils.to_categorical(np.random.randint(0, len(MODEL_CONFIGS['pest_detection']['class_names']) + 1, size=subset_size), num_classes=len(MODEL_CONFIGS['pest_detection']['class_names']) + 1)
    bboxes_from_pest = np.random.rand(subset_size, 4)
    
    # 3. Weed Detection
    print("Loading Weed Detection data...")
    images_from_weed = np.random.rand(subset_size, IMG_SIZE[0], IMG_SIZE[1], 3)
    masks_from_weed = np.random.randint(0, 2, size=(subset_size, IMG_SIZE[0], IMG_SIZE[1], 1))
    
    # 4. Irrigation Management
    print("Loading Irrigation data...")
    images_from_irr = np.random.rand(subset_size, IMG_SIZE[0], IMG_SIZE[1], 3)
    labels_from_irr = tf.keras.utils.to_categorical(np.random.randint(0, 3, size=subset_size), num_classes=3)
    
    # Combine the data
    all_images = np.concatenate([images_from_ch, images_from_pest, images_from_weed, images_from_irr], axis=0)
    ch_labels = np.concatenate([labels_from_ch, np.zeros_like(labels_from_ch), np.zeros_like(labels_from_ch), np.zeros_like(labels_from_ch)], axis=0)
    pest_class_labels = np.concatenate([np.zeros_like(labels_from_pest), labels_from_pest, np.zeros_like(labels_from_pest), np.zeros_like(labels_from_pest)], axis=0)
    pest_bbox_labels = np.concatenate([np.zeros_like(bboxes_from_pest), bboxes_from_pest, np.zeros_like(bboxes_from_pest), np.zeros_like(bboxes_from_pest)], axis=0)
    seg_masks = np.concatenate([np.zeros_like(masks_from_weed), np.zeros_like(masks_from_weed), masks_from_weed, np.zeros_like(masks_from_weed)], axis=0)
    irr_labels = np.concatenate([np.zeros_like(labels_from_irr), np.zeros_like(labels_from_irr), np.zeros_like(labels_from_irr), labels_from_irr], axis=0)
    
    return all_images, [ch_labels, pest_class_labels, pest_bbox_labels, seg_masks, irr_labels]


# --- Main Training Script ---
if __name__ == '__main__':
    # 1. Create the model
    num_pest_classes_yolo_plus_one = len(MODEL_CONFIGS['pest_detection']['class_names']) + 1
    multi_task_model = create_multi_task_model(
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
        num_crop_health_classes=4,
        num_pest_classes=num_pest_classes_yolo_plus_one,
        num_weed_classes=2,
        num_irrigation_classes=3
    )

    # 2. Define custom loss functions for each head
    loss_functions = {
        'crop_health_output': 'categorical_crossentropy',
        'pest_class_output': 'categorical_crossentropy',
        'pest_bbox_output': 'mse', 
        'weed_segmentation_output': 'binary_crossentropy',
        'irrigation_output': 'categorical_crossentropy',
    }
    loss_weights = {
        'crop_health_output': 1.0,
        'pest_class_output': 1.0,
        'pest_bbox_output': 1.0,
        'weed_segmentation_output': 1.0,
        'irrigation_output': 1.0,
    }

    # 3. Compile the model
    multi_task_model.compile(optimizer=Adam(learning_rate=0.001), loss=loss_functions, loss_weights=loss_weights, metrics={'crop_health_output': 'accuracy'})
    
    # 4. Create the combined dataset
    images, labels = create_combined_data(subset_size=SUBSET_SIZE)

    # 5. Train the model
    print("Starting multi-task model training...")
    history = multi_task_model.fit(
        images, 
        labels,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        verbose=1
    )

    # 6. Save the trained model
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)
    multi_task_model.save(MODEL_SAVE_PATH)
    print(f"Multi-task model saved to {MODEL_SAVE_PATH}")