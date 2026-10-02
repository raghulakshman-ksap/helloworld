# helloworld

- `frontend/` - Next.js + shadcn/ui
- `backend/` - FastAPI + Pydantic
- `compose.yaml` - runs both

```bash
podman compose up -d --build   # web on :3000, api on :8000
podman compose down
```

See `frontend/README.md` and `backend/README.md` for local development.
