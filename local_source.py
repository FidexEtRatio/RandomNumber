import os
import glob

IMG_DIR = "./images/"

def get_images():
    # Returns a list with all the files in ./images
    return glob.glob(os.path.join(IMG_DIR, "*"))

def cleanup():
    # Deletes all the images downloaded in this session
    for file in get_images():
        try:
            os.remove(file)
            print(f"Successfully removed {file}\n")
        except Exception:
            print(f"Error deleting {file}: {Exception}")