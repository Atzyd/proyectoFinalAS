# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copiar código
COPY app ./app

# Exponer puerto
EXPOSE 8000

# comando por defecto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
