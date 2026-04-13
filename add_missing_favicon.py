#!/usr/bin/env python3
"""
Финальный скрипт для добавления favicon во все HTML файлы, которые их не имеют.
"""

import re
from pathlib import Path

FAVICON_LINKS = """  <link rel="icon" type="image/png" href="/assets/icons/AlbaLogo.png" sizes="32x32">
  <link rel="apple-touch-icon" href="/assets/icons/AlbaLogo.png" sizes="180x180">"""

def add_favicon_to_html(content):
    """Добавляет favicon ссылки в head секцию."""
    # Проверяем есть ли уже favicon ссылки
    if re.search(r'rel="icon"', content) or re.search(r'rel="apple-touch-icon"', content):
        return None  # Favicon ссылки уже есть
    
    # Ищем head тег
    head_match = re.search(r'<head[^>]*>', content, re.IGNORECASE)
    if not head_match:
        return None  # Нет head тега
    
    # Вставляем favicon ссылки после head тега
    insert_pos = head_match.end()
    new_content = content[:insert_pos] + '\n' + FAVICON_LINKS + content[insert_pos:]
    return new_content

def update_html_file(file_path):
    """Добавляет favicon в HTML файл."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Пропускаем пустые файлы
        if len(content.strip()) < 100:
            return 'empty'
        
        original_content = content
        
        # Добавляем favicon если их нет
        new_content = add_favicon_to_html(content)
        
        if not new_content:
            return None  # Favicon уже есть или нет head
        
        # Пишем обновленный файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    
    except Exception as e:
        return f'error: {e}'

def main():
    """Главная функция."""
    repo_root = Path('/workspaces/Website_3.0')
    
    # Находим все HTML файлы
    html_files = sorted(repo_root.rglob('*.html'))
    
    print(f"Пополнение favicon для остальных HTML файлов")
    print("=" * 80)
    
    added = 0
    skipped = 0
    empty = 0
    errors = 0
    
    for html_file in html_files:
        relative_path = html_file.relative_to(repo_root)
        result = update_html_file(str(html_file))
        
        if result is True:
            print(f"✓ Добавлен favicon: {relative_path}")
            added += 1
        elif result == 'empty':
            empty += 1
        elif result and result.startswith('error'):
            print(f"✗ {result}: {relative_path}")
            errors += 1
        else:
            skipped += 1
    
    print("=" * 80)
    print(f"Результаты:")
    print(f"  ✓ Добавлен favicon: {added}")
    print(f"  - Пропущено (уже есть): {skipped}")
    print(f"  - Пустые файлы: {empty}")
    print(f"  ✗ Ошибок: {errors}")

if __name__ == '__main__':
    main()
