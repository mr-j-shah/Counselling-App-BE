# FastAPI Practice App

FastAPI project with structured architecture.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Run

```bash
python -m uvicorn app.main:app --reload
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /api/v1/health` - Health check
- `POST /api/v1/users/` - Create user

## Project Structure

```
app/
├── main.py              # App entry point
├── core/                # App-wide configs
├── api/                 # API layer
├── schemas/             # Pydantic models
├── services/            # Business logic
├── db/                  # DB related code
└── utils/               # Helpers
```

