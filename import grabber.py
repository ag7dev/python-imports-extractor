import os
import sys
import ast
from pathlib import Path
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)

PYPI_MAPPING = {
    'PIL': 'Pillow',
    'bs4': 'beautifulsoup4',
    'yaml': 'PyYAML',
    'discord': 'discord.py'
}

def extract_imports(file_path: Path) -> tuple[set[str], list[str]]:
    """Extracts all imports from a Python file"""
    imports = set()
    errors = []
    
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return imports, [f"Read error: {e}"]

    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        return imports, [f"Syntax error: {e}"]
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                base_pkg = alias.name.split('.')[0]
                imports.add(base_pkg)
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.level == 0:  # Ignores relative imports
                base_pkg = node.module.split('.')[0]
                imports.add(base_pkg)

    return imports, errors

def main():
    if len(sys.argv) < 2:
        print(f"{Fore.RED}Usage: {sys.argv[0]} <Directory or File>{Style.RESET_ALL}")
        sys.exit(1)

    target = Path(sys.argv[1]).resolve()
    
    if not target.exists():
        print(f"{Fore.RED}Path does not exist: {target}{Style.RESET_ALL}")
        sys.exit(1)

    # Handle both directories and single files
    if target.is_file():
        if target.suffix != '.py':
            print(f"{Fore.RED}Not a Python file: {target}{Style.RESET_ALL}")
            sys.exit(1)
        py_files = [target]
        base_path = target.parent
    else:
        py_files = list(target.rglob("*.py"))
        base_path = target

    if not py_files:
        print(f"{Fore.YELLOW}No Python files found{Style.RESET_ALL}")
        sys.exit()

    print(f"{Fore.CYAN}Processing {len(py_files)} files...{Style.RESET_ALL}")
    
    all_imports = set()
    error_count = 0

    for idx, file in enumerate(py_files, 1):
        print(f"{Fore.BLUE}[{idx}/{len(py_files)}] {file.relative_to(base_path)}", end='\r')
        
        imports, errors = extract_imports(file)
        
        if errors:
            error_count += 1
            print(f"\n{Fore.RED}Error in {file}:{Style.RESET_ALL}")
            print('\n'.join(f"  {e}" for e in errors))
        
        for pkg in imports:
            mapped_pkg = PYPI_MAPPING.get(pkg, pkg)
            all_imports.add(mapped_pkg)

    if all_imports:
        with open('requirements.txt', 'w') as f:
            f.write('\n'.join(sorted(all_imports)))
            
        print(f"\n{Fore.GREEN}requirements.txt created with {len(all_imports)} packages")
        print(f"{Fore.CYAN}Packages: {', '.join(sorted(all_imports))}")
    else:
        print(f"{Fore.YELLOW}No imports found{Style.RESET_ALL}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Aborted{Style.RESET_ALL}")
        sys.exit(1)