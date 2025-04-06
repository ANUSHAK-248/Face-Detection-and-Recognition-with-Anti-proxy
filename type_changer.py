import os
from PIL import Image

# Specify the folder containing images
folder_path = "Images_raw"
output_folder = "Images"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    input_path = os.path.join(folder_path, filename)
    # Check if the file is an image
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (for formats like PNG, WEBP)
            # Define the output path with JPG extension
            img = img.resize((216, 216))
            img = img.convert("RGB")
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".jpg")
            # Save the file in JPG format
            img.save(output_path, "JPEG")
            print(f"Converted: {filename} -> {os.path.basename(output_path)}")
            os.remove(f"{input_path}")
            print("successfully deleted "+filename+" from its previous folder ")
    except Exception as e:
        print(f"Skipping {filename}: {e}")

print("Conversion complete!")
