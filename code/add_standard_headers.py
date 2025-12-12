#!/usr/bin/env python3
"""
Додає стандартні headers до всіх Python файлів
"""
import os
from pathlib import Path

STANDARD_HEADER = '''"""
Verification of Engineering Emergence (Jansma & Hoel, 2025)

Author: Oleksii Onasenko
Developer: SubstanceNet
"""
'''

def add_header_to_file(filepath):
    """Додає header якщо його немає"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Перевіряємо чи вже є header
    if 'Verification of Engineering Emergence' in content:
        print(f"  ✓ {filepath.name} - header exists")
        return False
    
    # Додаємо header
    new_content = STANDARD_HEADER + '\n' + content
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  + {filepath.name} - header added")
    return True

def main():
    print("="*70)
    print("ДОДАВАННЯ СТАНДАРТНИХ HEADERS")
    print("="*70)
    
    # Знаходимо всі Python файли
    code_dir = Path('code')
    data_dir = Path('data')
    
    python_files = []
    python_files.extend(code_dir.glob('*.py'))
    python_files.extend(data_dir.glob('*.py'))
    
    print(f"\nЗнайдено {len(python_files)} Python файлів\n")
    
    added = 0
    for filepath in sorted(python_files):
        if add_header_to_file(filepath):
            added += 1
    
    print(f"\n{'='*70}")
    print(f"ЗАВЕРШЕНО: Додано headers до {added} файлів")
    print("="*70)

if __name__ == "__main__":
    main()
