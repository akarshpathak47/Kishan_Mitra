import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json
import os

# --- 1. SET THE PATH TO YOUR DATASET ---
# This path should point to the parent directory containing 'train', 'valid', and 'test' folders.
# We use '../' because we are in the 'ml' folder and need to go up one level to 'KisanMitra'
# and then down into the 'data' folder.
DATASET_ROOT_DIR = '../data/New Plant Diseases Dataset(Augmented)'

# --- 2. DEFINE THE DIRECTORIES FOR TRAINING, VALIDATION, AND TESTING ---
TRAIN_DIR = os.path.join(DATASET_ROOT_DIR, 'train')
VALID_DIR = os.path.join(DATASET_ROOT_DIR, 'valid')
TEST_DIR = os.path.join(DATASET_ROOT_DIR, 'test')

# --- 3. DEFINE MODEL PARAMETERS ---
IMG_HEIGHT = 224
IMG_WIDTH = 224
BATCH_SIZE = 32

# --- 4. DEFINE A FUNCTION TO CREATE DATA GENERATORS ---
def get_data_generators():
    """
    Creates and returns data generators for training, validation, and testing.
    """
    train_datagen = ImageDataGenerator(
        rescale=1./255, # Normalize pixel values
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    validation_datagen = ImageDataGenerator(rescale=1./255)
    test_datagen = ImageDataGenerator(rescale=1./255)

    print(f"Loading training data from: {os.path.abspath(TRAIN_DIR)}")
    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )

    print(f"Loading validation data from: {os.path.abspath(VALID_DIR)}")
    validation_generator = validation_datagen.flow_from_directory(
        VALID_DIR,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )

    test_generator = None
    if os.path.exists(TEST_DIR) and os.listdir(TEST_DIR):
        print(f"Loading test data from: {os.path.abspath(TEST_DIR)}")
        test_generator = test_datagen.flow_from_directory(
            TEST_DIR,
            target_size=(IMG_HEIGHT, IMG_WIDTH),
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            shuffle=False
        )
    else:
        print("Test directory not found or is empty. Skipping test data loading.")

    return train_generator, validation_generator, test_generator, train_generator.class_indices

# --- 5. A MAIN BLOCK TO RUN THE FUNCTION AND SAVE THE CLASS INDICES ---
if __name__ == '__main__':
    print("--- Running Data Preprocessing Script ---")
    train_gen, val_gen, test_gen, class_indices = get_data_generators()

    print(f"\nSummary:")
    # The fix is here: 'num_samples' was changed to 'samples'
    print(f"  Training images: {train_gen.samples} in {train_gen.num_classes} classes.")
    print(f"  Validation images: {val_gen.samples} in {val_gen.num_classes} classes.")
    if test_gen:
        print(f"  Test images: {test_gen.samples} in {test_gen.num_classes} classes.")
    else:
        print("  No test data loaded.")
    print(f"  Class names and their integer indices: {class_indices}")

    idx_to_class = {str(v): k for k, v in class_indices.items()}
    with open('class_names.json', 'w') as f:
        json.dump(idx_to_class, f, indent=4)
    print(f"Class names mapping saved to {os.path.abspath('class_names.json')}")
    print("--- Data Preprocessing Complete ---")