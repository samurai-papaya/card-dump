
from datetime import datetime
import os
import subprocess
import sys
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askdirectory

# Constants
# DESTINATION_BASE = r"C:\Users\ModSeven\Desktop\destination_test"  # Replace with your desired base destination
FOOTAGE_FOLDER_NAME= "1-footage"
PHOTO_FOLDER_NAME= "1-photos"
GOPRO_FOLDER_NAME="100GOPRO"
PROXY_FOLDER_NAME="Proxy"
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".flv"}
PROXY_EXTENSIONS = {".lrv"}
PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".cr2", ".nef", ".arw", ".dng", ".tiff"}

def organize_files(source, client_name, project_name):
    """
    Organizes files from the source SD card into a structured destination folder.
    """

    # Generate date prefix
    date_prefix = datetime.now().strftime("%y.%m.%d")
    project_folder_name = f"{date_prefix} {client_name} - {project_name}"


    DCIM = Path(source)  
    # Define target folders         
    goPro_folder = DCIM / GOPRO_FOLDER_NAME

    project_folder = DCIM.parent/ project_folder_name
    footage_folder = DCIM / FOOTAGE_FOLDER_NAME       

    goPro_folder.rename(footage_folder)
    DCIM.rename(project_folder)

    proxy_folder = project_folder / FOOTAGE_FOLDER_NAME / PROXY_FOLDER_NAME

    if proxy_folder.exists:
        # Get the original folder name and its parent directory
        folder_name = os.path.basename(proxy_folder)
        parent_dir = os.path.dirname(proxy_folder)

        # New folder path for the original folder renamed with "_og"
        original_folder_renamed = os.path.join(parent_dir, f"{folder_name}_og")

        # Rename the original folder by appending "_og"
        os.rename(proxy_folder, original_folder_renamed)

        # New folder where the modified files will be saved
        new_folder = os.path.join(parent_dir, folder_name)

        # Create the new folder
        os.makedirs(new_folder, exist_ok=True)

        # Iterate over all files in the original (now renamed) folder
        for filename in os.listdir(original_folder_renamed):
            # Make the extension check case-insensitive
            if filename.lower().endswith(".mp4") or filename.lower().endswith(".MP4"):
                # Full path to the input file in the renamed folder
                input_file = os.path.join(original_folder_renamed, filename)

                # Define the output file path in the new folder
                output_file = os.path.join(new_folder, filename)

                # FFmpeg command to copy streams and change color range to full (2)
                ffmpeg_command = [
                    "ffmpeg",
                    "-i", input_file,
                    "-c", "copy",
                    "-color_range", "2",
                    output_file
                ]

                # Run the FFmpeg command
                subprocess.run(ffmpeg_command)

        print("Processing completed.")
        print(f"Original folder renamed to: {original_folder_renamed}")
        print(f"Modified files saved in: {new_folder}")


    os.startfile(project_folder)
    print("Done")

if __name__ == "__main__":
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

    # Call the function
    organize_files(source, client_name, project_name)
