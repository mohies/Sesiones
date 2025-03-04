# Usar una imagen oficial de Python
FROM python:3.9

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivos de requerimientos e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente de la API
COPY . .

# Exponer el puerto en el que corre Django
EXPOSE 8000

# Comando para ejecutar el servidor
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Sesiones.wsgi:application"]
