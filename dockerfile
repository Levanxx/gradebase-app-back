# Etapa base
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto (si tu app lo usa)
EXPOSE 8000

# Comando de arranque (ajusta según tu app)
CMD ["python", "app.py"]