FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt backend/
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY . backend/

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
