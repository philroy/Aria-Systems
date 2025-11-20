FROM python:3.10-slim

WORKDIR /aria

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY frontend/ ./frontend/

WORKDIR /aria/backend
EXPOSE 8080

CMD ["python", "server.py"]
