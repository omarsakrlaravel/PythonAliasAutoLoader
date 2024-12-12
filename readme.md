# Python Batch File Generator

This tool allows you to quickly generate batch (`.bat`) files for Python scripts and custom commands, enabling you to run them effortlessly from any directory. With this setup, you can simplify running Python scripts or commands by using short, customizable aliases.

---

## What It Does

1. **Global Access:** Once `.bat` files are added to your system's PATH, you can run Python scripts and aliases globally, without specifying full paths.
2. **Batch File Automation:** Automatically generate `.bat` files for Python scripts in a specified directory.
3. **Custom Aliases:** Convert custom commands (like `php artisan serve`) into `.bat` files with aliases you define.
4. **Argument Passing:** Pass arguments to your aliases (e.g., `srv 8080 --host=192.168.1.1`) and forward them to the underlying command seamlessly.

---

## Directory Setup

Assume the following directory structure:

```
d:/Python/bin/
├── bat/
│   ├── bat.py     # Main Python script for generating batch files
│   └── bat.bat    # Shortcut batch file for running bat.py
├── alias/
│   └── php.txt    # Alias definition files
└── *.py            # Your Python scripts
```

### Key Folders:
- **`d:/Python/bin`**: Contains Python scripts.
- **`d:/Python/bin/bat`**: Stores generated `.bat` files.
- **`d:/Python/bin/alias`**: Stores custom alias definitions in `.txt` files.

---

## How to Use

### Step 1: Add the `bat` Directory to PATH
Add `d:/Python/bin/bat` to your system's PATH environment variable. This ensures that any `.bat` file in this folder can be executed globally.

### Step 2: Run the Generator
Run the `bat` utility (via `bat.bat` or `bat.py`). This script:
1. Creates `.bat` files for all `.py` scripts in `d:/Python/bin`.
2. Processes custom aliases defined in `d:/Python/bin/alias` and generates `.bat` files for them.

Example command to execute:
```bash
bat
```

### Step 3: Use Your Scripts
Once `.bat` files are generated, you can run your Python scripts or aliases directly from any directory.

#### Python Script Example:
A script named `tst.py` in `d:/Python/bin` will generate `tst.bat`.  
Now, you can run it from anywhere:
```bash
tst
```

---

## Custom Aliases: How They Work

### Defining Aliases
To create aliases, add them to `.txt` files in the `alias` folder (e.g., `php.txt`). Each line should follow this format:
```
command >> alias
```

- **`command`**: The full command you want to alias.
- **`alias`**: The short name you will use to execute it.

#### Example Alias File: `php.txt`
```text
php artisan serve --port=$1 >> srv
npm run dev >> dev
```

### What This Does
1. `srv`: Runs `php artisan serve` and passes any arguments you provide.
2. `dev`: Runs `npm run dev`.

### Generated Batch Files
- **`srv.bat`**:
  ```cmd
  @echo off
  php artisan serve --port=%1 %*
  ```
  When you run:
  ```bash
  srv 8080 --host=192.168.1.1
  ```
  It translates to:
  ```bash
  php artisan serve --port=8080 --host=192.168.1.1
  ```

- **`dev.bat`**:
  ```cmd
  @echo off
  npm run dev %*
  ```
  This simply runs `npm run dev`.

---

### How `srv 8080 --host=192.168.1.1` Works

1. **Command Input:**  
   When you type:
   ```bash
   srv 8080 --host=192.168.1.1
   ```
   - `srv` is the alias for the `php artisan serve` command.
   - `8080` is assigned to `$1` (first argument), which maps to `%1` in the batch file.
   - `--host=192.168.1.1` is passed as additional arguments (`%*`).

2. **Execution in Batch File:**  
   The generated `srv.bat` contains:
   ```cmd
   @echo off
   php artisan serve --port=%1 %*
   ```
   - `%1` is replaced by `8080`.
   - `%*` includes everything after `8080`, i.e., `--host=192.168.1.1`.

3. **Final Command:**  
   The batch file runs:
   ```bash
   php artisan serve --port=8080 --host=192.168.1.1
   ```

---

## Key Features

1. **Argument Passing**:  
   Use `$1`, `$2`, etc., in aliases for positional arguments. These are converted to `%1`, `%2`, etc., in the batch file.

2. **Dynamic Commands**:  
   Add flexibility to your aliases by supporting arguments and optional parameters.

3. **Global Execution**:  
   After adding the `bat` folder to PATH, run scripts or aliases from any directory.

---

## Main Script: `bat.py`

This script handles batch file generation for both Python scripts and aliases. Adjust the directory paths (`PYTHON_DIR`, `BAT_DIR`, `ALIAS_DIR`) as needed.

```python
import os

PYTHON_DIR = "d:/Python/bin"
BAT_DIR = "d:/Python/bin/bat"
ALIAS_DIR = "d:/Python/bin/alias"

override_all = False

def process_alias_files():
    for alias_file in os.listdir(ALIAS_DIR):
        if alias_file.endswith('.txt'):
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

    for i in range(1, 10):
        cmd_content = cmd_content.replace(f"${i}", f"%{i}")

    bat_content = (
        f"@echo off\n"
        f"{cmd_content} %*\n"
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
```

---

**Simplify your workflow with easy access to scripts and custom commands!**