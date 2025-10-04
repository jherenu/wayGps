FROM nginx:alpine

# Copiar configuración personalizada
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Crear directorios para archivos estáticos
RUN mkdir -p /app/staticfiles /app/mediafiles

# Exponer puerto
EXPOSE 80
