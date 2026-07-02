import { useState, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  api, CalendarData, CalendarEvent, MESES,
  displayTitle, formatOpciones, sortedEvents,
} from "./api";
import EventModal from "./EventModal";

// ── Tabla de eventos ───────────────────────────────────────────────────────────

function EventsTable({
  events,
  calendarName,
  calendarYear,
  search,
}: {
  events: CalendarEvent[];
  calendarName: string;
  calendarYear: number;
  search: string;
}) {
  const qc = useQueryClient();
  const [editing, setEditing] = useState<CalendarEvent | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const deleteMut = useMutation({
    mutationFn: (id: string) => api.deleteEvent(calendarName, id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["calendar", calendarName] });
      setDeletingId(null);
    },
  });

  const filtered = sortedEvents(events).filter((e) => {
    if (!search) return true;
    const q = search.toLowerCase();
    return (
      displayTitle(e.titulo).toLowerCase().includes(q) ||
      e.mes.includes(q) ||
      String(e.dia).includes(q)
    );
  });

  if (filtered.length === 0) {
    return (
      <div className="text-center py-12 text-gray-400">
        {search ? "No hay eventos que coincidan con la búsqueda." : "No hay eventos en este mes."}
      </div>
    );
  }

  return (
    <>
      <div className="overflow-x-auto rounded-xl border border-gray-200 shadow-sm">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-gray-50 border-b border-gray-200">
              <th className="text-left px-4 py-3 font-medium text-gray-600 w-14">Día</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600 w-32">Mes</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Título</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600 hidden sm:table-cell">Anotación</th>
              <th className="px-4 py-3 w-24"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {filtered.map((event) => (
              <tr key={event.id} className="hover:bg-gray-50 transition-colors">
                <td className="px-4 py-3 font-medium text-gray-900">{event.dia}</td>
                <td className="px-4 py-3 text-gray-600 capitalize">{event.mes}</td>
                <td className="px-4 py-3 text-gray-900">{displayTitle(event.titulo)}</td>
                <td className="px-4 py-3 text-gray-500 hidden sm:table-cell">
                  {formatOpciones(event.opciones, calendarYear)}
                </td>
                <td className="px-4 py-3">
                  <div className="flex gap-1 justify-end">
                    <button
                      onClick={() => setEditing(event)}
                      className="p-1.5 text-gray-400 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
                      title="Editar"
                    >
                      ✏️
                    </button>
                    {deletingId === event.id ? (
                      <div className="flex gap-1">
                        <button
                          onClick={() => deleteMut.mutate(event.id)}
                          className="px-2 py-1 text-xs text-white bg-red-600 hover:bg-red-700 rounded"
                        >
                          Sí
                        </button>
                        <button
                          onClick={() => setDeletingId(null)}
                          className="px-2 py-1 text-xs text-gray-600 bg-gray-100 rounded"
                        >
                          No
                        </button>
                      </div>
                    ) : (
                      <button
                        onClick={() => setDeletingId(event.id)}
                        className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                        title="Eliminar"
                      >
                        🗑️
                      </button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {editing && (
        <EventModal
          calendarName={calendarName}
          calendarYear={calendarYear}
          event={editing}
          onClose={() => setEditing(null)}
        />
      )}
    </>
  );
}

// ── Panel PDF ──────────────────────────────────────────────────────────────────

function PDFSection({ calendarName }: { calendarName: string }) {
  const [pdfTs, setPdfTs] = useState<number | null>(null);
  const [generating, setGenerating] = useState(false);
  const [genError, setGenError] = useState("");

  const handleGenerate = async () => {
    setGenerating(true);
    setGenError("");
    try {
      await api.generatePdf(calendarName);
      setPdfTs(Date.now());
    } catch (e) {
      setGenError((e as Error).message);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="mt-6 bg-white rounded-xl border border-gray-200 shadow-sm p-5">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-base font-semibold text-gray-900">Vista previa PDF</h2>
        <button
          onClick={handleGenerate}
          disabled={generating}
          className="px-4 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:bg-primary-300 rounded-lg transition-colors flex items-center gap-2"
        >
          {generating && (
            <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
          )}
          {generating ? "Generando PDF…" : pdfTs ? "Regenerar PDF" : "Generar PDF"}
        </button>
      </div>

      {generating && (
        <div className="flex items-center gap-3 p-4 bg-primary-50 rounded-lg text-sm text-primary-700 mb-4">
          <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          Compilando con pdflatex… esto puede tardar unos segundos.
        </div>
      )}

      {genError && (
        <details className="mb-4">
          <summary className="text-sm text-red-600 cursor-pointer">Error al generar el PDF (click para ver detalles)</summary>
          <pre className="mt-2 text-xs bg-red-50 text-red-800 p-3 rounded-lg overflow-auto max-h-40 whitespace-pre-wrap">
            {genError}
          </pre>
        </details>
      )}

      {pdfTs && !generating && (
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-gray-400">
              Generado a las {new Date(pdfTs).toLocaleTimeString("es-ES")}
            </span>
            <a
              href={api.pdfUrl(calendarName, pdfTs)}
              download={`${calendarName}.pdf`}
              className="text-xs text-primary-600 hover:underline"
            >
              ⬇ Descargar PDF
            </a>
          </div>
          <iframe
            src={api.pdfUrl(calendarName, pdfTs)}
            className="w-full rounded-lg border border-gray-200"
            style={{ height: "70vh" }}
            title="Vista previa del calendario"
          />
        </div>
      )}

      {!pdfTs && !generating && !genError && (
        <div className="text-center py-10 text-gray-400 text-sm border-2 border-dashed border-gray-200 rounded-lg">
          Pulsa «Generar PDF» para compilar el calendario con LaTeX
        </div>
      )}
    </div>
  );
}

// ── Clonar modal ───────────────────────────────────────────────────────────────

function CloneModal({ calendarName, calendarYear, onClose }: { calendarName: string; calendarYear: number; onClose: () => void }) {
  const navigate = useNavigate();
  const [newName, setNewName] = useState(`${calendarName}_copia`);
  const [newYear, setNewYear] = useState(calendarYear + 1);
  const [error, setError] = useState("");
  const [result, setResult] = useState<{ calendar: CalendarData; skipped: unknown[] } | null>(null);

  const cloneMut = useMutation({
    mutationFn: () => api.cloneCalendar(calendarName, newName.trim(), newYear),
    onSuccess: (data) => setResult(data),
    onError: (e: Error) => setError(e.message),
  });

  if (result) {
    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-xl shadow-2xl w-full max-w-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-3">Calendario clonado</h2>
          <p className="text-sm text-gray-600 mb-2">
            <strong>{result.calendar.events?.length ?? "?"}</strong> eventos copiados a <strong>{newName}</strong> ({newYear}).
          </p>
          {result.skipped.length > 0 && (
            <p className="text-sm text-amber-600">{result.skipped.length} eventos saltados (días inválidos para el año {newYear}).</p>
          )}
          <div className="flex gap-3 justify-end mt-5">
            <button onClick={onClose} className="px-4 py-2 text-sm text-gray-700 bg-gray-100 rounded-lg">
              Cerrar
            </button>
            <button
              onClick={() => { onClose(); navigate(`/calendar/${newName}`); }}
              className="px-4 py-2 text-sm text-white bg-primary-600 rounded-lg"
            >
              Ir al nuevo calendario
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-md p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Clonar calendario</h2>
        <p className="text-sm text-gray-500 mb-4">Copia todos los eventos a un nuevo calendario con distinto año u otro nombre.</p>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Nuevo nombre</label>
            <input
              type="text"
              value={newName}
              onChange={(e) => { setNewName(e.target.value); setError(""); }}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Año nuevo</label>
            <input
              type="number"
              value={newYear}
              onChange={(e) => setNewYear(Number(e.target.value))}
              min={2000}
              max={2100}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          {error && <p className="text-sm text-red-600">{error}</p>}
        </div>
        <div className="flex gap-3 justify-end mt-6">
          <button onClick={onClose} className="px-4 py-2 text-sm text-gray-700 bg-gray-100 rounded-lg">Cancelar</button>
          <button
            onClick={() => cloneMut.mutate()}
            disabled={!newName.trim() || cloneMut.isPending}
            className="px-4 py-2 text-sm text-white bg-primary-600 hover:bg-primary-700 disabled:bg-primary-300 rounded-lg"
          >
            {cloneMut.isPending ? "Clonando…" : "Clonar"}
          </button>
        </div>
      </div>
    </div>
  );
}

// ── Vista principal ────────────────────────────────────────────────────────────

export default function CalendarView() {
  const { name } = useParams<{ name: string }>();
  const navigate = useNavigate();
  const fileRef = useRef<HTMLInputElement>(null);
  const qc = useQueryClient();

  const [mesFiltro, setMesFiltro] = useState<string>("todos");
  const [search, setSearch] = useState("");
  const [showAdd, setShowAdd] = useState(false);
  const [showClone, setShowClone] = useState(false);
  const [importStatus, setImportStatus] = useState<string>("");

  const { data: cal, isLoading, error } = useQuery<CalendarData>({
    queryKey: ["calendar", name],
    queryFn: () => api.getCalendar(name!),
    enabled: !!name,
  });

  const handleImportCsv = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !name) return;
    setImportStatus("Importando…");
    try {
      const result = await api.importCsv(name, file);
      setImportStatus(`✅ ${result.added} eventos importados, ${result.skipped.length} saltados.`);
      qc.invalidateQueries({ queryKey: ["calendar", name] });
    } catch (err) {
      setImportStatus(`❌ ${(err as Error).message}`);
    }
    e.target.value = "";
  };

  const eventsForMes = cal
    ? mesFiltro === "todos"
      ? cal.events
      : cal.events.filter((e) => e.mes === mesFiltro)
    : [];

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center text-gray-400">
        Cargando…
      </div>
    );
  }

  if (error || !cal) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-500 mb-4">Calendario no encontrado.</p>
          <button onClick={() => navigate("/")} className="text-primary-600 hover:underline text-sm">
            ← Volver a calendarios
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3 min-w-0">
            <button
              onClick={() => navigate("/")}
              className="p-1.5 text-gray-400 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors shrink-0"
              title="Volver"
            >
              ←
            </button>
            <div className="min-w-0">
              <div className="flex items-center gap-2">
                <h1 className="font-semibold text-gray-900 truncate">{cal.name}</h1>
                <span className="px-2 py-0.5 bg-primary-100 text-primary-700 text-xs font-medium rounded-full shrink-0">
                  {cal.year}
                </span>
              </div>
              <p className="text-xs text-gray-400">{cal.events.length} eventos</p>
            </div>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <button
              onClick={() => setShowClone(true)}
              className="px-3 py-2 text-sm text-gray-600 hover:bg-gray-100 border border-gray-200 rounded-lg transition-colors hidden sm:block"
            >
              Clonar
            </button>
            <input
              ref={fileRef}
              type="file"
              accept=".csv"
              onChange={handleImportCsv}
              className="hidden"
            />
            <button
              onClick={() => fileRef.current?.click()}
              className="px-3 py-2 text-sm text-gray-600 hover:bg-gray-100 border border-gray-200 rounded-lg transition-colors hidden sm:block"
            >
              Importar CSV
            </button>
            <button
              onClick={() => setShowAdd(true)}
              className="px-3 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors"
            >
              + Evento
            </button>
          </div>
        </div>

        {importStatus && (
          <div className={`px-4 py-2 text-sm text-center ${importStatus.startsWith("✅") ? "bg-green-50 text-green-700" : importStatus.startsWith("❌") ? "bg-red-50 text-red-700" : "bg-blue-50 text-blue-700"}`}>
            {importStatus}{" "}
            <button onClick={() => setImportStatus("")} className="ml-2 opacity-60 hover:opacity-100">✕</button>
          </div>
        )}
      </header>

      <main className="max-w-6xl mx-auto px-4 py-6">
        {/* Filtros de mes */}
        <div className="flex gap-1 overflow-x-auto pb-2 mb-4 scrollbar-none">
          <button
            onClick={() => setMesFiltro("todos")}
            className={`px-3 py-1.5 text-sm font-medium rounded-full whitespace-nowrap transition-colors ${mesFiltro === "todos" ? "bg-primary-600 text-white" : "text-gray-600 hover:bg-gray-100"}`}
          >
            Todos ({cal.events.length})
          </button>
          {MESES.map((m) => {
            const count = cal.events.filter((e) => e.mes === m).length;
            if (count === 0) return null;
            return (
              <button
                key={m}
                onClick={() => setMesFiltro(m)}
                className={`px-3 py-1.5 text-sm font-medium rounded-full whitespace-nowrap transition-colors ${mesFiltro === m ? "bg-primary-600 text-white" : "text-gray-600 hover:bg-gray-100"}`}
              >
                {m.charAt(0).toUpperCase() + m.slice(1)} ({count})
              </button>
            );
          })}
        </div>

        {/* Búsqueda */}
        <div className="mb-4 flex gap-2">
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Buscar eventos…"
            className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
          {search && (
            <button
              onClick={() => setSearch("")}
              className="px-3 py-2 text-sm text-gray-500 hover:bg-gray-100 border border-gray-200 rounded-lg"
            >
              ✕
            </button>
          )}
        </div>

        {/* Tabla */}
        <EventsTable
          events={eventsForMes}
          calendarName={cal.name}
          calendarYear={cal.year}
          search={search}
        />

        {/* PDF */}
        <PDFSection calendarName={cal.name} />
      </main>

      {showAdd && (
        <EventModal
          calendarName={cal.name}
          calendarYear={cal.year}
          onClose={() => setShowAdd(false)}
        />
      )}
      {showClone && (
        <CloneModal
          calendarName={cal.name}
          calendarYear={cal.year}
          onClose={() => setShowClone(false)}
        />
      )}
    </div>
  );
}
