# helloworld-api

FastAPI + Pydantic backend.

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows (source .venv/bin/activate elsewhere)
pip install -e ".[dev]"
fastapi dev app/main.py       # http://localhost:8000/docs
pytest
```

Settings are read from environment variables prefixed `API_` or from `backend/.env`.
