from datetime import datetime, timezone, timedelta
import ephem
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

UTC_PLUS_5 = timezone(timedelta(hours=5))

app = FastAPI(title="Test Backend", description="Простой тестовый бэкенд с временем сервера. ПЛАНИРУЕТСЯ ТЕСТИРОВАНИЕ")


def _ephem_date_to_utc5(ephem_date) -> datetime:
    """Конвертирует ephem.Date в datetime UTC+5."""
    d = ephem.Date(ephem_date)
    try:
        dt_utc = d.datetime().replace(tzinfo=timezone.utc)
    except AttributeError:
        t = d.tuple()
        dt_utc = datetime(
            int(t[0]), int(t[1]), int(t[2]),
            int(t[3]), int(t[4]), int(t[5]),
            tzinfo=timezone.utc,
        )
    return dt_utc.astimezone(UTC_PLUS_5)


def _moon_phase_name(illumination: float) -> str:
    """Название фазы луны по проценту освещённости (0–100)."""
    if illumination < 2:
        return "Новолуние"
    if illumination < 23:
        return "Молодая луна (растущий серп)"
    if illumination < 48:
        return "Первая четверть (растущая)"
    if illumination < 52:
        return "Полнолуние"
    if illumination < 77:
        return "Последняя четверть (убывающая)"
    if illumination < 98:
        return "Убывающий серп"
    return "Новолуние"


@app.get("/")
def root():
    """Корневой эндпоинт."""
    return {"message": "Test Backend", "docs": "/docs", "moon": "/ui"}


def _render_ui_html(moon_phase: dict | None = None) -> str:
    """HTML интерфейса с кнопкой MOON вверху."""
    moon_block = ""
    if moon_phase:
        moon_block = f"""
        <section style="background: #16213e; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <h2 style="margin-top: 0;">Фаза луны (UTC+5)</h2>
            <p><strong>{moon_phase.get("phase_name", "")}</strong>, освещённость {moon_phase.get("illumination_percent", 0)}%</p>
            <p><a href="/moon/phase">JSON</a> · <a href="/moon/next-new">Ближайшее новолуние</a> · <a href="/moon/next-full">Ближайшее полнолуние</a></p>
        </section>
        """
    return f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Backend</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ font-family: system-ui, sans-serif; margin: 0; padding: 0; background: #1a1a2e; color: #eee; min-height: 100vh; }}
        .top-bar {{ background: #16213e; padding: 1rem 1.5rem; display: flex; align-items: center; gap: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.3); }}
        .btn-moon {{ background: linear-gradient(135deg, #0f3460 0%, #533483 100%); color: #fff; border: none; padding: 0.6rem 1.2rem; font-size: 1rem; font-weight: 600; border-radius: 8px; cursor: pointer; text-decoration: none; display: inline-flex; align-items: center; gap: 0.5rem; }}
        .btn-moon:hover {{ filter: brightness(1.15); }}
        .content {{ padding: 2rem; max-width: 800px; margin: 0 auto; }}
        .content a {{ color: #e94560; }}
    </style>
</head>
<body>
    <header class="top-bar">
        <a href="/moon" class="btn-moon">MOON</a>
        <a href="/ui" style="color: #aaa; text-decoration: none;">Test Backend</a>
    </header>
    <main class="content">
        <h1>Приложение</h1>
        {moon_block}
        <p><a href="/docs">Документация API</a> · <a href="/moon/phase">Фаза луны (API)</a></p>
    </main>
</body>
</html>
"""


@app.get("/ui", response_class=HTMLResponse)
def ui():
    """Интерфейс приложения с кнопкой MOON вверху."""
    return _render_ui_html()


@app.get("/moon", response_class=HTMLResponse)
def moon_page():
    """Страница с данными о луне (UTC+5); кнопка MOON ведёт сюда."""
    try:
        phase = get_moon_phase()
    except Exception:
        phase = None
    return _render_ui_html(phase)


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


@app.get("/moon/phase")
def get_moon_phase():
    """Фаза луны по текущему времени UTC+5."""
    now_utc5 = datetime.now(UTC_PLUS_5)
    now_utc = now_utc5.astimezone(timezone.utc)
    ephem_date = ephem.Date(now_utc)
    moon = ephem.Moon(ephem_date)
    illumination = moon.phase  # процент освещённости (0–100 в ephem)
    return {
        "time_utc5": now_utc5.isoformat(),
        "phase_name": _moon_phase_name(illumination),
        "illumination_percent": round(illumination, 2),
    }


@app.get("/moon/next-new")
def get_next_new_moon():
    """Ближайшие дата и время новолуния (UTC+5)."""
    now_utc = datetime.now(timezone.utc)
    ephem_date = ephem.Date(now_utc)
    next_new = ephem.next_new_moon(ephem_date)
    dt_utc5 = _ephem_date_to_utc5(next_new)
    return {
        "next_new_moon_utc5": dt_utc5.isoformat(),
        "date": dt_utc5.date().isoformat(),
        "time": dt_utc5.time().isoformat(),
    }


@app.get("/moon/next-full")
def get_next_full_moon():
    """Ближайшие дата и время полнолуния (UTC+5)."""
    now_utc = datetime.now(timezone.utc)
    ephem_date = ephem.Date(now_utc)
    next_full = ephem.next_full_moon(ephem_date)
    dt_utc5 = _ephem_date_to_utc5(next_full)
    return {
        "next_full_moon_utc5": dt_utc5.isoformat(),
        "date": dt_utc5.date().isoformat(),
        "time": dt_utc5.time().isoformat(),
    }


@app.get("/health")
def health():
    """Проверка состояния сервиса."""
    return {"status": "ok"}
