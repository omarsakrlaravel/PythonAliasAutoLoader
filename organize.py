import os
import shutil
import argparse

default_desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

def organize_files_by_extension(path, include_folders=False):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)

        if os.path.isdir(item_path):
            if not include_folders:
                continue

            folder_path = os.path.join(path, 'folders')
            os.makedirs(folder_path, exist_ok=True)
            try:
                shutil.move(item_path, folder_path)
                print(f"Moved folder '{item}' to '{folder_path}'")
            except Exception as e:
                print(f"Error moving folder '{item}': {e}")
            continue

        file_extension = os.path.splitext(item)[1][1:].lower()

        if not file_extension:
            file_extension = 'no_extension'

        extension_folder_path = os.path.join(path, file_extension)
        os.makedirs(extension_folder_path, exist_ok=True)

        try:
            shutil.move(item_path, extension_folder_path)
            print(f"Moved '{item}' to '{extension_folder_path}'")
        except Exception as e:
            print(f"Error moving '{item}': {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files on the desktop by their extensions.")
    parser.add_argument("path", type=str, nargs='?', default=default_desktop_path, help="Path to the directory to organize (default: Desktop).")
    parser.add_argument("--include-folders", action="store_true", help="Include folders in the organization.")

    args = parser.parse_args()

    organize_files_by_extension(args.path, args.include_folders)