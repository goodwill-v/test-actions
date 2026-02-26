# Test Backend (FastAPI)

Простой тестовый бэкенд, возвращающий текущее время сервера.

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

## Эндпоинты

- **GET /** — приветствие и ссылка на документацию
- **GET /time** — текущее время сервера (UTC, ISO и timestamp)
- **GET /health** — проверка состояния сервиса
- **GET /docs** — интерактивная документация Swagger UI
