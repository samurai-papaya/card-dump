
from datetime import datetime
import os
import sys
import shutil
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askdirectory
import configparser


# Constants
CONFIG_FILE = "config.cfg"
VIDEO_FOLDER_NAME= "1-Footage"
PHOTO_FOLDER_NAME= "1-Photos"
AUDIO_FOLDER_NAME= "1-Audio"
OTHERS_FOLDER_NAME= "1-otros"
PROXY_FOLDER_NAME= "Proxies"
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".flv"}
PROXY_EXTENSIONS = {".lrv"}
AUDIO_EXTENSIONS = {
  ".wav", 
  ".flac", 
  ".m4a", 
  ".wv", 
  ".ape", 
  ".mp3", 
  ".aac", 
  ".ogg", 
  ".oga", 
  ".wma", 
  ".mid", 
  ".midi", 
}
PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".cr2", ".nef", ".arw", ".dng", ".tiff"}


def create_default_config(file_path):
    """Creates a default config file if it doesn't exist."""

    Tk().withdraw()  # Hide the root Tkinter window
    destination = askdirectory(title="Select the destination Directory")
    
    config = configparser.ConfigParser()

    # Add default configuration sections and values
    config['settings'] = {'destination_folder': destination}

    # Write the default configuration to the file
    with open(file_path, 'w') as config_file:
        config.write(config_file)
    print(f"Default configuration file created at: {file_path}")

def load_config(file_path):
    """Loads the configuration file, creating it if necessary."""
    if not os.path.exists(file_path):
        create_default_config(file_path)

    # Read the configuration file
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

def organize_files(destination_dir,source, client_name, project_name,folder_tag):
    """
    Organizes files from the source SD card into a structured destination folder.
    """
    # Generate date prefix
    date_prefix = datetime.now().strftime("%y.%m.%d")
    project_folder_name = f"{date_prefix} {client_name} - {project_name}"


    destination = Path(destination_dir)
    # Define target folders
    client_folder = destination / client_name
    project_folder = client_folder / project_folder_name
    video_folder = project_folder / f"{VIDEO_FOLDER_NAME} {folder_tag}"
    photo_folder = project_folder / f"{PHOTO_FOLDER_NAME} {folder_tag}"
    audio_folder = project_folder / f"{AUDIO_FOLDER_NAME} {folder_tag}"
    others_folder = project_folder / f"{OTHERS_FOLDER_NAME} {folder_tag}"

    # Create directories if they don't exist

    # Walk through the source folder and organize files
    for root, _, files in os.walk(source):
        for file in files:
            file_path = Path(root) / file
            file_extension = file_path.suffix.lower()

            if file_extension in VIDEO_EXTENSIONS:
                video_folder.mkdir(parents=True, exist_ok=True)
                target_path = video_folder / file
            elif file_extension in PHOTO_EXTENSIONS:
                photo_folder.mkdir(parents=True, exist_ok=True)
                target_path = photo_folder / file
            elif file_extension in AUDIO_EXTENSIONS:
                audio_folder.mkdir(parents=True, exist_ok=True)
                target_path = audio_folder / file
            else:
                others_folder.mkdir(parents=True, exist_ok=True)
                target_path = others_folder / file
                

            # Copy file to the target location
            shutil.copy2(file_path, target_path)
            print(f"Copied: {file_path} -> {target_path}")
    os.startfile(project_folder)
    print("Done")

if __name__ == "__main__":


    # Load the configuration (creating the file if it doesn't exist)
    config = load_config(CONFIG_FILE)
    destination_dir = config.get('settings', 'destination_folder')

     # Check if the source folder is passed as an argument
    source=None
    if len(sys.argv) > 1:
        source = sys.argv[1]
    
    if not source:
        # Use a file dialog if no folder is dragged in
        Tk().withdraw()  # Hide the root Tkinter window
        source = askdirectory(title="Select the Source SD Card Directory")
    
    if not source:
        print("No source directory selected. Exiting.")
        exit()

    # Prompt the user for client and project names
    client_name = input("Enter the client name: ").strip()
    if not client_name:
        client_name="dump"
    project_name = input("Enter the project name: ").strip()
    if not project_name:
        project_name="dump"
    folder_tag = input("Enter the Camera, device, day, etc: ").strip()
    if not folder_tag:
        project_name="undefined"

    # Call the function
    organize_files(destination_dir,source, client_name, project_name,folder_tag)
