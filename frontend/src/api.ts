export const MESES = [
  "enero", "febrero", "marzo", "abril", "mayo", "junio",
  "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
] as const;

export type MesName = (typeof MESES)[number];

export interface CalendarSummary {
  name: string;
  year: number;
  event_count: number;
}

export interface CalendarData {
  name: string;
  year: number;
  events: CalendarEvent[];
}

export interface CalendarEvent {
  id: string;
  dia: number;
  mes: string;
  titulo: string;
  opciones: string;
}

export interface EventCreate {
  dia: number;
  mes: string;
  titulo: string;
  opciones: string;
}

export interface ImportResult {
  added: number;
  skipped: Array<{ row: Record<string, string>; error: string }>;
}

// ── helpers ────────────────────────────────────────────────────────────────────

export function displayTitle(titulo: string): string {
  return titulo.replace(/\\Cross\s*/g, "✝ ").trim();
}

export function formatOpciones(opciones: string, calYear: number): string {
  if (!opciones) return "—";
  const n = parseInt(opciones, 10);
  if (!isNaN(n)) {
    const diff = calYear - n;
    if (diff > 0) return `${n} (${diff} años)`;
    if (diff === 0) return `${n} (este año)`;
    return `${n} (hace ${-diff} años)`;
  }
  if (opciones === "cumple") return "Cumpleaños";
  if (opciones === "santo") return "Festividad";
  if (opciones === "memoria") return "En memoria ✝";
  return opciones;
}

export function sortedEvents(events: CalendarEvent[]): CalendarEvent[] {
  return [...events].sort((a, b) => {
    const ma = MESES.indexOf(a.mes as MesName);
    const mb = MESES.indexOf(b.mes as MesName);
    if (ma !== mb) return ma - mb;
    return a.dia - b.dia;
  });
}

// ── fetch wrapper ──────────────────────────────────────────────────────────────

async function req<T>(method: string, path: string, body?: unknown): Promise<T> {
  const res = await fetch(`/api${path}`, {
    method,
    headers: body ? { "Content-Type": "application/json" } : {},
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail ?? res.statusText);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

// ── API calls ──────────────────────────────────────────────────────────────────

export const api = {
  listCalendars: () => req<CalendarSummary[]>("GET", "/calendars"),

  createCalendar: (name: string, year: number) =>
    req<CalendarData>("POST", "/calendars", { name, year }),

  getCalendar: (name: string) => req<CalendarData>("GET", `/calendars/${name}`),

  deleteCalendar: (name: string) => req<{ ok: boolean }>("DELETE", `/calendars/${name}`),

  cloneCalendar: (name: string, new_name: string, new_year: number) =>
    req<{ calendar: CalendarData; skipped: unknown[] }>(
      "POST", `/calendars/${name}/clone`, { new_name, new_year }
    ),

  addEvent: (calName: string, event: EventCreate) =>
    req<CalendarEvent>("POST", `/calendars/${calName}/events`, event),

  updateEvent: (calName: string, id: string, updates: Partial<EventCreate>) =>
    req<CalendarEvent>("PUT", `/calendars/${calName}/events/${id}`, updates),

  deleteEvent: (calName: string, id: string) =>
    req<{ ok: boolean }>("DELETE", `/calendars/${calName}/events/${id}`),

  generatePdf: (calName: string) =>
    req<{ ok: boolean; pdf: string }>("POST", `/calendars/${calName}/generate`),

  pdfUrl: (calName: string, ts: number) =>
    `/api/calendars/${calName}/pdf?t=${ts}`,

  importCsv: (calName: string, file: File) => {
    const form = new FormData();
    form.append("file", file);
    return fetch(`/api/calendars/${calName}/import-csv`, {
      method: "POST",
      body: form,
    }).then(async (res) => {
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }));
        throw new Error(err.detail ?? res.statusText);
      }
      return res.json() as Promise<ImportResult>;
    });
  },

  migrateFromCsv: (year: number) =>
    req<unknown[]>("POST", `/migrate/csv?year=${year}`),
};
