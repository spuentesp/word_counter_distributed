FROM python:3.12-slim

WORKDIR /app

# 1. Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libbz2-dev gcc g++ make curl libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Instalar ZeroC ICE para Python
RUN pip install --no-cache-dir zeroc-ice

# 3. Instalar Flask y dependencias de la app
COPY maestro/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar archivos del proyecto
COPY maestro/ ./maestro/
COPY shared/ ./maestro/shared/

WORKDIR /app/maestro

# 5. Exponer el puerto 80 para la web
EXPOSE 80

# 6. Ejecutar la app Flask
CMD ["python", "main.py"]

