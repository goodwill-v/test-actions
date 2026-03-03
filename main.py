from datetime import datetime, timezone
from fastapi import FastAPI

app = FastAPI(title="Test Backend", description="Простой тестовый бэкенд с временем сервера.ПЛАНИРУЕТСЯ ТЕСТИРОВАНИЕ")


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


@app.get("/date")
def get_server_date():
    """Возвращает текущую дату сервера в UTC."""
    now = datetime.now(timezone.utc)
    return {
        "date_iso": now.date().isoformat(),
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "weekday": now.strftime("%A"),
    }


@app.get("/date/iso")
def get_server_date_iso():
    """Возвращает только дату в формате ISO (YYYY-MM-DD)."""
    now = datetime.now(timezone.utc)
    return {"date": now.date().isoformat()}


@app.get("/health")
def health():
    """Проверка состояния сервиса."""
    return {"status": "ok"}
