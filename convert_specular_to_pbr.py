import os
import re
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

def identify_texture_maps(folder_path):
    texture_maps = {
        'specular': None,
        'gloss': None
    }
    
    pattern = re.compile(r'(spec(ular)?|gloss(iness)?)', re.IGNORECASE)
    
    for filename in os.listdir(folder_path):
        match = pattern.search(filename)
        if match:
            map_type = match.group(1).lower()
            if map_type.startswith('spec'):
                texture_maps['specular'] = os.path.join(folder_path, filename)
            elif map_type.startswith('gloss'):
                texture_maps['gloss'] = os.path.join(folder_path, filename)
    
    return texture_maps

def create_metalness_map(specular_path):
    with Image.open(specular_path) as spec_img:
        spec_array = np.array(spec_img.convert('L'), dtype=float) / 255.0
    
    # Estimate metalness based on specular intensity
    metalness = np.clip((spec_array - 0.5) * 2, 0, 1)
    
    # Enhance contrast
    metalness = np.power(metalness, 0.5)
    
    return Image.fromarray((metalness * 255).astype(np.uint8))

def create_roughness_map(gloss_path):
    with Image.open(gloss_path) as gloss_img:
        gloss_array = np.array(gloss_img.convert('L'), dtype=float) / 255.0
    
    # Convert glossiness to roughness
    roughness = 1 - gloss_array
    
    # Adjust roughness curve
    roughness = np.power(roughness, 1.5)
    
    return Image.fromarray((roughness * 255).astype(np.uint8))

def process_textures(texture_maps, output_folder):
    if not texture_maps['specular']:
        raise ValueError("Specular map is required for conversion.")
    
    # Create metalness map
    metalness_map = create_metalness_map(texture_maps['specular'])
    metalness_map.save(os.path.join(output_folder, "metalness.png"))
    print("Created metalness map.")
    
    # Create roughness map if gloss map is available
    if texture_maps['gloss']:
        roughness_map = create_roughness_map(texture_maps['gloss'])
        roughness_map.save(os.path.join(output_folder, "roughness.png"))
        print("Created roughness map.")
    else:
        print("No gloss map found. Skipping roughness map creation.")

def main():
    root = tk.Tk()
    root.withdraw()
    
    print("Please select the folder containing the Specular-Gloss textures to convert.")
    input_folder = filedialog.askdirectory(title="Select Input Folder")
    
    if not input_folder:
        print("No folder selected. Exiting.")
        return
    
    output_folder = os.path.join(input_folder, "metallic_roughness_output")
    os.makedirs(output_folder, exist_ok=True)
    
    try:
        texture_maps = identify_texture_maps(input_folder)
        process_textures(texture_maps, output_folder)
        print("Conversion completed successfully.")
        messagebox.showinfo("Conversion Complete", f"Textures have been converted and saved to:\n{output_folder}")
    except Exception as e:
        error_message = f"An error occurred during conversion: {str(e)}"
        print(error_message)
        messagebox.showerror("Conversion Error", error_message)

if __name__ == "__main__":
    main()
