# Python Batch File Generator

A Python-based tool that automatically generates and manages batch files for your Python scripts and custom aliases. By running this utility, you can quickly create `.bat` files, making your Python scripts and aliases easily accessible from any directory on your system.

## Features

- **Global Access:** Run Python scripts and aliases from anywhere once the `.bat` files are in your PATH.
- **Automated Batch Generation:** Automatically create `.bat` files for Python scripts in a specified directory.
- **Custom Aliases with Arguments:** Define aliases that can accept arguments. For example, `$1`, `$2` in your alias commands will be converted to `%1`, `%2` in the resulting `.bat` file, allowing you to pass parameters directly to your aliases.
- **Command-Line Options:**  
  - `-f` (force override): Automatically override existing `.bat` files without prompting.  
  - `-c` (clean): Remove all `.bat` files in the batch directory (except `bat.py` and `bat.bat`) before generating new ones.

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

2. **Generate Batch Files**  
   Run `bat` (i.e., `bat.bat`) to:
   - Generate `.bat` files for each `.py` file in `d:/Python/bin`.
   - Convert aliases defined in `d:/Python/bin/alias` into corresponding `.bat` files.

3. **Command-Line Arguments**  
   - **Force Override (-f):**  
     If you want to overwrite existing `.bat` files without any prompts, run:  
     ```
     bat -f
     ```
   - **Clean (-c):**  
     To remove existing `.bat` files (except `bat.py` and `bat.bat`) before generating new ones, run:  
     ```
     bat -c
     ```
     You can combine both flags:  
     ```
     bat -c -f
     ```

4. **Passing Arguments to Python Scripts and Aliases**  
   - For Python scripts, you can simply append arguments after the command:
     ```
     script_name arg1 arg2
     ```
   - For aliases, define placeholders `$1`, `$2`, etc. in your alias command. These will be replaced with `%1`, `%2` in the generated `.bat` file. For example:
     ```
     myalias >> some_command $1 $2
     ```
     After generation, you can run:
     ```
     myalias value_1 value_2
     ```
     The alias will receive these values as arguments.

5. **Create and Use Python Files**  
   Place a Python script (e.g., `tst.py`) in `d:/Python/bin`. After running `bat` with or without flags, a corresponding `tst.bat` will be generated.  
   You can then run your script from any directory by typing:
   ```
   tst
   ```
   No need to specify the `.py` or `.bat` extension.

6. **Custom Aliases**  
   - In the `alias` directory, create a `.txt` file (e.g., `php.txt`).
   - Each line should follow the format:  
     ```
     command >> alias_name
     ```
     *Note:* The order here is `command >> alias_name`.  
   
   **Example:**
   ```
   php artisan serve >> srv
   npm run dev >> dev
   ```
   
   After running `bat`, this creates `srv.bat` and `dev.bat`, allowing you to run `srv` or `dev` from anywhere.

## Example

If `php.txt` contains:
```
php artisan serve >> srv
npm run dev >> dev
```

Running `bat -f` (force override) will generate:
- `srv.bat` (executes `php artisan serve`)
- `dev.bat` (executes `npm run dev`)

Now, with `d:/Python/bin/bat` in your PATH, you can run:
```
srv
dev
```
These commands are available globally. Add arguments as needed if you defined `$1`, `$2`, etc.

## Important Note on Path Changes

If you move or rename directories, such as `d:/Python/bin`, be sure to:
- Update the directory constants in the script.
- Refresh your system's PATH to point to the correct `bat` directory.
- Re-run `bat` (with or without flags) to regenerate the batch files with the new paths.

---

**Enjoy streamlined access to your Python scripts, custom aliases, and easy argument passing!**