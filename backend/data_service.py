import json
import uuid
import calendar as _cal
import csv
import io
from pathlib import Path

from .config import config

MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]


def _calendar_path(name: str) -> Path:
    return Path(config.CALENDARS_PATH) / f"{name}.json"


def _load(name: str) -> dict | None:
    path = _calendar_path(name)
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _save(data: dict) -> None:
    path = _calendar_path(data["name"])
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def validate_day(dia: int, mes: str, year: int) -> None:
    if mes not in MESES:
        raise ValueError(f"Mes '{mes}' no válido.")
    mes_num = MESES.index(mes) + 1
    _, max_day = _cal.monthrange(year, mes_num)
    if dia < 1 or dia > max_day:
        raise ValueError(f"Día {dia} inválido para {mes} en {year} (1–{max_day}).")


# ── Calendar CRUD ──────────────────────────────────────────────────────────────

def list_calendars() -> list[dict]:
    result = []
    for path in sorted(Path(config.CALENDARS_PATH).glob("*.json")):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        result.append({
            "name": data["name"],
            "year": data["year"],
            "event_count": len(data["events"]),
        })
    return result


def get_calendar(name: str) -> dict | None:
    return _load(name)


def create_calendar(name: str, year: int) -> dict:
    data = {"name": name, "year": year, "events": []}
    _save(data)
    return data


def delete_calendar(name: str) -> bool:
    path = _calendar_path(name)
    if path.exists():
        path.unlink()
        return True
    return False


def clone_calendar(source_name: str, new_name: str, new_year: int) -> dict:
    source = _load(source_name)
    if source is None:
        raise ValueError(f"Calendario '{source_name}' no encontrado.")

    new_events = []
    skipped = []
    for event in source["events"]:
        try:
            validate_day(event["dia"], event["mes"], new_year)
            new_events.append({**event, "id": str(uuid.uuid4())})
        except ValueError as e:
            skipped.append({"event": event, "error": str(e)})

    data = {"name": new_name, "year": new_year, "events": new_events}
    _save(data)
    return {"calendar": data, "skipped": skipped}


# ── Event CRUD ─────────────────────────────────────────────────────────────────

def add_event(cal_name: str, dia: int, mes: str, titulo: str, opciones: str) -> dict:
    data = _load(cal_name)
    if data is None:
        raise ValueError(f"Calendario '{cal_name}' no encontrado.")
    validate_day(dia, mes, data["year"])
    event = {"id": str(uuid.uuid4()), "dia": dia, "mes": mes, "titulo": titulo, "opciones": opciones}
    data["events"].append(event)
    _save(data)
    return event


def update_event(cal_name: str, event_id: str, updates: dict) -> dict | None:
    data = _load(cal_name)
    if data is None:
        return None
    for event in data["events"]:
        if event["id"] == event_id:
            event.update(updates)
            validate_day(event["dia"], event["mes"], data["year"])
            _save(data)
            return event
    return None


def delete_event(cal_name: str, event_id: str) -> bool:
    data = _load(cal_name)
    if data is None:
        return False
    original = len(data["events"])
    data["events"] = [e for e in data["events"] if e["id"] != event_id]
    if len(data["events"]) < original:
        _save(data)
        return True
    return False


# ── CSV import ─────────────────────────────────────────────────────────────────

def import_csv(cal_name: str, csv_text: str) -> dict:
    data = _load(cal_name)
    if data is None:
        raise ValueError(f"Calendario '{cal_name}' no encontrado.")

    year = data["year"]
    reader = csv.DictReader(io.StringIO(csv_text))
    added, skipped = 0, []

    for row in reader:
        try:
            dia = int(row["dia"])
            mes = row["mes"].strip().lower()
            titulo = row["titulo"].strip()
            opciones = row.get("opciones", "").strip()
            validate_day(dia, mes, year)
            data["events"].append({
                "id": str(uuid.uuid4()),
                "dia": dia, "mes": mes, "titulo": titulo, "opciones": opciones,
            })
            added += 1
        except (ValueError, KeyError) as e:
            skipped.append({"row": dict(row), "error": str(e)})

    _save(data)
    return {"added": added, "skipped": skipped}


# ── Bulk migration from input/ CSVs ───────────────────────────────────────────

def migrate_from_input_csvs(default_year: int) -> list[dict]:
    import glob
    results = []
    for csv_file in sorted(glob.glob(str(Path(config.CSV_FOLDER) / "*.csv"))):
        name = Path(csv_file).stem
        if _load(name) is not None:
            results.append({"name": name, "status": "skipped", "reason": "ya existe"})
            continue
        create_calendar(name, default_year)
        with open(csv_file, encoding="utf-8") as f:
            result = import_csv(name, f.read())
        results.append({"name": name, "status": "ok", **result})
    return results
