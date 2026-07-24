# Page Pulse

## Project Overview

Page Pulse is a lightweight webpage audit tool. Submit a URL through the React interface or the API to retrieve core content, accessibility, and performance signals from its HTML.

## Features

The API returns the following metrics for each audit:

- Final URL after redirects
- HTTP status code
- Response time in milliseconds
- Page title
- Meta description
- H1 count
- Images missing alternative text
- Visible word count

## Tech Stack

### Backend

- Python 3.12
- FastAPI
- httpx
- BeautifulSoup4
- Pydantic
- pytest

### Frontend

- React
- Vite
- TypeScript
- TailwindCSS
- Axios

## Installation

### Backend setup

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

### Frontend setup

```powershell
cd frontend
npm install
```

## Running Locally

### Backend

```powershell
cd backend
.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

The API is available at `http://localhost:8000`.

### Frontend

```powershell
cd frontend
npm run dev
```

Open the Vite URL shown in the terminal, normally `http://localhost:5173`.

### Tests

```powershell
cd backend
.venv\Scripts\Activate.ps1
python -m pytest -v
```

## API Contract

### `POST /api/audit`

#### Request JSON

```json
{
  "url": "https://example.com"
}
```

#### Example request

```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/audit" -ContentType "application/json" -Body '{"url":"https://example.com"}'
```

#### Example success response

```json
{
  "url": "https://example.com/",
  "status_code": 200,
  "response_time_ms": 245,
  "title": "Example Domain",
  "meta_description": "An example page.",
  "h1_count": 1,
  "images_missing_alt": 0,
  "word_count": 18
}
```

#### Example error responses

**400 — Invalid URL**

```json
{
  "detail": "A valid HTTP or HTTPS URL is required."
}
```

**408 — Timeout**

```json
{
  "detail": "The webpage did not respond within 10 seconds."
}
```

**415 — Non-HTML response**

```json
{
  "detail": "The provided URL does not point to an HTML page."
}
```

**500 — Internal server error**

```json
{
  "detail": "The webpage could not be analysed."
}
```

## Folder Structure

```text
backend/
  app/
    routers/      API endpoint definitions
    schemas/      Request and response models
    services/     Webpage fetch and parsing logic
  tests/          Isolated backend tests
frontend/
  src/
    components/   Reusable interface elements
    pages/        Page-level UI composition
    services/     API client code
```

## Design Decisions

### Asynchronous HTTP requests

Page Pulse uses `httpx.AsyncClient` so the server can await a slow webpage fetch without blocking other incoming requests. This keeps the API responsive when multiple audits are in progress and fits FastAPI's asynchronous request handling model.

### Separate routers and services

The router only handles the HTTP request and response contract, while the service owns fetching, HTML parsing, and metric calculation. This keeps the API layer easy to read and makes the parsing logic straightforward to test without real network traffic.

### Meaningful HTTP status codes

The API reports invalid input, timeouts, unsupported content, and unexpected processing failures with clear status codes and messages. Clients can reliably distinguish an input issue from a temporary fetch problem or a response type the service does not support.
