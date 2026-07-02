import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import config
from .models import CalendarCreate, CalendarClone, EventCreate, EventUpdate
from . import data_service, calendar_gen

app = FastAPI(title="PhotoCalendar API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Calendarios ────────────────────────────────────────────────────────────────

@app.get("/api/calendars")
def list_calendars():
    return data_service.list_calendars()


@app.post("/api/calendars", status_code=201)
def create_calendar(body: CalendarCreate):
    if data_service.get_calendar(body.name):
        raise HTTPException(400, f"El calendario '{body.name}' ya existe.")
    return data_service.create_calendar(body.name, body.year)


@app.get("/api/calendars/{name}")
def get_calendar(name: str):
    cal = data_service.get_calendar(name)
    if not cal:
        raise HTTPException(404, "Calendario no encontrado.")
    return cal


@app.delete("/api/calendars/{name}")
def delete_calendar(name: str):
    if not data_service.delete_calendar(name):
        raise HTTPException(404, "Calendario no encontrado.")
    return {"ok": True}


@app.post("/api/calendars/{name}/clone", status_code=201)
def clone_calendar(name: str, body: CalendarClone):
    if data_service.get_calendar(body.new_name):
        raise HTTPException(400, f"El calendario '{body.new_name}' ya existe.")
    try:
        return data_service.clone_calendar(name, body.new_name, body.new_year)
    except ValueError as e:
        raise HTTPException(404, str(e))


# ── Eventos ────────────────────────────────────────────────────────────────────

@app.get("/api/calendars/{name}/events")
def get_events(name: str, mes: str | None = None):
    cal = data_service.get_calendar(name)
    if not cal:
        raise HTTPException(404, "Calendario no encontrado.")
    events = cal["events"]
    if mes:
        events = [e for e in events if e["mes"] == mes]
    return events


@app.post("/api/calendars/{name}/events", status_code=201)
def add_event(name: str, body: EventCreate):
    try:
        return data_service.add_event(name, body.dia, body.mes, body.titulo, body.opciones)
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.put("/api/calendars/{name}/events/{event_id}")
def update_event(name: str, event_id: str, body: EventUpdate):
    updates = body.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(400, "Sin cambios.")
    result = data_service.update_event(name, event_id, updates)
    if result is None:
        raise HTTPException(404, "Evento no encontrado.")
    return result


@app.delete("/api/calendars/{name}/events/{event_id}")
def delete_event(name: str, event_id: str):
    if not data_service.delete_event(name, event_id):
        raise HTTPException(404, "Evento no encontrado.")
    return {"ok": True}


# ── Importar CSV ───────────────────────────────────────────────────────────────

@app.post("/api/calendars/{name}/import-csv")
async def import_csv(name: str, file: UploadFile = File(...)):
    if not data_service.get_calendar(name):
        raise HTTPException(404, "Calendario no encontrado.")
    content = (await file.read()).decode("utf-8")
    return data_service.import_csv(name, content)


# ── Generar PDF ────────────────────────────────────────────────────────────────

@app.post("/api/calendars/{name}/generate")
def generate_pdf(name: str):
    cal = data_service.get_calendar(name)
    if not cal:
        raise HTTPException(404, "Calendario no encontrado.")
    try:
        days = calendar_gen.load_all_days(cal["events"], cal["year"])
        calendar_gen.create_calendar_tex(days, cal["year"])
        pdf_path = calendar_gen.compile_pdf(name)
        return {"ok": True, "pdf": f"/api/calendars/{name}/pdf"}
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/api/calendars/{name}/pdf")
def get_pdf(name: str):
    pdf_path = Path(config.OUTPUT_PATH) / f"{name}.pdf"
    if not pdf_path.exists():
        raise HTTPException(404, "PDF no generado aún. Usa el botón 'Generar PDF'.")
    return FileResponse(str(pdf_path), media_type="application/pdf")


# ── Migración desde CSVs de input/ ────────────────────────────────────────────

@app.post("/api/migrate/csv")
def migrate_from_csv(year: int | None = None):
    default_year = year or config.DEFAULT_YEAR
    return data_service.migrate_from_input_csvs(default_year)


# ── Servir frontend en producción ──────────────────────────────────────────────

_frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if _frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(_frontend_dist), html=True), name="static")
