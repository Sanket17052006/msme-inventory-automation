FROM python:3.12-slim

RUN groupadd -r app && useradd -r -g app app

WORKDIR /app
COPY dashboard/requirements.txt dashboard/
RUN pip install --no-cache-dir -r dashboard/requirements.txt
COPY . .

USER app

CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
