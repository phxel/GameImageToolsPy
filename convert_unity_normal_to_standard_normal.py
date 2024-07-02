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

        # Extract channels (assuming RGBA, handle RGB similarly)
        r, g, b, a = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2], img_array[:, :, 3]

        # Perform the conversion
        new_r = a  # Alpha to Red
        new_g = b  # Blue to Green
        new_b = r  # Red to Blue
        new_a = 255 * np.ones_like(r)  # White Alpha

        # Recombine into a new image array
        new_img_array = np.dstack((new_r, new_g, new_b, new_a))

        # Create and save the new image
        converted_img = Image.fromarray(new_img_array.astype(np.uint8), 'RGBA') 
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
