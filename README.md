# Email Marketing Platform

Веб-сервис на Django для управления email-рассылками: клиенты, сообщения, кампании, попытки отправки, статистика и система ролей.

**GitHub:** https://github.com/moldique/Email-Marketing-Platform

## Установка и настройка

### Требования
- Python 3.13+
- Poetry
- PostgreSQL 13+
- Redis 6+
- Аккаунт Mail.ru с паролем приложения (SMTP)

### Установка проекта

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/moldique/Email-Marketing-Platform.git
   cd Email-Marketing-Platform
   ```

2. Установите Poetry (если ещё не установлен):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Установите зависимости:
   ```bash
   poetry install
   ```

4. Активируйте виртуальное окружение:
   ```bash
   poetry shell
   ```

5. Создайте файл переменных окружения на основе примера:
   ```bash
   copy .env.exemple .env   # Windows
   cp .env.exemple .env     # Linux / macOS
   ```

6. Заполните `.env` (пример значений):
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost

   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432

   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.mail.ru
   EMAIL_PORT=465
   EMAIL_USE_TLS=False
   EMAIL_USE_SSL=True
   EMAIL_HOST_USER=your@mail.ru
   EMAIL_HOST_PASSWORD=mailru_app_password
   DEFAULT_FROM_EMAIL=your@mail.ru

   REDIS_URL=redis://127.0.0.1:6379/1
   ```

### Подготовка базы данных и запуск

```bash
# Применение миграций
poetry run python manage.py migrate

# Создание суперпользователя
poetry run python manage.py createsuperuser

# Создание группы «Менеджеры» и назначение прав
poetry run python manage.py create_managers_group

# Запуск Redis (пример для Windows)
"D:\program\python\redis\Redis-x64-3.0.504\redis-server.exe"

# Запуск сервера разработки
poetry run python manage.py runserver
```

После запуска проект доступен по адресу http://127.0.0.1:8000/.

## Разработка

```bash
# Установка зависимостей с dev-группой (если нужна)
poetry install --with dev

# Запуск тестов (при наличии)
poetry run python manage.py test

# Проверка код-стайла (если flake8 добавлен)
poetry run flake8
```

## Структура проекта

```
Email-Marketing-Platform/
├── config/
│   ├── settings.py               # Настройки проекта
│   └── urls.py                   # Основные URL-ы
├── mailings/
│   ├── models.py                 # Recipient, Message, MailingList, MailingAttempt
│   ├── views.py                  # CRUD, статистика, отправка, кеширование
│   ├── urls.py
│   └── management/
│       └── commands/
│           └── create_managers_group.py
├── user/
│   ├── models.py                 # Кастомный пользователь (email-логин, аватар, телефон, страна)
│   ├── forms.py                  # Регистрация, авторизация, профиль
│   ├── views.py                  # Регистрация, вход, выход, профиль, подтверждение email
│   └── urls.py
├── mailings/templates/           # Шаблоны (базовый layout, страницы приложения)
├── manage.py
├── pyproject.toml
├── README.md
└── .env.exemple
```

## Функциональность

- ✅ CRUD для получателей, сообщений и рассылок (привязка к владельцу)
- ✅ Кастомная модель пользователя с авторизацией по email, аватаром, телефоном и страной
- ✅ Регистрация с подтверждением email, вход, выход, профиль, сброс пароля
- ✅ Ручная отправка рассылок с логированием попыток (успешно/неуспешно, ответ сервера)
- ✅ Главная страница с агрегированной статистикой (всего рассылок, активных, уникальных получателей)
- ✅ Страница детальной статистики (успешные/неуспешные попытки, количество отправленных сообщений)
- ✅ Ролевая модель: пользователи управляют своими данными, менеджеры видят всё
- ✅ Серверное кеширование (Redis + `cache_page`), выставление заголовков `Cache-Control`
- ✅ Группа «Менеджеры» создаётся management-командой и получает необходимые права

## Работа с почтой

1. Создайте в Mail.ru пароль приложения (опция «Только отправка писем»).
2. Пропишите реквизиты SMTP в `.env`.
3. Функция `send_verification_email` использует `django.core.mail.send_mail` и отправляет пользователю ссылку подтверждения.

## Кеширование

- Используется `django-redis` и Redis (по умолчанию база 1).
- Страницы `/` и `/statistics/` кешируются на 5 минут.
- Проверка ключей: `redis-cli -n 1 keys "*"`.

## Дополнительно

Дополнительные задания (автопланирование рассылок, расширенное логирование) не реализованы.

## Системные требования

- Python 3.13+
- PostgreSQL
- Redis
- Mail.ru (SMTP с паролем приложения)
- Poetry для управления зависимостями