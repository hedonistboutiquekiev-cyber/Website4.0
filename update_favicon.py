#!/usr/bin/env python3
"""
Скрипт для обновления favicon на всех HTML страницах сайта.
Заменяет существующие favicon ссылки на AlbaLogo.png и добавляет дополнительные варианты.
"""

import os
import re
from pathlib import Path

def update_html_file(file_path):
    """Обновляет favicon ссылки в HTML файле."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Паттерны для замены
        replacements = [
            # Замена SVG favicon
            (r'  <link rel="icon" type="image/svg\+xml" href="/favicon\.svg">', 
             r'  <link rel="icon" type="image/png" href="/assets/icons/AlbaLogo.png" sizes="32x32">'),
            
            # Замена PNG favicon (старый формат)
            (r'  <link rel="icon" type="image/png" href="/favicon\.png" sizes="32x32">', 
             r'  <link rel="icon" type="image/png" href="/assets/icons/AlbaLogo.png" sizes="32x32">'),
            
            # Замена apple-touch-icon (старый формат)
            (r'  <link rel="apple-touch-icon" href="/apple-touch-icon\.svg" sizes="180x180">',
             r'  <link rel="apple-touch-icon" href="/assets/icons/AlbaLogo.png" sizes="180x180">'),
        ]
        
        for old_pattern, new_pattern in replacements:
            content = re.sub(old_pattern, new_pattern, content)
        
        # Проверяем что контент изменился
        if content == original_content:
            return None
        
        # Пишем обновленный файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    
    except Exception as e:
        print(f"  Ошибка при обработке {file_path}: {e}")
        return False

def main():
    """Главная функция."""
    repo_root = Path('/workspaces/Website_3.0')
    
    # Находим все HTML файлы
    html_files = sorted(repo_root.rglob('*.html'))
    
    print(f"Найдено {len(html_files)} HTML файлов для обновления")
    print("=" * 80)
    
    updated = 0
    skipped = 0
    errors = 0
    
    for html_file in html_files:
        relative_path = html_file.relative_to(repo_root)
        result = update_html_file(str(html_file))
        
        if result is True:
            print(f"✓ Обновлен: {relative_path}")
            updated += 1
        elif result is False:
            print(f"✗ Ошибка: {relative_path}")
            errors += 1
        else:
            # Skipped (результат None)
            skipped += 1
    
    print("=" * 80)
    print(f"Результаты:")
    print(f"  ✓ Обновлено: {updated}")
    print(f"  - Пропущено: {skipped}")
    print(f"  ✗ Ошибок: {errors}")
    print(f"  Всего файлов: {len(html_files)}")

if __name__ == '__main__':
    main()
