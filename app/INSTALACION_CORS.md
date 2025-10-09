# Solución al Error de CORS

## Problema
El navegador bloquea las peticiones desde el frontend al API debido a la política de CORS (Cross-Origin Resource Sharing).

## Solución

### Paso 1: Instalar django-cors-headers

Ejecuta el siguiente comando en tu terminal:

```bash
pip install django-cors-headers
```

O instala todas las dependencias actualizadas:

```bash
pip install -r requirements.txt
```

### Paso 2: Verificar la configuración

Ya he actualizado los siguientes archivos:

1. **`requirements.txt`** - Agregado `django-cors-headers==4.6.0`
2. **`wayproject/settings.py`** - Agregado:
   - `'corsheaders'` en `INSTALLED_APPS`
   - `'corsheaders.middleware.CorsMiddleware'` en `MIDDLEWARE`
   - Configuración de CORS al final del archivo

### Paso 3: Reiniciar el servidor Django

1. **Detén el servidor** si está corriendo (Ctrl+C en la terminal)
2. **Reinstala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Inicia el servidor nuevamente**:
   ```bash
   python manage.py runserver
   ```

### Paso 4: Probar el frontend

Abre el archivo `index.html` en tu navegador y verifica que ahora funcione correctamente.

## Configuración Actual de CORS

He configurado `CORS_ALLOW_ALL_ORIGINS = True` para facilitar el desarrollo. Esto permite peticiones desde cualquier origen.

### Para Producción

En producción, deberías cambiar esto en `settings.py`:

```python
# Comentar o eliminar esta línea:
# CORS_ALLOW_ALL_ORIGINS = True

# Y descomentar y configurar esta:
CORS_ALLOWED_ORIGINS = [
    "https://tu-dominio.com",
    "https://www.tu-dominio.com",
]
```

## Alternativa: Usar un servidor local

Si no quieres instalar paquetes adicionales, puedes servir el frontend desde un servidor web local:

### Opción 1: Python HTTP Server
```bash
# En el directorio donde está index.html
python -m http.server 8080
```
Luego abre: `http://localhost:8080`

### Opción 2: Live Server (VS Code)
Si usas VS Code, instala la extensión "Live Server" y haz clic derecho en `index.html` > "Open with Live Server"

### Opción 3: Node.js http-server
```bash
npm install -g http-server
http-server -p 8080
```

## Verificación

Después de configurar CORS, deberías ver en la consola del navegador:

✅ Sin errores de CORS
✅ Peticiones GET/POST/PUT/DELETE funcionando
✅ Datos cargándose correctamente en el frontend

## Comandos Resumidos

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Reiniciar servidor Django
python manage.py runserver

# 3. Abrir frontend en navegador
# Abrir index.html directamente o usar un servidor local
```

¡Listo! El error de CORS debería estar resuelto.
