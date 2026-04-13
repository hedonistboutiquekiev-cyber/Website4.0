# 🎤 Albamen Voice Chat - Улучшенная версия

## Что улучшено

### 1. **Улучшенная обработка ошибок** ✅
- Добавлены информативные сообщения об ошибках
- Поддержка timeout для запросов к Worker (15 сек)
- Обработка ошибок микрофона и браузера
- Эмодзи для лучшей визуализации статуса

### 2. **Комплексное логирование** 📋
- Все действия логируются в консоль для отладки
- Включается автоматически в режиме development
- Помогает диагностировать проблемы

### 3. **Лучшая инициализация** 🔧
- Надежное обнаружение DOM элементов
- Observer для динамически загружаемых виджетов
- Безопасная обработка исключений
- Предотвращение множественной инициализации

### 4. **Улучшенный синтез речи** 🔊
- Отмена предыдущего воспроизведения
- Оптимизированная скорость произношения
- Обработка ошибок синтеза

### 5. **Диагностический инструмент** 🛠️
- Файл `voice-diagnostics.js` для проверки работоспособности
- Проверка браузерных API
- Тестирование соединения с Worker
- Проверка микрофона и синтеза речи

---

## Использование диагностики

Откройте консоль браузера (F12) и используйте:

```javascript
// Полная диагностика
VoiceDiagnostics.runFullDiagnostics()

// Отдельные проверки
VoiceDiagnostics.checkDOMElements()           // Проверка элементов
VoiceDiagnostics.checkAPIs()                  // Проверка API браузера
VoiceDiagnostics.checkWorkerConnection()      // Проверка воркера
VoiceDiagnostics.testMicrophone()             // Тест микрофона
VoiceDiagnostics.testSpeechSynthesis()        // Тест синтеза речи
VoiceDiagnostics.checkStorage()               // Проверка localStorage
VoiceDiagnostics.help()                       // Справка
```

---

## Структура файлов

### Основные файлы голосового чата:

- **`assets/js/script.js`** - Главный скрипт логики голосового чата (улучшен)
- **`assets/js/voice-diagnostics.js`** - Диагностический инструмент (новый)
- **`assets/js/include.js`** - Подключение виджетов и скриптов
- **`assets/css/site.css`** - Стили для виджетов

### Удалены:
- **`assets/css/script.js`** - Старый конфликтующий файл (удален)

---

## Логирование

Все сообщения для отладки выводятся в консоль с префиксом:
```
[Albamen Voice HH:MM:SS]
```

Примеры логов:
```
[Albamen Voice 14:30:45] Initializing voice handlers...
[Albamen Voice 14:30:45] Elements found: {voiceButtons: 1, voiceModal: true, ...}
[Albamen Voice 14:30:46] Voice button clicked (index 0)
[Albamen Voice 14:30:47] Sending transcript to worker: Merhaba...
[Albamen Voice 14:30:48] Worker response received: {reply: "Merhaba, hoş geldin!"}
```

---

## Обработка ошибок

### Возможные сообщения об ошибках:

| Ошибка | Причина | Решение |
|--------|---------|--------|
| ❌ Tarayıcınız ses tanımadı desteklemiyor | Browser не поддерживает SpeechRecognition | Используйте Chrome, Edge, Firefox |
| 🔇 Ses algılanmadı | Микрофон не слышит голос | Проверьте микрофон, говорите громче |
| ❌ Ağ hatası | Проблема с интернетом | Проверьте соединение |
| ⏱️ Albamen cevap vermedi | Worker не ответил | Проверьте URL воркера в script.js |
| 🎤 Mikrofon sorunu | Проблема с микрофоном | Проверьте разрешения браузера |
| 🔒 Mikrofon izni reddedildi | Доступ к микрофону заблокирован | Разрешите доступ в настройках браузера |

---

## Проверка Worker

Worker URL настроен в `script.js` строка 2:
```javascript
const VOICE_WORKER_URL = 'https://albamen-voice.nncdecdgc.workers.dev';
```

Для проверки работоспособности используйте:
```javascript
VoiceDiagnostics.checkWorkerConnection()
```

---

## Основные функции в script.js

### `initVoiceHandlers()`
Инициализация всех обработчиков голосового чата.

### `sendTextToWorker(transcript)`
Отправка распознанного текста на Worker с обработкой timeout.

### `speakReply(text)`
Синтез речи для ответа от Albamen.

### `getVoiceIdentity()`
Получение информации о сессии пользователя.

---

## Требования к браузеру

- ✅ **Chrome/Chromium** 25+
- ✅ **Firefox** 25+
- ✅ **Safari** 14.1+
- ✅ **Edge** 79+
- ❌ **Internet Explorer** - не поддерживается

**Требует:**
- HTTPS соединение
- Разрешение на доступ к микрофону
- Поддержка Web Speech API

---

## Известные ограничения

1. **Только HTTPS** - Web Speech API работает только по защищенному соединению
2. **Один язык** - Настроен на турецкий (tr-TR), можно изменить в script.js
3. **Timeout 15 сек** - Если Worker не ответит за 15 секунд, запрос отменяется
4. **Синтез речи** - Зависит от браузера и установленных голосов

---

## Примеры кода для интеграции

### Вручную открыть голосовой чат
```javascript
const voiceModal = document.querySelector('.ai-panel-voice');
if (voiceModal) voiceModal.classList.add('ai-open');
```

### Проверить, открыт ли голосовой чат
```javascript
const voiceModal = document.querySelector('.ai-panel-voice');
const isOpen = voiceModal?.classList.contains('ai-open') || false;
```

### Закрыть голосовой чат
```javascript
const voiceModal = document.querySelector('.ai-panel-voice');
if (voiceModal) voiceModal.classList.remove('ai-open');
```

### Получить идентификацию пользователя
```javascript
const identity = window.albamenVoiceIdentity;
console.log('User:', identity.name, 'Age:', identity.age);
```

---

## Поддержка

Для отладки используйте:
1. **Консоль браузера** (F12) - смотрите логи
2. **VoiceDiagnostics** - запустите полную диагностику
3. **Network tab** - проверьте запросы к Worker
4. **Sources/Debugger** - установите breakpoints в script.js

---

## История версий

### v2.0 (Текущая) - Январь 2026
- ✅ Комплексная обработка ошибок
- ✅ Расширенное логирование
- ✅ Диагностический инструмент
- ✅ Улучшенная инициализация
- ✅ Удален конфликтующий файл в css папке

### v1.0 - Базовая версия
- Базовая функциональность голосового чата
- Web Speech API интеграция
- REST API для обработки
