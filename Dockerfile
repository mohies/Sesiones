# Usa Python 3.11
FROM python:3.11

# Configurar el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de dependencias primero
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 🚨 Instalar `rest_framework_simplejwt` manualmente en caso de que falle
RUN pip install --no-cache-dir djangorestframework-simplejwt

# Copiar el resto del código del proyecto
COPY . .

# Exponer el puerto de Django
EXPOSE 8000

# Comando por defecto para ejecutar Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
