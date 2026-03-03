# Test Backend (FastAPI)

Простой тестовый бэкенд: время и дата сервера, фазы Луны (UTC+5), веб-интерфейс с кнопкой MOON.

## Запуск

Создайте виртуальное окружение и установите зависимости:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
# или: .venv\Scripts\activate  на Windows

pip install -r requirements.txt
uvicorn main:app --reload
```

Сервер будет доступен по адресу: http://127.0.0.1:8000

### Docker

```bash
docker build -t test-actions .
docker run -p 8000:8000 test-actions
```

## Эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/` | Приветствие, ссылки на docs и moon |
| GET | `/time` | Текущее время сервера (UTC, ISO и timestamp) |
| GET | `/date` | Текущая дата (UTC): date_iso, year, month, day, weekday |
| GET | `/date/iso` | Только дата в формате ISO (YYYY-MM-DD) |
| GET | `/moon/phase` | Фаза Луны по текущему времени UTC+5 (название и % освещённости) |
| GET | `/moon/next-new` | Ближайшие дата и время новолуния (UTC+5) |
| GET | `/moon/next-full` | Ближайшие дата и время полнолуния (UTC+5) |
| GET | `/health` | Проверка состояния сервиса |
| GET | `/ui` | Веб-интерфейс с кнопкой MOON вверху |
| GET | `/moon` | Страница с данными о Луне (фаза, ссылки на новолуние/полнолуние) |
| GET | `/docs` | Интерактивная документация Swagger UI |

## Интерфейс

- **/ui** — стартовая страница приложения с кнопкой **MOON** в верхней панели.
- **/moon** — страница «Луна»: текущая фаза (UTC+5) и ссылки на API новолуния и полнолуния.

## GitHub Actions (деплой)

Workflow `.github/workflows/deploy.yml` при пуше в `main` (или по кнопке):

1. **build-and-push** — сборка Docker-образа и пуш в GitHub Container Registry (`ghcr.io/<owner>/test-actions:latest`).
2. **deploy** — подключение по SSH к серверу, `docker login` в GHCR, `docker pull` и запуск контейнера `test-actions` на порту 8000.

### Секреты репозитория (Settings → Secrets and variables → Actions)

| Секрет | Описание |
|--------|----------|
| `SSH_HOST` | Адрес сервера (IP или домен) |
| `SSH_USER` | Пользователь SSH |
| `SSH_PRIVATE_KEY` | Приватный SSH-ключ (содержимое файла, без пароля) |
| `SSH_PORT` | Порт SSH (например `22`), опционально |
| `GHCR_USERNAME` | Логин GitHub (для `docker login ghcr.io`) |
| `GHCR_TOKEN` | Personal Access Token с правом `read:packages` (для доступа к образу с сервера) |

На сервере должны быть установлены Docker и настроенный доступ по SSH по ключу.

## Описание изменений

- **Время и дата:** эндпоинты `/time`, `/date`, `/date/iso` для времени и даты сервера в UTC.
- **Луна (UTC+5):** эндпоинты `/moon/phase`, `/moon/next-new`, `/moon/next-full`; расчёт через библиотеку `ephem`.
- **Веб-интерфейс:** страницы `/ui` и `/moon` с кнопкой MOON вверху и блоком с текущей фазой Луны.
- **Docker:** `Dockerfile` и `.dockerignore` для сборки образа без лишних файлов.
- **Прочее:** `.gitignore` (в т.ч. `.venv`), настройки Cursor (исключение `.venv` из watcher).
