import os
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog

def invert_green_channel(input_path, output_path):
    with Image.open(input_path) as img:
        # Convert to numpy array
        img_array = np.array(img)
        
        # Check if the image is in RGB mode
        if img.mode == 'RGB':
            # Invert only the green channel
            img_array[:, :, 1] = 255 - img_array[:, :, 1]
        else:
            print(f"Warning: Unexpected color mode {img.mode} for {input_path}")
            return

        # Create a new image from the modified array
        inverted_img = Image.fromarray(img_array)
        
        # Save the new image
        inverted_img.save(output_path, quality=100, subsampling=0)
    
    print(f"Processed: {os.path.basename(input_path)}")

def process_folder(input_folder):
    output_folder = os.path.join(input_folder, "output")
    os.makedirs(output_folder, exist_ok=True)
    
    supported_extensions = ('.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp')
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(supported_extensions):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"inverted_{filename}")
            try:
                invert_green_channel(input_path, output_path)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

# GUI setup
root = tk.Tk()
root.withdraw()

print("Please select the folder containing the normal maps to process.")
folder_path = filedialog.askdirectory(title="Select Folder")

if folder_path:
    process_folder(folder_path)
else:
    print("No folder selected. Exiting.")