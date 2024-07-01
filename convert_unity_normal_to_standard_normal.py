import os
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog

def convert_normal_map(input_path, output_folder):
    # Open the image
    with Image.open(input_path) as img:
        # Convert to numpy array
        img_array = np.array(img)

        # Check if the image is in RGB mode
        if img.mode != 'RGB':
            print(f"Warning: Unexpected color mode {img.mode} for {input_path}")
            return

        # Move alpha to green and fill blue with 255 (white)
        img_array[:,:,1] = img_array[:,:,3]  # Alpha to Green
        img_array[:,:,2] = 255               # Blue to White

        # Create and save the new image
        converted_img = Image.fromarray(img_array[:,:,:3], 'RGB')  # Remove alpha channel

        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(output_folder, f"{base_name}_converted.png")
        converted_img.save(output_path)

        print(f"Converted: {os.path.basename(input_path)}")
        print(f"  Output: {output_path}")

def process_folder(input_folder):
    output_folder = os.path.join(input_folder, "converted_normal_maps")
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp')):
            input_path = os.path.join(input_folder, filename)
            try:
                convert_normal_map(input_path, output_folder)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

# GUI setup
root = tk.Tk()
root.withdraw()

print("Please select the folder containing the Unity normal maps to convert.")
folder_path = filedialog.askdirectory(title="Select Folder")

if folder_path:
    process_folder(folder_path)
else:
    print("No folder selected. Exiting.")
