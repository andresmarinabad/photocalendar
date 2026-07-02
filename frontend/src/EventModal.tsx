import { useState, useEffect } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api, CalendarEvent, EventCreate, MESES } from "./api";

type OpcionType = "none" | "birthyear" | "cumple" | "santo" | "memoria";

function opcionesFromRaw(opciones: string): [OpcionType, number] {
  if (!opciones) return ["none", 1980];
  const n = parseInt(opciones, 10);
  if (!isNaN(n)) return ["birthyear", n];
  if (opciones === "cumple") return ["cumple", 1980];
  if (opciones === "santo") return ["santo", 1980];
  if (opciones === "memoria") return ["memoria", 1980];
  return ["none", 1980];
}

function opcionesToRaw(type: OpcionType, year: number): string {
  if (type === "birthyear") return String(year);
  if (type === "cumple") return "cumple";
  if (type === "santo") return "santo";
  if (type === "memoria") return "memoria";
  return "";
}

function daysInMonth(mes: string, year: number): number {
  const idx = MESES.indexOf(mes as (typeof MESES)[number]);
  if (idx === -1) return 31;
  const date = new Date(year, idx + 1, 0);
  return date.getDate();
}

interface Props {
  calendarName: string;
  calendarYear: number;
  event?: CalendarEvent | null;
  onClose: () => void;
}

export default function EventModal({ calendarName, calendarYear, event, onClose }: Props) {
  const qc = useQueryClient();
  const isEditing = !!event;

  const [mes, setMes] = useState(event?.mes ?? "enero");
  const [dia, setDia] = useState(event?.dia ?? 1);
  const [titleRaw, setTitleRaw] = useState(
    event ? event.titulo.replace(/^\\Cross\s*/, "") : ""
  );
  const [deceased, setDeceased] = useState(
    event ? event.titulo.startsWith("\\Cross") : false
  );
  const [opcionType, setOpcionType] = useState<OpcionType>("none");
  const [birthYear, setBirthYear] = useState(1980);
  const [error, setError] = useState("");

  useEffect(() => {
    if (event) {
      const [t, y] = opcionesFromRaw(event.opciones);
      setOpcionType(t);
      setBirthYear(y);
    }
  }, [event]);

  const maxDia = daysInMonth(mes, calendarYear);
  useEffect(() => {
    if (dia > maxDia) setDia(maxDia);
  }, [mes, maxDia, dia]);

  const buildPayload = (): EventCreate => {
    const titulo = deceased ? `\\Cross ${titleRaw.trim()}` : titleRaw.trim();
    const opciones = opcionesToRaw(opcionType, birthYear);
    return { dia, mes, titulo, opciones };
  };

  const saveMut = useMutation({
    mutationFn: () => {
      const payload = buildPayload();
      if (isEditing) return api.updateEvent(calendarName, event!.id, payload);
      return api.addEvent(calendarName, payload);
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["calendar", calendarName] });
      onClose();
    },
    onError: (e: Error) => setError(e.message),
  });

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-5">
          {isEditing ? "Editar evento" : "Añadir evento"}
        </h2>

        <div className="space-y-4">
          {/* Mes + Día */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Mes</label>
              <select
                value={mes}
                onChange={(e) => { setMes(e.target.value); setError(""); }}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                {MESES.map((m) => (
                  <option key={m} value={m}>
                    {m.charAt(0).toUpperCase() + m.slice(1)}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Día <span className="text-gray-400">(1–{maxDia})</span>
              </label>
              <input
                type="number"
                value={dia}
                min={1}
                max={maxDia}
                onChange={(e) => { setDia(Math.min(maxDia, Math.max(1, Number(e.target.value)))); setError(""); }}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>

          {/* Título */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Título</label>
            <input
              type="text"
              value={titleRaw}
              onChange={(e) => { setTitleRaw(e.target.value); setError(""); }}
              placeholder="Cumpleaños Andrés"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          {/* Fallecido */}
          <label className="flex items-center gap-2 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={deceased}
              onChange={(e) => setDeceased(e.target.checked)}
              className="w-4 h-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
            />
            <span className="text-sm text-gray-700">Persona fallecida ✝ (añade cruz en el calendario)</span>
          </label>

          {/* Tipo de anotación */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Anotación</label>
            <select
              value={opcionType}
              onChange={(e) => setOpcionType(e.target.value as OpcionType)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="none">— Sin anotación</option>
              <option value="birthyear">Año (muestra diferencia con año del calendario)</option>
              <option value="cumple">Cumpleaños (sin año)</option>
              <option value="santo">Festividad / Santo</option>
              <option value="memoria">En memoria ✝ (añade cruz al final)</option>
            </select>
          </div>

          {/* Año (condicional) */}
          {opcionType === "birthyear" && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Año <span className="text-gray-400">(nacimiento, matrimonio…)</span>
              </label>
              <input
                type="number"
                value={birthYear}
                min={1900}
                max={2100}
                onChange={(e) => setBirthYear(Number(e.target.value))}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
              <p className="text-xs text-gray-400 mt-1">
                En el calendario {calendarYear} aparecerá como: «{titleRaw || "Nombre"} {calendarYear - birthYear}»
              </p>
            </div>
          )}

          {error && <p className="text-sm text-red-600 bg-red-50 px-3 py-2 rounded-lg">{error}</p>}
        </div>

        <div className="flex gap-3 justify-end mt-6">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            Cancelar
          </button>
          <button
            onClick={() => saveMut.mutate()}
            disabled={!titleRaw.trim() || saveMut.isPending}
            className="px-4 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:bg-primary-300 rounded-lg transition-colors"
          >
            {saveMut.isPending ? "Guardando…" : isEditing ? "Guardar cambios" : "Añadir"}
          </button>
        </div>
      </div>
    </div>
  );
}
