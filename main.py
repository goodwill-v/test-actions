from datetime import datetime, timezone
from fastapi import FastAPI

app = FastAPI(title="Test Backend", description="Простой тестовый бэкенд с временем сервера")


@app.get("/")
def root():
    """Корневой эндпоинт."""
    return {"message": "Test Backend", "docs": "/docs"}


@app.get("/time")
def get_server_time():
    """Возвращает текущее время сервера в UTC и ISO формате."""
    now = datetime.now(timezone.utc)
    return {
        "time_utc": now.isoformat(),
        "timestamp": now.timestamp(),
    }


@app.get("/health")
def health():
    """Проверка состояния сервиса."""
    return {"status": "ok"}
