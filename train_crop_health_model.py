import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
import os
import shutil
import glob
from config import DATA_DIR, MODELS_DIR, MODEL_CONFIGS

# --- Configuration ---
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 5
SECTOR_NAME = "crop_health"
DATASET_NAME = MODEL_CONFIGS[SECTOR_NAME]["dataset_name"]
DATASET_ROOT = os.path.join(DATA_DIR, DATASET_NAME, "Longitudinal_Nutrient_Deficiency")
MODEL_SAVE_PATH = os.path.join(MODELS_DIR, "crop_health_model.h5")

# --- Function to Prepare Data Structure (Crucial for this dataset) ---
def organize_dataset_for_generator(source_root, temp_dir):
    """
    Creates a temporary, class-labeled directory structure required by 
    ImageDataGenerator from the complex field_XXX structure.
    
    NOTE: This is a simplification. In a real scenario, you would need 
    an annotation CSV inside Longitudinal_Nutrient_Deficiency to map 
    image files to their nutrient class (e.g., 'Healthy', 'N_Deficient').
    
    We simulate a simple scenario here where sub-images inside field_XXX 
    are assumed to be class-labeled: field_XXX/Healthy/*.jpg.
    """
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    os.makedirs(temp_dir, exist_ok=True)
    
    field_dirs = glob.glob(os.path.join(source_root, 'field_*'))
    
    # We define assumed classes based on typical nutrient deficiency datasets
    # In a real setup, these classes are read from an annotation file
    assumed_classes = ["Healthy", "Nitrogen_Deficient", "Potassium_Deficient", "General_Stress"]
    
    for cls in assumed_classes:
        os.makedirs(os.path.join(temp_dir, 'train', cls), exist_ok=True)
        os.makedirs(os.path.join(temp_dir, 'validation', cls), exist_ok=True)
    
    # Simulate moving/linking images from field_XXX into class folders
    # This loop is placeholder logic, demonstrating the necessary file organization step
    print("Simulating dataset organization for Keras generator...")
    
    for i, field_dir in enumerate(field_dirs):
        # Placeholder: Assume a distribution of classes within each field for simulation
        
        # Determine split (80% train, 20% validation)
        split_folder = 'train' if i % 5 != 0 else 'validation'
        
        for cls in assumed_classes:
            # Create a dummy file path to simulate image files being present
            dummy_file = os.path.join(field_dir, f"sample_{cls}_{i}.jpg")
            
            # Use touch or similar method to create dummy files if running locally,
            # or copy actual images if available.
            # Here, we skip file creation for generality but print status:
            pass # Replace with actual file movement/copy logic in a real run

    print(f"Dataset structure simulated in temporary directory: {temp_dir}")
    return os.path.join(temp_dir, 'train'), os.path.join(temp_dir, 'validation')

# --- Main Training Script ---

# 1. Prepare Data
TEMP_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_data_crop_health")
train_dir, validation_dir = organize_dataset_for_generator(DATASET_ROOT, TEMP_DATA_DIR)

# 2. Setup Data Generators
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# 3. Build Model (Transfer Learning)
# Load the pre-trained ResNet50 model (ImageNet weights)
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3))

# Add a custom classification head (Fine-tuning)
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(train_generator.num_classes, activation='softmax')(x)

# Create the final model
model = Model(inputs=base_model.input, outputs=predictions)

# Freeze the base model layers
for layer in base_model.layers:
    layer.trainable = False

# 4. Compile and Train
model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

print("Starting fine-tuning for Crop Health model...")
# Note: The steps_per_epoch need real data to run correctly.
try:
    model.fit(
        train_generator,
        steps_per_epoch=max(1, train_generator.n // BATCH_SIZE),
        epochs=EPOCHS,
        validation_data=validation_generator,
        validation_steps=max(1, validation_generator.n // BATCH_SIZE)
    )
except Exception as e:
    print(f"Training failed (expected due to simulated data): {e}")
    
# 5. Save Model
if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)
model.save(MODEL_SAVE_PATH)
print(f"Crop Health model saved to {MODEL_SAVE_PATH}")

# Clean up temporary data structure
# shutil.rmtree(TEMP_DATA_DIR)
# print(f"Cleaned up temporary directory: {TEMP_DATA_DIR}")