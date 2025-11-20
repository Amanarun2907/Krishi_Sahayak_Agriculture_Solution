
# import torch
# import torch.nn as nn
# 
# from torch.utils.data import Dataset, DataLoader
# import segmentation_models_pytorch as smp
# import cv2
# import numpy as np
# from pathlib import Path
# from tqdm import tqdm

# from config import DATA_DIR, MODELS_DIR, MODEL_CONFIGS
# from modules import preprocessing

# # --- Configuration ---
# BATCH_SIZE = 4
# EPOCHS = 1
# SECTOR_NAME = "irrigation_management"
# DATASET_NAME = MODEL_CONFIGS[SECTOR_NAME]["dataset_name"]
# DATASET_PATH = Path(DATA_DIR) / DATASET_NAME
# MODEL_SAVE_PATH = Path(MODELS_DIR) / "agriculture_vision_segmentation_model.pth"
# IMG_SIZE = (512, 512)
# NUM_CLASSES = 6

# # --- Custom Dataset Class ---
# class AgricultureVisionDataset(Dataset):
#     def __init__(self, data_root, transform=None):
#         self.data_root = Path(data_root)
#         self.image_paths = sorted((self.data_root / 'images' / 'rgb').glob('*.jpg'))
#         self.transform = transform
        
#     def __len__(self):
#         return len(self.image_paths)

#     def __getitem__(self, idx):
#         rgb_path = self.image_paths[idx]
#         nir_path = self.data_root / 'images' / 'nir' / rgb_path.name
#         mask_path = self.data_root / 'masks' / rgb_path.name.replace('.jpg', '.png')
        
#         rgb_image = cv2.imread(str(rgb_path), cv2.IMREAD_UNCHANGED)
#         nir_image = cv2.imread(str(nir_path), cv2.IMREAD_UNCHANGED)
#         mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)

#         if rgb_image is None or nir_image is None or mask is None:
#             raise FileNo
# tFoundError(f"Missing file for sample: {rgb_path.name}")

#         combined_image = np.dstack((rgb_image, nir_image))
        
#         combined_image = cv2.resize(combined_image, IMG_SIZE)
#         mask = cv2.resize(mask, IMG_SIZE, interpolation=cv2.INTER_NEAREST)
        
#         # --- FIX: Remap mask values to a valid range (0-5) ---
#         # NOTE: This remapping is based on a common scenario. You may need to
#         # adjust it based on your dataset's specific pixel-to-class mapping.
        
#         # Create a new, empty mask
#         remapped_mask = np.zeros_like(mask, dtype=np.int64)
        
#         # Example remapping (you should verify your dataset's actual values)
#         # Assuming different pixel values represent different classes
#         remapped_mask[mask == 128] = 1 # Example mapping
#         remapped_mask[mask == 255] = 2 # Example mapping
#         # Add more remapping as needed
        
#         # A simpler, more general fix is to just convert the existing 0/255 mask
#         # to 0/1, as your model is configured for a single class (weeds, etc) with a background.
#         remapped_mask = (mask > 0).astype(np.int64)
#         # --- END FIX ---
        
#         image_tensor = np.transpose(combined_image, (2, 0, 1)).astype(np.float32) / 255.0
        
#         return torch.tensor(image_tensor), torch.tensor(remapped_mask)

# # --- Initialize Dataset and Dataloaders ---
# train_data_root = DATASET_PATH / 'train'
# if not train_data_root.exists():
#     raise FileNotFoundError(f"Training data directory not found: {train_data_root}")
    
# train_dataset = AgricultureVisionDataset(data_root=train_data_root)

# if len(train_dataset) == 0:
#     print(f"No images found in: {train_data_root / 'images' / 'rgb'}")
#     raise ValueError("The training dataset is empty.")

# train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

# # --- Define the U-Net Model (for multi-class segmentation) ---
# # Note: The 'in_channels' is set to 4 to accept the combined RGB+NIR image.
# model = smp.Unet(
#     encoder_name="resnet34",
#     encoder_weights="imagenet",
#     in_channels=4,
#     classes=2,  # FIX: Set classes to 2 (background + 1 class, e.g., water)
# )

