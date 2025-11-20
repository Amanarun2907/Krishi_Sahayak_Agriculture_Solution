import tensorflow as tf
from tensorflow.keras import layers, Model

def create_multi_task_model(input_shape=(224, 224, 3), 
                            num_crop_health_classes=4, 
                            num_pest_classes=19, # +1 for background class
                            num_weed_classes=2, # Weed/Not-Weed for segmentation
                            num_irrigation_classes=3): # Low, Moderate, High Water Stress
    """
    Creates a custom multi-task deep learning model with shared backbone and
    separate heads for each agricultural task.
    """

    # --- Shared Feature Extractor (Backbone) ---
    inputs = layers.Input(shape=input_shape, name="input_image")
    x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2))(x)

    x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2))(x)
    
    x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = layers.BatchNormalization()(x)
    shared_features = layers.MaxPooling2D((2, 2))(x)

    # --- Head 1: Crop Health Classification ---
    ch_head = layers.Flatten(name="crop_health_flatten")(shared_features)
    ch_head = layers.Dense(128, activation='relu')(ch_head)
    ch_output = layers.Dense(num_crop_health_classes, activation='softmax', name='crop_health_output')(ch_head)

    # --- Head 2: Pest Detection (Simplified Bounding Box and Class) ---
    pest_features = layers.Flatten(name="pest_flatten")(shared_features)
    pest_features = layers.Dense(128, activation='relu')(pest_features)
    pest_class_output = layers.Dense(num_pest_classes, activation='softmax', name='pest_class_output')(pest_features)
    pest_bbox_output = layers.Dense(4, activation='sigmoid', name='pest_bbox_output')(pest_features) 

    # --- Head 3: Weed Segmentation ---
    seg_head = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(shared_features)
    seg_head = layers.UpSampling2D((2, 2))(seg_head)
    seg_head = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(seg_head)
    seg_head = layers.UpSampling2D((2, 2))(seg_head)
    seg_head = layers.Conv2D(16, (3, 3), activation='relu', padding='same')(seg_head)
    # FIX: Use the Keras Resizing layer instead of tf.image.resize()
    seg_head = layers.Resizing(input_shape[0], input_shape[1])(seg_head)
    seg_output = layers.Conv2D(1, (1, 1), activation='sigmoid', name='weed_segmentation_output')(seg_head)

    # --- Head 4: Irrigation/Water Stress Classification ---
    irr_head = layers.Flatten(name="irrigation_flatten")(shared_features)
    irr_head = layers.Dense(64, activation='relu')(irr_head)
    irr_output = layers.Dense(num_irrigation_classes, activation='softmax', name='irrigation_output')(irr_head)

    # --- Combine all heads into a single model ---
    model = Model(inputs=inputs, 
                  outputs=[ch_output, pest_class_output, pest_bbox_output, seg_output, irr_output], 
                  name="MultiTaskAgriculturalModel")
    return model

if __name__ == '__main__':
    model = create_multi_task_model()
    model.summary()
    tf.keras.utils.plot_model(model, to_file='multi_task_model.png', show_shapes=True, show_layer_names=True)