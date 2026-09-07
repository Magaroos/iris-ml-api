FROM python:3.11-slim

WORKDIR /app

# Copy dependencies first
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy full project
COPY . .

# Expose port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]