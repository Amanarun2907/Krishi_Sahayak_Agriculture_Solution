import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image

def display_segmentation_mask(image_np, mask_np, title="Segmentation"):
    """
    Displays an image with a segmentation mask overlay.
    
    Args:
        image_np (np.array): The original image as a NumPy array.
        mask_np (np.array): The binary mask as a NumPy array (e.g., 0 and 255).
        title (str): The title for the plot.
    """
    # Create an RGBA image from the mask
    overlay = np.zeros((*mask_np.shape, 4), dtype=np.uint8)
    overlay[mask_np == 255] = [255, 0, 0, 150]  # Red overlay with transparency
    
    # Convert original image to RGBA
    if image_np.shape[2] == 3:
        image_rgba = cv2.cvtColor(image_np, cv2.COLOR_RGB2RGBA)
    else:
        image_rgba = image_np

    # Blend the original image with the overlay
    blended = cv2.addWeighted(image_rgba, 1.0, overlay, 1.0, 0)
    
    st.image(blended, caption=title, use_column_width=True)

def display_bounding_boxes(image_np, detections, title="Object Detection"):
    """
    Displays an image with bounding boxes and labels.
    
    Args:
        image_np (np.array): The original image as a NumPy array.
        detections (list): A list of dictionaries with 'box' and 'label' keys.
        title (str): The title for the plot.
    """
    img_with_boxes = image_np.copy()
    
    for det in detections:
        box = det['box']
        label = det['label']
        confidence = det['confidence']
        
        x_min, y_min, x_max, y_max = [int(val) for val in box]
        
        # Draw rectangle and label
        color = (0, 255, 0)  # Green
        cv2.rectangle(img_with_boxes, (x_min, y_min), (x_max, y_max), color, 2)
        cv2.putText(img_with_boxes, f"{label}: {confidence:.2f}", (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
    st.image(img_with_boxes, caption=title, use_column_width=True)

def display_ndvi_map(ndvi_map, title="NDVI Map"):
    """
    Displays a color-coded NDVI map.
    
    Args:
        ndvi_map (np.array): The NDVI values.
        title (str): The title for the plot.
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.imshow(ndvi_map, cmap='RdYlGn')
    cbar = fig.colorbar(im, ax=ax, shrink=0.7)
    cbar.set_label("NDVI Value (Scaled)")
    ax.set_title(title)
    ax.axis('off')
    
    st.pyplot(fig)