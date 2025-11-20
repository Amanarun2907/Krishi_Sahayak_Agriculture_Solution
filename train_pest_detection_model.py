from ultralytics import YOLO
import os
from config import DATA_DIR, MODELS_DIR, MODEL_CONFIGS

# --- Configuration ---
SECTOR_NAME = "pest_detection"
DATASET_NAME = MODEL_CONFIGS[SECTOR_NAME]["dataset_name"]
DATASET_PATH = os.path.join(DATA_DIR, DATASET_NAME)
MODEL_SAVE_PATH = os.path.join(MODELS_DIR, "pest_detection_model.pt")

# Load a pre-trained YOLOv8 model
# 'yolov8n.pt' is the nano version, fast and efficient for low-resource deployment
model = YOLO('yolov8n.pt')

# Train the model on the custom dataset
print("Starting fine-tuning for Pest Detection model...")

# The 'data.yaml' file in the dataset directory specifies the paths to images and labels
results = model.train(data=os.path.join(DATASET_PATH, 'OPA_data.yaml'), epochs=1, imgsz=416)

# Save the fine-tuned model
# The best model will be saved in a 'runs' directory, we'll move it
best_model_path = os.path.join(model.trainer.save_dir, 'weights', 'best.pt')
final_model = YOLO(best_model_path)
final_model.save(MODEL_SAVE_PATH)

print(f"Pest Detection model saved to {MODEL_SAVE_PATH}")