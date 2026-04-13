#!/usr/bin/env python3
"""
Умная замена "AlbaSpace" на "Alba Space" только в SEO полях и текстовом контенте.
Исключает: переменные, ID, API URL-ы, имена файлов, URL-ы.
"""

import re
from pathlib import Path

def should_replace_albaspace(match, before_text, after_text):
    """Определяет должна ли быть выполнена замена в данном контексте."""
    matched_text = match.group(0)
    
    # Не заменяем в:
    # 1. ID атрибутах (id="...")
    if re.search(r'id="[^"]*' + re.escape(matched_text) + r'[^"]*"', before_text + matched_text + after_text):
        return False
    
    # 2. data- атрибутах
    if re.search(r'data-[a-z-]*="[^"]*' + re.escape(matched_text), before_text):
        return False
    
    # 3. URL-ах и путях (albaspace.com, albaspace-api, etc)
    if re.search(r'(https?://|albaspace-|albaspace\.)', before_text[-50:] + matched_text + after_text[:50]):
        return False
    
    # 4. Переменных JavaScript
    if re.search(r'(const|let|var)\s+.*' + re.escape(matched_text), before_text[-100:]):
        return False
    
    # 5. Имён классов CSS
    if re.search(r'class=["\']([^"\']*' + re.escape(matched_text) + '[^"\']*)["\']', before_text[-50:] + matched_text):
        return False
    
    return True

def replace_in_seo_fields(content):
    """Заменяет AlbaSpace на Alba Space только в SEO полях."""
    # Сначала обработаем title теги
    content = re.sub(
        r'<title>([^<]*?)AlbaSpace(\s*[^<]*?</title>)',
        r'<title>\1Alba Space\2',
        content,
        flags=re.IGNORECASE
    )
    
    # Обработаем meta description
    content = re.sub(
        r'(content=["\'])([^"\']*?)AlbaSpace([^"\']*?["\'])',
        r'\1\2Alba Space\3',
        content,
        flags=re.IGNORECASE
    )
    
    # Обработаем текстовый контент в p, span, div тегах (но не в атрибутах)
    content = re.sub(
        r'(>)([^<]*?)AlbaSpace([^<]*?)(<)',
        lambda m: m.group(1) + m.group(2).replace('alba Space', 'Alba Space').replace('AlbaSpace', 'Alba Space') + m.group(3) + m.group(4),
        content,
        flags=re.IGNORECASE
    )
    
    # Обработаем text nodes между тегами
    content = re.sub(
        r'(?<![a-zA-Z0-9_-])AlbaSpace(?![a-zA-Z0-9_.-])',
        'Alba Space',
        content
    )
    
    return content

def process_file(file_path):
    """Обрабатывает один HTML файл."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        
        # Заменяем AlbaSpace на Alba Space в SEO полях
        content = replace_in_seo_fields(content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return None
    except Exception as e:
        print(f"  Ошибка в {file_path}: {e}")
        return False

def main():
    repo_root = Path('/workspaces/Website_3.0')
    
    # Находим все HTML, JSON и JS файлы
    html_files = list(repo_root.rglob('*.html'))
    json_files = list(repo_root.rglob('*.json'))
    js_files = list(repo_root.rglob('*.js'))
    
    all_files = html_files + json_files + js_files
    
    print(f"Обработка {len(all_files)} файлов...")
    print("=" * 80)
    
    updated = 0
    skipped = 0
    errors = 0
    
    for file_path in sorted(all_files):
        # Пропускаем node_modules и .git
        if 'node_modules' in str(file_path) or '.git' in str(file_path):
            continue
        
        result = process_file(file_path)
        
        if result is True:
            relative_path = file_path.relative_to(repo_root)
            print(f"✓ Обновлен: {relative_path}")
            updated += 1
        elif result is False:
            errors += 1
        else:
            skipped += 1
    
    print("=" * 80)
    print(f"Результаты:")
    print(f"  ✓ Обновлено файлов: {updated}")
    print(f"  - Без изменений: {skipped}")
    print(f"  ✗ Ошибок: {errors}")

if __name__ == '__main__':
    main()
