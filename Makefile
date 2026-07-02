.PHONY: install build start dev-backend dev-frontend

# Setup completo (primera vez o tras cambiar deps)
install:
	uv sync
	cd frontend && npm install

# Compilar frontend → dist/ (necesario tras cambios en frontend)
build:
	cd frontend && npm run build

# Arrancar la app completa (frontend compilado + backend)
start: build
	uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Solo backend (si frontend ya está compilado)
dev-backend:
	uv run uvicorn backend.main:app --reload

# Solo frontend con hot-reload (para desarrollo del UI)
dev-frontend:
	cd frontend && npm run dev
