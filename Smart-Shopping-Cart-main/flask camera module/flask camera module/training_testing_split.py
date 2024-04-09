import os
from sklearn.model_selection import train_test_split
from shutil import copyfile

# Set the root directory of your dataset
dataset_root = '../prediction/new_prediction_frames'

# Set the output directories for train and test
output_train_dir = '../dataset_v8/train/'
output_test_dir = '../dataset_v8/test/'

# Get a list of all class folders
class_folders = [folder for folder in os.listdir(dataset_root) if os.path.isdir(os.path.join(dataset_root, folder))]

# Set the minimum number of images per class
min_images_per_class = 2

# Iterate through each class folder
for class_folder in class_folders:
    class_path = os.path.join(dataset_root, class_folder)
    
    # Get a list of all image files in the class folder
    class_images = [os.path.join(class_folder, image) for image in os.listdir(class_path) if image.endswith('.jpg')]
    
    # Print the number of images for each class
    print(f"Class '{class_folder}' has {len(class_images)} images.")
    
    # Check if the class has enough images for the split
    if len(class_images) < min_images_per_class:
        print(f"Skipping class '{class_folder}' due to insufficient images.")
        continue
    
    # Split the images into training and testing sets
    train_class_images, test_class_images = train_test_split(class_images, test_size=0.2, random_state=42)
    
    # Create output directories if they don't exist
    os.makedirs(os.path.join(output_train_dir, class_folder), exist_ok=True)
    os.makedirs(os.path.join(output_test_dir, class_folder), exist_ok=True)

    # Copy images to the train directory
    for train_image in train_class_images:
        source_path = os.path.join(dataset_root, train_image)
        destination_path = os.path.join(output_train_dir, train_image)
        copyfile(source_path, destination_path)

    # Copy images to the test directory
    for test_image in test_class_images:
        source_path = os.path.join(dataset_root, test_image)
        destination_path = os.path.join(output_test_dir, test_image)
        copyfile(source_path, destination_path)

print("Data splitting and organization completed.")
