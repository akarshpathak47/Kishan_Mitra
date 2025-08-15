import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import MobileNetV2 # Using MobileNetV2 for efficiency
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from data_preprocessing import get_data_generators, IMG_HEIGHT, IMG_WIDTH
import json
import os

def build_model(num_classes):
    """
    Builds a deep learning model using transfer learning with MobileNetV2.
    """
    # Load the pre-trained MobileNetV2 model (without its top classification layer)
    base_model = MobileNetV2(
        input_shape=(IMG_HEIGHT, IMG_WIDTH, 3),
        include_top=False, # We'll add our own classification head
        weights='imagenet' # Use weights pre-trained on ImageNet dataset
    )
    
    # Freeze the base model to prevent its weights from being updated during initial training.
    # This allows us to train only the new classification layers quickly.
    base_model.trainable = False

    model = Sequential([
        base_model, # The frozen pre-trained CNN
        Flatten(),  # Flatten the 3D output of the base model into 1D
        Dense(512, activation='relu'), # A dense layer with ReLU activation
        BatchNormalization(),         # Improves training stability and performance
        Dropout(0.5),                 # Dropout for regularization to prevent overfitting
        Dense(num_classes, activation='softmax') # Output layer: one neuron per class, softmax for probabilities
    ])

    # Compile the model
    model.compile(optimizer=Adam(learning_rate=0.0001), # Adam optimizer with a small learning rate
                  loss='categorical_crossentropy',       # Appropriate loss for multi-class classification
                  metrics=['accuracy'])                  # Track accuracy during training
    model.summary()
    return model

def train_model():
    """
    Loads data, builds, trains, and saves the ML model.
    """
    print("\n--- Preparing Data Generators ---")
    train_generator, validation_generator, test_generator, class_indices = get_data_generators()
    num_classes = len(class_indices)
    model = build_model(num_classes)

    # Callbacks for better training
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, verbose=1)
    model_checkpoint = ModelCheckpoint('crop_disease_model_best_weights.h5',
                                        save_best_only=True, monitor='val_accuracy', mode='max', verbose=1)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=0.000001, verbose=1)

    print("\n--- Training Model (Initial Layers) ---")
    history = model.fit(
        train_generator,
        epochs=10, # Number of epochs for initial training (adjust as needed, 5-10 usually good)
        validation_data=validation_generator,
        callbacks=[early_stopping, model_checkpoint, reduce_lr]
    )

    # Optional: Fine-tune the base model (unfreeze some layers) for better accuracy
    print("\n--- Fine-tuning (Unfreezing some base model layers) ---")
    model.load_weights('crop_disease_model_best_weights.h5')

    base_model = model.layers[0] # Get the MobileNetV2 layer
    base_model.trainable = True  # Unfreeze the entire base model

    for layer in base_model.layers[:-60]: # Unfreeze the last 60 layers
        if not isinstance(layer, tf.keras.layers.BatchNormalization):
            layer.trainable = False

    model.compile(optimizer=Adam(learning_rate=0.00001), # Lower learning rate for fine-tuning
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    model.summary() # Check trainable parameters again

    history_fine_tune = model.fit(
        train_generator,
        epochs=10, # Additional epochs for fine-tuning (adjust as needed)
        validation_data=validation_generator,
        callbacks=[early_stopping, model_checkpoint, reduce_lr]
    )

    model.load_weights('crop_disease_model_best_weights.h5')

    model_path = 'crop_disease_model.h5'
    model.save(model_path)
    print(f"\nModel saved to {os.path.abspath(model_path)}")

    if test_generator and test_generator.samples > 0:
        print("\n--- Evaluating on Test Set ---")
        loss, accuracy = model.evaluate(test_generator)
        print(f"Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}")
    else:
        print("\nNo test data available for final evaluation.")

    idx_to_class = {str(v): k for k, v in class_indices.items()}
    with open('class_names.json', 'w') as f:
        json.dump(idx_to_class, f, indent=4)
    print(f"Class names mapping saved to {os.path.abspath('class_names.json')}")
    print("--- Model Training Complete ---")

if __name__ == '__main__':
    train_model()