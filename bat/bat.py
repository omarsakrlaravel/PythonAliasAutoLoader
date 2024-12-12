import os

PYTHON_DIR = "d:/Python/bin"
BAT_DIR = "d:/Python/bin/bat"
ALIAS_DIR = "d:/Python/bin/alias"

def process_alias_files():
    for alias_file in os.listdir(ALIAS_DIR):
        if alias_file.endswith('.txt'):
            with open(os.path.join(ALIAS_DIR, alias_file), 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        process_alias_line(line)

def process_alias_line(line):
    parts = line.split('>>')
    if len(parts) != 2:
        return

    cmd_name = parts[0].strip()
    cmd_content = parts[1].strip()
    bat_file_name = f"{cmd_name}.bat"
    bat_path = os.path.join(BAT_DIR, bat_file_name)

    if os.path.exists(bat_path):
        response = input(f"Batch file '{bat_file_name}' already exists. Update it? (y/n): ")
        if response.lower() != 'y':
            return

    bat_content = (
        f"@echo off\n"
        f"{cmd_content}\n"
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

if __name__ == "__main__":
    process_alias_files()
    for file_name in os.listdir(PYTHON_DIR):
        if file_name.endswith(".py"):
            generate_bat_file(file_name)