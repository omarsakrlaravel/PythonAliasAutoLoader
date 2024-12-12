# Python Batch File Generator

A Python-based tool that automatically generates and manages batch files for your Python scripts and custom aliases. By running this utility, you can quickly create `.bat` files, making your Python scripts and aliases easily accessible from any directory on your system.

## Features

- **Global Access:** Run Python scripts and aliases from anywhere once the `.bat` files are in your PATH.
- **Automated Batch Generation:** Automatically create `.bat` files for Python scripts in a specified directory.
- **Custom Aliases:** Define custom aliases in `.txt` files and convert them into `.bat` files with a simple command.

## Prerequisites

- **Python:** Ensure that [Python](https://www.python.org/downloads/) is installed on your system.
- **PATH Setup:** Add the `d:/Python/bin/bat` directory to your system's PATH environment variable.  
  *If you change the directory paths, remember to update the code and instructions accordingly.*

## Directory Structure

```
d:/Python/bin/
├── bat/
│   ├── bat.py     # Main Python script for batch generation
│   └── bat.bat    # Executor script to trigger batch file creation
├── alias/
│   └── php.txt    # Alias definition files (one file per group of aliases)
└── *.py            # Your Python scripts
```

## Usage

1. **Add `bat` Directory to PATH**  
   Add `d:/Python/bin/bat` to your PATH so that generated batch files are accessible globally.

2. **Run the Generator**
   ```
   bat
   ```
   Execute `bat` (i.e., `bat.bat`) to:
   - Generate `.bat` files for each `.py` file in `d:/Python/bin`.
   - Convert aliases defined in `d:/Python/bin/alias` into corresponding `.bat` files.

4. **Create and Use Python Files**  
   Simply create a Python script (e.g., `tst.py`) in `d:/Python/bin`. After running `bat`, a corresponding `tst.bat` will be generated.  
   This means you can now run your script from any directory by typing:
   ```
   tst
   ```
   No need to specify the `.py` or `.bat` extension.

5. **Custom Aliases**  
   - In the `alias` directory, create a `.txt` file (e.g., `php.txt`).
   - Each line should follow the format:  
     ```
     alias_name >> command
     ```
   - For multiple commands, separate them using `>>`.

   **Example:**
   ```
   srv >> php artisan serve
   dev >> npm run dev
   ```

   After running `bat`, this creates `srv.bat` and `dev.bat` in the `bat` directory, allowing you to run `srv` or `dev` directly from any directory.

## Example

Consider you have `php.txt` in the `alias` folder with:
```
srv >> php artisan serve
dev >> npm run dev
```

Running `bat` will generate:
- `srv.bat` (executes `php artisan serve`)
- `dev.bat` (executes `npm run dev`)

Now, open a new command prompt. With `d:/Python/bin/bat` in your PATH, you can run:
```
srv
dev
```
These commands are now available globally.

## Important Note on Path Changes

If you move or rename directories, such as `d:/Python/bin`, be sure to:
- Update the constants `PYTHON_DIR`, `BAT_DIR`, and `ALIAS_DIR` in `bat.py`.
- Refresh your system's PATH to point to the correct `bat` directory.
- Re-run `bat` to regenerate the batch files with the new paths.

## Code Reference

Below is the main `bat.py` script used for generating batch files. Adjust the directory paths at the top if your setup differs.

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

    cmd_name = parts[0].strip()
    cmd_content = parts[1].strip()
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

**Enjoy streamlined access to your Python scripts and custom aliases!**
