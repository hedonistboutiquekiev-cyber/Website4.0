# Git Setup Instructions for AlbaSpace Website

## Измененные файлы (готовы к коммиту):

### 1. Исправление модального окна регистрации:
- `assets/includes/signup-modal.html` - Исправлен z-index и видимость модального окна

### 2. Выравнивание галерей продуктов (соответствие турецким шаблонам):

#### Hoodie продукты:
- `rus/product-hoodie.html` - Удалено лишнее изображение
- `eng/product-hoodie.html` - Удалены placeholder и лишнее изображение

#### Shirt продукты:
- `rus/product-shirt.html` - Удалено лишнее изображение shirt4.png
- `eng/product-shirt.html` - Удалены placeholder-logo2.jpg и лишнее изображение

#### Stanley продукты:
- `rus/product-stanley.html` - Удалено лишнее изображение stanley4.png
- `eng/product-stanley.html` - Удалены placeholder-logo3.jpg и лишнее изображение

#### Hat продукты:
- `eng/product-hat.html` - Удалены placeholder-logo8.jpg и лишнее изображение hat4.png

### 3. Подготовительные файлы:
- `.gitignore` - Создан для игнорирования ненужных файлов

## Команды для выполнения (на вашем компьютере):

```bash
# 1. Установить Git (если еще не установлен)
# Скачать с: https://git-scm.com/

# 2. Инициализировать репозиторий
git init

# 3. Добавить все файлы
git add .

# 4. Сделать коммит
git commit -m "Fix registration modal visibility and align product galleries across languages

- Fixed z-index stacking issue for registration popup across all language versions
- Aligned product gallery structures to match Turkish reference templates
- Removed placeholder images and extra gallery items from Russian and English pages
- Ensured consistent gallery button counts across hoodie, shirt, stanley, and hat products"

# 5. Добавить удаленный репозиторий (замените на ваш URL)
git remote add origin https://github.com/your-username/your-repo.git

# 6. Сделать push
git push -u origin main
```

## Примечания:
- Русская версия страницы дракона уже соответствует турецкой
- Английская версия дракона пустая (возможно, требуется создание)
- Все галереи теперь имеют одинаковую структуру в трех языковых версиях