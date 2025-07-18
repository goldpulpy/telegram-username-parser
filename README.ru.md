<div align="center">
  <h1>🤖 Telegram Username Parser</h1>

![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

</div>

<div align="center">
    <a href="/README.md">English</a> |
    <b>Русский</b>
</div>

## 📋 Обзор

Telegram username parser - инструмент, который извлекает username из каналов Telegram и истории сообщений. Он предоставляет эффективный способ сбора имен пользователей как из участников каналов, так и от авторов сообщений.

## ✨ Возможности

- 🔍 Извлечение имен пользователей из участников канала
- 📃 Парсинг имен пользователей из истории сообщений
- 💾 Сохранение результатов в файл
- 🔄 Предотвращение дубликатов в результатах
- 🔐 Использование Telegram API с управлением сессиями

## 🚀 Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/goldpulpy/telegram-username-parser.git
   cd telegram-username-parser
   ```

2. Установите зависимости используя Makefile:

   ```bash
   make setup
   ```

   Это создаст виртуальное окружение и установит все необходимые зависимости.

3. Настройте учетные данные Telegram API:
   - Отредактируйте `config.json` и добавьте:
     - `api_id`: Ваш Telegram API ID
     - `api_hash`: Ваш Telegram API hash
     - `phone`: Ваш номер телефона в международном формате

## 🛠️ Конфигурация

Создайте или отредактируйте файл `config.json`:

```json
{
  "api_id": ВАШ_API_ID,
  "api_hash": "ВАШ_API_HASH",
  "phone": "+ВАШ_НОМЕР_ТЕЛЕФОНА"
}
```

> ⚠️ **Примечание**: Чтобы получить `api_id` и `api_hash`, зарегистрируйте своё приложение на [https://my.telegram.org/apps](https://my.telegram.org/apps)

## 🖥️ Использование

Запустите основной скрипт:

```bash
source venv/bin/activate
python main.py
```

### Аргументы командной строки:

- `--config`: Путь к файлу конфигурации (по умолчанию: `config.json`)
- `--result_directory`: Путь для хранения результатов (по умолчанию: `result`)
- `--session_directory`: Путь для хранения сессий (по умолчанию: `sessions`)
- `--debug`: Включить режим отладки (опционально)

## 📊 Как это работает

1. Инструмент подключается к Telegram, используя ваши учетные данные
2. Запрашивает целевое username канала или чата
3. Сначала извлекает username из участников чата/канала
4. Затем анализирует историю сообщений для извлечения username авторов сообщений
5. Все уникальные имена пользователей сохраняются в файл (формат `@username`)

> ⚠️ **Примечание**: если сбор идет с канала, бот должен находиться в канале и иметь доступ к участникам.

## 🧩 Архитектура

Проект организован в несколько модулей:

| Модуль           | Описание                               |
| ---------------- | -------------------------------------- |
| `app/config.py`  | Функциональность загрузки конфигурации |
| `app/parser.py`  | Стратегии парсинга имен пользователей  |
| `app/result.py`  | Хранение и управление результатами     |
| `app/session.py` | Обработка сессий Telegram              |
| `main.py`        | Основная точка входа                   |

## 📝 Лицензия

Этот проект доступен по лицензии [MIT](LICENSE).

<h6 align="center">Created by goldpulpy with ❤️</h6>
