# Python Imports Extractor

A Python script that scans a specified directory for Python files, extracts all the `import` statements, and generates a `requirements.txt` file containing all the unique dependencies used across those files.

## Features

- Recursively scans a directory for `.py` files.
- Extracts both `import` and `from ... import` statements.
- Saves all unique imports in a `requirements.txt` file.
- Handles common errors such as missing directories or unreadable files.

## Usage
- Run the script by providing a directory path as an argument:

```bash
python main.py /path/to/your/directory
```