# # --- Define Loss and Optimizer ---
# loss_fn = nn.CrossEntropyLoss()
# optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# # --- Training Loop with tqdm progress bar ---
# print("Starting fine-tuning for Agriculture-Vision segmentation model...")
# for epoch in range(EPOCHS):
#     pbar = tqdm(train_dataloader, desc=f"Epoch {epoch+1}/{EPOCHS}")
#     for images, masks in pbar:
#         outputs = model(images)
#         loss = loss_fn(outputs, masks)
#         optimizer.zero_grad()
#         loss.backward()
#         optimizer.step()
        
#         pbar.set_postfix({'loss': loss.item()})

# # --- Save the Model ---
# torch.save(model.state_dict(), MODEL_SAVE_PATH)

# print(f"Agriculture-Vision segmentation model saved to {MODEL_SAVE_PATH}")

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import segmentation_models_pytorch as smp
import cv2
import numpy as np
from pathlib import Path
from tqdm import tqdm

from config import DATA_DIR, MODELS_DIR, MODEL_CONFIGS
from modules import preprocessing

# --- Configuration ---
BATCH_SIZE = 4
EPOCHS = 1
SECTOR_NAME = "irrigation_management"
DATASET_NAME = MODEL_CONFIGS[SECTOR_NAME]["dataset_name"]
DATASET_PATH = Path(DATA_DIR) / DATASET_NAME
MODEL_SAVE_PATH = Path(MODELS_DIR) / "agriculture_vision_segmentation_model.pth"
IMG_SIZE = (512, 512)
NUM_CLASSES = 6

# --- Custom Dataset Class ---
class AgricultureVisionDataset(Dataset):
    def __init__(self, data_root, transform=None, subset_size=None):
        self.data_root = Path(data_root)
        self.image_paths = sorted((self.data_root / 'images' / 'rgb').glob('*.jpg'))
        
        # --- FIX: Take a subset of images ---
        if subset_size and subset_size < len(self.image_paths):
            self.image_paths = self.image_paths[:subset_size]
        # --- END FIX ---
        
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        rgb_path = self.image_paths[idx]
        nir_path = self.data_root / 'images' / 'nir' / rgb_path.name
        mask_path = self.data_root / 'masks' / rgb_path.name.replace('.jpg', '.png')
        
        rgb_image = cv2.imread(str(rgb_path), cv2.IMREAD_UNCHANGED)
        nir_image = cv2.imread(str(nir_path), cv2.IMREAD_UNCHANGED)
        mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)

        if rgb_image is None or nir_image is None or mask is None:
            raise FileNotFoundError(f"Missing file for sample: {rgb_path.name}")

        combined_image = np.dstack((rgb_image, nir_image))
        
        combined_image = cv2.resize(combined_image, IMG_SIZE)
        mask = cv2.resize(mask, IMG_SIZE, interpolation=cv2.INTER_NEAREST)
        
        remapped_mask = (mask > 0).astype(np.int64)
        
        image_tensor = np.transpose(combined_image, (2, 0, 1)).astype(np.float32) / 255.0
        
        return torch.tensor(image_tensor), torch.tensor(remapped_mask)

# --- Initialize Dataset and Dataloaders ---
train_data_root = DATASET_PATH / 'train'
if not train_data_root.exists():
    raise FileNotFoundError(f"Training data directory not found: {train_data_root}")
    
# --- FIX: Pass a subset_size to the dataset ---
train_dataset = AgricultureVisionDataset(data_root=train_data_root, subset_size=300)
# --- END FIX ---

if len(train_dataset) == 0:
    print(f"No images found in: {train_data_root / 'images' / 'rgb'}")
    raise ValueError("The training dataset is empty.")

train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

# --- Define the U-Net Model (for multi-class segmentation) ---
model = smp.Unet(
    encoder_name="resnet34",
    encoder_weights="imagenet",
    in_channels=4,
    classes=2,
)

# --- Define Loss and Optimizer ---
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# --- Training Loop with tqdm progress bar ---
print("Starting fine-tuning for Agriculture-Vision segmentation model...")
for epoch in range(EPOCHS):
    pbar = tqdm(train_dataloader, desc=f"Epoch {epoch+1}/{EPOCHS}")
    for images, masks in pbar:
        outputs = model(images)
        loss = loss_fn(outputs, masks)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        pbar.set_postfix({'loss': loss.item()})

# --- Save the Model ---
torch.save(model.state_dict(), MODEL_SAVE_PATH)
print(f"Agriculture-Vision segmentation model saved to {MODEL_SAVE_PATH}")