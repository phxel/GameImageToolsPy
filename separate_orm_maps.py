import os
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog

def separate_orm(input_path, output_folder):
    # Open the image
    with Image.open(input_path) as img:
        # Convert to numpy array
        img_array = np.array(img)
        
        # Check if the image is in RGB mode
        if img.mode != 'RGB':
            print(f"Warning: Unexpected color mode {img.mode} for {input_path}")
            return

        # Extract channels
        ao = Image.fromarray(img_array[:,:,0], 'L')
        roughness = Image.fromarray(img_array[:,:,1], 'L')
        metallic = Image.fromarray(img_array[:,:,2], 'L')

        # Generate output filenames
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        ao_path = os.path.join(output_folder, f"{base_name}_AO.png")
        roughness_path = os.path.join(output_folder, f"{base_name}_Roughness.png")
        metallic_path = os.path.join(output_folder, f"{base_name}_Metallic.png")

        # Save separated channels
        ao.save(ao_path)
        roughness.save(roughness_path)
        metallic.save(metallic_path)

    print(f"Processed: {os.path.basename(input_path)}")
    print(f"  AO: {ao_path}")
    print(f"  Roughness: {roughness_path}")
    print(f"  Metallic: {metallic_path}")

def process_folder(input_folder):
    output_folder = os.path.join(input_folder, "separated_orm")
    os.makedirs(output_folder, exist_ok=True)
    
    supported_extensions = ('.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp')
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(supported_extensions):
            input_path = os.path.join(input_folder, filename)
            try:
                separate_orm(input_path, output_folder)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

# GUI setup
root = tk.Tk()
root.withdraw()

print("Please select the folder containing the ORM texture maps to process.")
folder_path = filedialog.askdirectory(title="Select Folder")

if folder_path:
    process_folder(folder_path)
else:
    print("No folder selected. Exiting.")
