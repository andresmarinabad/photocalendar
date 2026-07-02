import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api, CalendarSummary } from "./api";

function CreateCalendarModal({ onClose }: { onClose: () => void }) {
  const qc = useQueryClient();
  const [name, setName] = useState("");
  const [year, setYear] = useState(new Date().getFullYear() + 1);
  const [error, setError] = useState("");

  const createMut = useMutation({
    mutationFn: () => api.createCalendar(name.trim(), year),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["calendars"] });
      onClose();
    },
    onError: (e: Error) => setError(e.message),
  });

  const nameValid = /^[a-zA-Z0-9_-]+$/.test(name.trim());

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-md p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Nuevo calendario</h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nombre <span className="text-gray-400 font-normal">(letras, números, guiones)</span>
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => { setName(e.target.value); setError(""); }}
              placeholder="familia_marin_2027"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Año</label>
            <input
              type="number"
              value={year}
              onChange={(e) => setYear(Number(e.target.value))}
              min={2000}
              max={2100}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          {error && <p className="text-sm text-red-600">{error}</p>}
        </div>

        <div className="flex gap-3 justify-end mt-6">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            Cancelar
          </button>
          <button
            onClick={() => createMut.mutate()}
            disabled={!name.trim() || !nameValid || createMut.isPending}
            className="px-4 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:bg-primary-300 rounded-lg transition-colors"
          >
            {createMut.isPending ? "Creando…" : "Crear"}
          </button>
        </div>
      </div>
    </div>
  );
}

function MigrateModal({ onClose }: { onClose: () => void }) {
  const qc = useQueryClient();
  const [year, setYear] = useState(new Date().getFullYear() + 1);
  const [result, setResult] = useState<unknown[] | null>(null);

  const migMut = useMutation({
    mutationFn: () => api.migrateFromCsv(year),
    onSuccess: (data) => {
      setResult(data);
      qc.invalidateQueries({ queryKey: ["calendars"] });
    },
  });

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-md p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Migrar desde CSVs</h2>
        <p className="text-sm text-gray-500 mb-4">
          Importa los archivos CSV de la carpeta <code className="bg-gray-100 px-1 rounded">input/</code> como nuevos calendarios.
        </p>

        {!result ? (
          <>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Año del calendario</label>
              <input
                type="number"
                value={year}
                onChange={(e) => setYear(Number(e.target.value))}
                min={2000}
                max={2100}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
            <div className="flex gap-3 justify-end mt-6">
              <button onClick={onClose} className="px-4 py-2 text-sm text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg">
                Cancelar
              </button>
              <button
                onClick={() => migMut.mutate()}
                disabled={migMut.isPending}
                className="px-4 py-2 text-sm text-white bg-primary-600 hover:bg-primary-700 disabled:bg-primary-300 rounded-lg"
              >
                {migMut.isPending ? "Importando…" : "Importar"}
              </button>
            </div>
          </>
        ) : (
          <>
            <div className="space-y-2 max-h-60 overflow-y-auto text-sm">
              {(result as Array<{ name: string; status: string; added?: number; skipped?: unknown[] }>).map((r) => (
                <div key={r.name} className={`p-2 rounded ${r.status === "ok" ? "bg-green-50 text-green-800" : "bg-yellow-50 text-yellow-800"}`}>
                  <strong>{r.name}</strong>:{" "}
                  {r.status === "ok" ? `${r.added} eventos añadidos, ${r.skipped?.length ?? 0} saltados` : r.status}
                </div>
              ))}
            </div>
            <div className="flex justify-end mt-4">
              <button onClick={onClose} className="px-4 py-2 text-sm text-white bg-primary-600 rounded-lg">
                Cerrar
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

function CalendarCard({ cal }: { cal: CalendarSummary }) {
  const navigate = useNavigate();
  const qc = useQueryClient();
  const [confirmDelete, setConfirmDelete] = useState(false);

  const deleteMut = useMutation({
    mutationFn: () => api.deleteCalendar(cal.name),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["calendars"] }),
  });

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="font-semibold text-gray-900 text-lg leading-tight">{cal.name}</h3>
          <span className="inline-block mt-1 px-2 py-0.5 bg-primary-100 text-primary-700 text-xs font-medium rounded-full">
            {cal.year}
          </span>
        </div>
        <span className="text-2xl text-gray-300">📅</span>
      </div>

      <p className="text-sm text-gray-500 mb-4">{cal.event_count} eventos</p>

      <div className="flex gap-2">
        <button
          onClick={() => navigate(`/calendar/${cal.name}`)}
          className="flex-1 px-3 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors"
        >
          Abrir
        </button>
        {confirmDelete ? (
          <div className="flex gap-1">
            <button
              onClick={() => deleteMut.mutate()}
              className="px-3 py-2 text-sm text-white bg-red-600 hover:bg-red-700 rounded-lg"
            >
              Confirmar
            </button>
            <button
              onClick={() => setConfirmDelete(false)}
              className="px-3 py-2 text-sm text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-lg"
            >
              No
            </button>
          </div>
        ) : (
          <button
            onClick={() => setConfirmDelete(true)}
            className="px-3 py-2 text-sm text-red-600 hover:bg-red-50 border border-red-200 rounded-lg transition-colors"
          >
            Borrar
          </button>
        )}
      </div>
    </div>
  );
}

export default function CalendarList() {
  const [showCreate, setShowCreate] = useState(false);
  const [showMigrate, setShowMigrate] = useState(false);

  const { data: calendars, isLoading, error } = useQuery({
    queryKey: ["calendars"],
    queryFn: api.listCalendars,
  });

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl">📷</span>
            <h1 className="text-xl font-bold text-gray-900">PhotoCalendar</h1>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setShowMigrate(true)}
              className="px-3 py-2 text-sm text-gray-600 hover:bg-gray-100 border border-gray-200 rounded-lg transition-colors"
            >
              Importar CSV
            </button>
            <button
              onClick={() => setShowCreate(true)}
              className="px-3 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors"
            >
              + Nuevo calendario
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-8">
        {isLoading && (
          <div className="text-center py-16 text-gray-400">Cargando…</div>
        )}
        {error && (
          <div className="bg-red-50 text-red-700 p-4 rounded-lg text-sm">
            Error al cargar calendarios: {(error as Error).message}
          </div>
        )}
        {calendars && calendars.length === 0 && (
          <div className="text-center py-16">
            <p className="text-gray-400 text-lg mb-4">No hay calendarios aún</p>
            <p className="text-gray-400 text-sm mb-6">
              Crea uno nuevo o importa tus CSVs existentes de <code className="bg-gray-100 px-1 rounded">input/</code>
            </p>
            <div className="flex gap-3 justify-center">
              <button
                onClick={() => setShowMigrate(true)}
                className="px-4 py-2 text-sm text-gray-700 bg-white border border-gray-300 hover:bg-gray-50 rounded-lg"
              >
                Importar desde CSV
              </button>
              <button
                onClick={() => setShowCreate(true)}
                className="px-4 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-lg"
              >
                + Crear calendario
              </button>
            </div>
          </div>
        )}
        {calendars && calendars.length > 0 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {calendars.map((cal) => (
              <CalendarCard key={cal.name} cal={cal} />
            ))}
          </div>
        )}
      </main>

      {showCreate && <CreateCalendarModal onClose={() => setShowCreate(false)} />}
      {showMigrate && <MigrateModal onClose={() => setShowMigrate(false)} />}
    </div>
  );
}
