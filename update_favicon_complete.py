#!/usr/bin/env python3
"""
Улучшенный скрипт для обновления favicon на всех HTML страницах сайта.
1. Заменяет существующие favicon ссылки на AlbaLogo.png
2. Добавляет favicon ссылки в файлы, где их нет
"""

import re
from pathlib import Path

FAVICON_LINKS = """  <link rel="icon" type="image/png" href="/assets/icons/AlbaLogo.png" sizes="32x32">
  <link rel="apple-touch-icon" href="/assets/icons/AlbaLogo.png" sizes="180x180">"""

def add_favicon_to_head(content):
    """Добавляет favicon ссылки в head секцию, если их нет."""
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

def update_favicon_in_head(content):
    """Обновляет существующие favicon ссылки."""
    changed = False
    
    # 1. Заменяем SVG favicon на PNG
    if re.search(r'<link rel="icon" type="image/svg\+xml" href="/favicon\.svg">', content):
        content = re.sub(
            r'<link rel="icon" type="image/svg\+xml" href="/favicon\.svg">',
            r'  <link rel="icon" type="image/png" href="/assets/icons/AlbaLogo.png" sizes="32x32">',
            content
        )
        changed = True
    
    # 2. Заменяем старый PNG favicon
    if re.search(r'<link rel="icon" type="image/png" href="/favicon\.png"', content):
        content = re.sub(
            r'<link rel="icon" type="image/png" href="/favicon\.png"[^>]*>',
            r'  <link rel="icon" type="image/png" href="/assets/icons/AlbaLogo.png" sizes="32x32">',
            content
        )
        changed = True
    
    # 3. Заменяем apple-touch-icon на старый путь
    if re.search(r'href="/apple-touch-icon', content):
        content = re.sub(
            r'<link rel="apple-touch-icon" href="/apple-touch-icon[^"]*"[^>]*>',
            r'  <link rel="apple-touch-icon" href="/assets/icons/AlbaLogo.png" sizes="180x180">',
            content
        )
        changed = True
    
    return content if changed else None

def update_html_file(file_path):
    """Обновляет favicon ссылки в HTML файле."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Сначала пытаемся обновить существующие favicon ссылки
        updated = update_favicon_in_head(content)
        
        if updated:
            content = updated
        else:
            # Если нет favicon ссылок для обновления, добавляем новые
            added = add_favicon_to_head(content)
            if added:
                content = added
        
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
            skipped += 1
    
    print("=" * 80)
    print(f"Результаты:")
    print(f"  ✓ Обновлено: {updated}")
    print(f"  - Пропущено: {skipped}")
    print(f"  ✗ Ошибок: {errors}")
    print(f"  Всего файлов: {len(html_files)}")

if __name__ == '__main__':
    main()
