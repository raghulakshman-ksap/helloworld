# helloworld

A small full-stack app: a Next.js + shadcn/ui frontend that calls a FastAPI + Pydantic backend. Both run together with `podman compose`.

## Repository structure

```
helloworld/
├── compose.yaml              # Runs api + web containers
├── frontend/                 # Next.js (App Router, TypeScript, Tailwind, shadcn/ui)
│   ├── Dockerfile            # Multi-stage build, standalone output, non-root runtime
│   ├── .env.example          # NEXT_PUBLIC_API_URL
│   ├── next.config.ts        # output: "standalone" (needed by the Dockerfile)
│   ├── components.json       # shadcn/ui configuration
│   ├── public/               # Static assets
│   └── src/
│       ├── app/
│       │   ├── layout.tsx    # Root layout
│       │   ├── page.tsx      # Home page (card + HelloButton), a server component
│       │   └── globals.css   # Tailwind and shadcn theme tokens
│       ├── components/
│       │   ├── hello-button.tsx   # Client component that calls GET /hello
│       │   └── ui/                # shadcn/ui components (button, card)
│       └── lib/utils.ts      # cn() class-name helper
└── backend/                  # FastAPI + Pydantic
    ├── Dockerfile            # python:3.13-slim, non-root runtime
    ├── pyproject.toml        # Dependencies, pytest and ruff config
    ├── app/
    │   ├── main.py           # FastAPI app, CORS middleware, routes
    │   ├── schemas.py        # Pydantic request/response models
    │   └── config.py         # pydantic-settings (API_* environment variables)
    └── tests/
        ├── test_hello.py     # /hello and CORS
        └── test_items.py     # /health and /items CRUD + validation
```

## How the frontend and backend interact

```
Browser ──(1) GET /  ─────────────▶ web  (Next.js, :3000)   serves HTML + JS
Browser ──(2) GET /hello (fetch) ─▶ api  (FastAPI, :8000)   returns {"message": "Hello, World!"}
```

- The page is served by the `web` container. Clicking **Say hello** runs `fetch()` **in the browser** (`hello-button.tsx`) against `${NEXT_PUBLIC_API_URL}/hello`. The Next.js server does not proxy the call.
- Because the browser calls the API directly, the API address must be reachable from the user's machine (`http://localhost:8000`, the published port), not a container-internal hostname.
- `NEXT_PUBLIC_API_URL` is inlined into the JS bundle at **build time**. Changing it requires rebuilding the frontend image (it is a build arg in `compose.yaml`).
- The page origin (`:3000`) differs from the API origin (`:8000`), so the browser enforces CORS. The backend allows the origins in `API_CORS_ORIGINS` (default `["http://localhost:3000"]`).
- The API response shape is defined by the Pydantic `Hello` model in `backend/app/schemas.py`. The frontend mirrors it with a hand-written TypeScript type (`{ message: string }`), so keep the two in sync.

### Backend endpoints

| Method | Path          | Description                                       |
| ------ | ------------- | ------------------------------------------------- |
| GET    | `/hello`      | Returns `{"message": "Hello, World!"}`            |
| GET    | `/health`     | Liveness check, used by the compose health check  |
| GET    | `/items`      | Lists items                                       |
| POST   | `/items`      | Creates an item (validated by `ItemCreate`)       |
| GET    | `/items/{id}` | Returns one item, 404 if missing                  |

Items are stored in memory and reset on restart. Interactive docs are at `http://localhost:8000/docs`.

## Run with Podman Compose

```bash
podman compose up -d --build   # web on http://localhost:3000, api on http://localhost:8000
podman compose down
```

`web` waits for the `api` health check before starting.

## Local development

Run each side in its own terminal.

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows (source .venv/bin/activate elsewhere)
pip install -e ".[dev]"
fastapi dev app/main.py         # http://localhost:8000/docs
pytest
ruff check .
```

```bash
cd frontend
npm install
npm run dev                     # http://localhost:3000
npm run lint
npm run build
```

Optionally copy `frontend/.env.example` to `frontend/.env.local` to point the frontend at a different API URL.

## Configuration

| Variable               | Used by  | Default                   | Notes                                   |
| ---------------------- | -------- | ------------------------- | --------------------------------------- |
| `NEXT_PUBLIC_API_URL`  | frontend | `http://localhost:8000`   | Build-time, visible in the browser      |
| `API_CORS_ORIGINS`     | backend  | `["http://localhost:3000"]` | JSON list of allowed browser origins  |
| `API_APP_NAME`         | backend  | `helloworld-api`          | FastAPI title                           |

Backend settings can also be placed in `backend/.env`.

See `frontend/README.md` and `backend/README.md` for more detail on each side.
