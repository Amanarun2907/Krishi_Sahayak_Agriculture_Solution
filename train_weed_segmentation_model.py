import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import segmentation_models_pytorch as smp
import cv2
import numpy as npimport os
from pathlib import Path
from tqdm import tqdm  # Import the tqdm library

from config import DATA_DIR, MODELS_DIR, MODEL_CONFIGS
from modules import preprocessing

# --- Configuration ---
BATCH_SIZE = 8
EPOCHS = 1
SECTOR_NAME = "weed_detection"
DATASET_NAME = MODEL_CONFIGS[SECTOR_NAME]["dataset_name"]
DATASET_PATH = Path(DATA_DIR) / DATASET_NAME
MODEL_SAVE_PATH = Path(MODELS_DIR) / "weed_segmentation_model.pth"
IMG_SIZE = (512, 512)

# Custom Dataset Class
class WeedDataset(Dataset):
    def __init__(self, images_dir, labels_dir, transform=None):
        self.images_dir = Path(images_dir)
        self.labels_dir = Path(labels_dir)
        
        self.image_paths = sorted(
            [path for path in self.images_dir.glob('*.jpg') if not path.name.startswith('._')]
        )
        
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        
        label_path = self.labels_dir / f"{image_path.stem}.txt"

        image = cv2.imread(str(image_path))
        if image is None:
            raise FileNotFoundError(f"Image not found at {image_path}")
            
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        mask = preprocessing.create_segmentation_mask(str(label_path), image_size=(image.shape[1], image.shape[0]))
        
        image = cv2.resize(image, IMG_SIZE)
        mask = cv2.resize(mask, IMG_SIZE, interpolation=cv2.INTER_NEAREST)
        
        image = np.transpose(image, (2, 0, 1)).astype(np.float32) / 255.0
        mask = np.expand_dims(mask, axis=0).astype(np.float32) / 255.0
        
        return torch.tensor(image), torch.tensor(mask)

# Initialize dataset and dataloaders
train_dataset = WeedDataset(
    images_dir=DATASET_PATH / 'train' / 'images',
    labels_dir=DATASET_PATH / 'train' / 'labels'
)

if len(train_dataset) == 0:
    print(f"No images found at: {DATASET_PATH / 'train/images'}")
    raise ValueError("The training dataset is empty. Please check your file paths and content.")

train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

# Define the U-Net model
model = smp.Unet(
    encoder_name="resnet34",
    encoder_weights="imagenet",
    in_channels=3,
    classes=1,
)

# Define loss function and optimizer
loss_fn = smp.losses.DiceLoss(mode='binary')
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# --- Training loop with tqdm progress bar ---
print("Starting fine-tuning for Weed Segmentation model...")
for epoch in range(EPOCHS):
    # Wrap the dataloader with tqdm
    pbar = tqdm(train_dataloader, desc=f"Epoch {epoch+1}/{EPOCHS}")
    for images, masks in pbar:
        outputs = model(images)
        loss = loss_fn(outputs, masks)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        # Update progress bar description with current loss
        pbar.set_postfix({'loss': loss.item()})

# Save the model
torch.save(model.state_dict(), MODEL_SAVE_PATH)
print(f"Weed Segmentation model saved to {MODEL_SAVE_PATH}")