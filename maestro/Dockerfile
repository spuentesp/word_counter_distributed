FROM python:3.12-slim

WORKDIR /app

# Dependencias necesarias
RUN apt-get update && apt-get install -y \
    libbz2-dev gcc g++ make curl libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar ice desde PyPI
RUN pip install --no-cache-dir zeroc-ice

# Copiar archivos del proyecto
COPY maestro/ ./
COPY shared/ ./shared/

# Puerto por defecto del worker
EXPOSE 10000

# Ejecutar directamente
CMD ["python", "main.py"]
