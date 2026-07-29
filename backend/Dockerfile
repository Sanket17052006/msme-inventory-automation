FROM python:3.12-slim

RUN groupadd -r app && useradd -r -g app app

WORKDIR /app
COPY backend/requirements.txt backend/
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY . .

USER app

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
