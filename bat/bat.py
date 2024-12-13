import os
import argparse

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
PYTHON_DIR = os.path.join(current_dir, "../")
BAT_DIR = current_dir
ALIAS_DIR = os.path.join(current_dir, "../alias")

override_all = False

def ensure_bat_bat_exists():
    bat_bat_path = os.path.join(BAT_DIR, "bat.bat")
    if not os.path.exists(bat_bat_path):
        with open(bat_bat_path, "w") as bat_bat_file:
            bat_bat_file.write(
                "@echo off\n"
                f"py {os.path.join(BAT_DIR, 'bat.py').replace('\\', '/')} %*\n"
            )
        print("Generated 'bat.bat' with the correct content.")

ensure_bat_bat_exists()

def process_alias_files():
    for alias_file in os.listdir(ALIAS_DIR):
        if alias_file.endswith('.alias'):  # Changed from .txt to .alias
            with open(os.path.join(ALIAS_DIR, alias_file), 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        process_alias_line(line)

def process_alias_line(line):
    global override_all
    parts = line.split('>>')
    if len(parts) != 2:
        return

    cmd_content = parts[0].strip()
    cmd_name = parts[1].strip()
    bat_file_name = f"{cmd_name}.bat"
    bat_path = os.path.join(BAT_DIR, bat_file_name)

    if os.path.exists(bat_path):
        if override_all:
            proceed = True
        else:
            response = input(f"Batch file '{bat_file_name}' already exists. Update it? (y/n/a): ")
            if response.lower() == 'a':
                override_all = True
                proceed = True
            elif response.lower() == 'y':
                proceed = True
            else:
                proceed = False
        if not proceed:
            return

    max_arg_used = 0
    for i in range(1, 10):
        if f"${i}" in cmd_content:
            max_arg_used = i
            cmd_content = cmd_content.replace(f"${i}", f"%{i}")

    extra_args = ' '.join(f"%{i}" for i in range(max_arg_used + 1, min(max_arg_used + 11, 10)))

    bat_content = (
        f"@echo off\n"
        f"{cmd_content} {extra_args}\n"
    )

    try:
        with open(bat_path, "w") as bat_file:
            bat_file.write(bat_content)
        print(f"Batch file '{bat_file_name}' has been {'updated' if os.path.exists(bat_path) else 'created'} successfully.")
    except OSError as e:
        print(f"Error: Could not create/update the batch file '{bat_file_name}'. {e}")

def generate_bat_file(python_file_name):
    if not python_file_name.endswith(".py"):
        python_file_name += ".py"

    base_name = os.path.splitext(python_file_name)[0]
    bat_file_name = f"{base_name}.bat"

    python_file_path = os.path.join(PYTHON_DIR, python_file_name).replace("\\", "/")

    bat_content = (
        f"@echo off\n"
        f"py {python_file_path} %*\n"
    )

    try:
        with open(os.path.join(BAT_DIR, bat_file_name), "w") as bat_file:
            bat_file.write(bat_content)
        print(f"Batch file '{bat_file_name}' has been {'updated' if os.path.exists(os.path.join(BAT_DIR, bat_file_name)) else 'created'} successfully.")
    except OSError as e:
        print(f"Error: Could not create/update the batch file '{bat_file_name}'. {e}")

def clean_bat_directory():
    for file in os.listdir(BAT_DIR):
        if file.endswith('.bat') and file not in ['bat.py', 'bat.bat']:
            os.remove(os.path.join(BAT_DIR, file))
    print("Cleaned BAT_DIR except bat.py and bat.bat.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage batch files.")
    parser.add_argument('-f', '--force', action='store_true', help='Force override without prompting.')
    parser.add_argument('-c', '--clean', action='store_true', help='Clean BAT_DIR before generating files.')
    args = parser.parse_args()

    if args.clean:
        clean_bat_directory()

    override_all = args.force

    process_alias_files()
    for file_name in os.listdir(PYTHON_DIR):
        if file_name.endswith(".py"):
            generate_bat_file(file_name)