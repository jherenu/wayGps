# WayGPS Frontend

Frontend personalizado para el sistema de seguimiento GPS de móviles que se conecta a la API REST en `http://127.0.0.1:8000/api/moviles/`.

## Características

### 🚗 Dashboard
- **Vista general** con estadísticas en tiempo real
- **Contadores** de móviles totales, en línea, con encendido
- **Velocidad promedio** de la flota
- **Mapa en tiempo real** con ubicaciones de móviles activos
- **Lista de móviles recientes** con sus últimas actualizaciones

### 📱 Gestión de Móviles
- **Tabla completa** con información detallada de cada móvil
- **Filtros avanzados** por estado, encendido, tipo de vehículo
- **Búsqueda en tiempo real** por patente, alias o código
- **Acciones CRUD** completas (crear, leer, actualizar, eliminar)
- **Estados visuales** (en línea/desconectado, encendido/apagado)

### 🗺️ Mapa Interactivo
- **Mapa principal** con todos los móviles
- **Marcadores personalizados** con colores según estado
- **Popups informativos** con datos detallados del móvil
- **Vista automática** que se ajusta a todos los marcadores
- **Integración con OpenStreetMap**

### 📊 Funcionalidades Adicionales
- **Actualización automática** cada 30 segundos
- **Diseño responsivo** para móviles y tablets
- **Interfaz moderna** con Bootstrap 5
- **Notificaciones** de éxito y error
- **Indicadores de carga** durante las operaciones

## Instalación y Uso

### Requisitos Previos
1. Tu API Django debe estar ejecutándose en `http://127.0.0.1:8000`
2. El endpoint `/api/moviles/` debe estar disponible
3. Un navegador web moderno

### Pasos de Instalación

1. **Descarga los archivos**:
   - `index.html` - Página principal
   - `app.js` - Lógica JavaScript
   - `README.md` - Este archivo

2. **Abre el archivo**:
   - Simplemente abre `index.html` en tu navegador web
   - O sirve los archivos desde un servidor web local

3. **Verifica la conexión**:
   - Asegúrate de que tu API Django esté corriendo
   - El frontend intentará conectarse automáticamente

### Configuración de CORS (IMPORTANTE)

⚠️ **Si obtienes errores de CORS**, sigue estos pasos:

#### Solución Rápida

1. **Instala django-cors-headers**:
   ```bash
   pip install django-cors-headers
   ```
   O ejecuta el archivo incluido:
   ```bash
   instalar_cors.bat    # En Windows
   ```

2. **La configuración ya está lista** en `settings.py`:
   - ✅ `corsheaders` agregado a `INSTALLED_APPS`
   - ✅ Middleware de CORS configurado
   - ✅ Permisos de CORS establecidos

3. **Reinicia tu servidor Django**:
   ```bash
   # Detén el servidor (Ctrl+C)
   python manage.py runserver
   ```

4. **¡Listo!** Recarga tu frontend y debería funcionar.

#### Configuración Manual

Si prefieres hacerlo manualmente, revisa el archivo `INSTALACION_CORS.md` incluido para instrucciones detalladas.

## Uso del Sistema

### Dashboard
- **Vista principal** al cargar la aplicación
- Muestra **estadísticas generales** de la flota
- **Mapa en tiempo real** con móviles activos
- **Lista de móviles recientes** ordenados por última actualización

### Gestión de Móviles
1. **Ver lista completa**: Navega a la sección "Móviles"
2. **Filtrar datos**: Usa los filtros en la parte superior
3. **Buscar específico**: Escribe en el campo de búsqueda
4. **Agregar móvil**: Clic en "Nuevo Móvil"
5. **Editar móvil**: Clic en el ícono de lápiz
6. **Ver detalles**: Clic en el ícono de ojo
7. **Eliminar móvil**: Clic en el ícono de basura

### Mapa
1. **Ver ubicaciones**: Navega a la sección "Mapa"
2. **Marcadores verdes**: Móviles en línea
3. **Marcadores rojos**: Móviles desconectados
4. **Información detallada**: Clic en cualquier marcador

## Estructura de Datos

El frontend espera que la API devuelva objetos con la siguiente estructura:

```json
{
  "id": 1,
  "codigo": "M001",
  "alias": "Camión 1",
  "patente": "ABC123",
  "vin": "1HGBH41JXMN109186",
  "marca": "Ford",
  "modelo": "F-150",
  "anio": 2023,
  "color": "Blanco",
  "tipo_vehiculo": "camion",
  "gps_id": "GPS001",
  "ultimo_lat": -34.6037,
  "ultimo_lon": -58.3816,
  "ultimo_rumbo": 45,
  "ultima_velocidad_kmh": 65.5,
  "ultima_altitud_m": 25.0,
  "ult_satelites": 8,
  "ultimo_hdop": 1.2,
  "fecha_gps": "2024-01-15T10:30:00Z",
  "fecha_recepcion": "2024-01-15T10:30:05Z",
  "ignicion": true,
  "bateria_pct": 85.5,
  "odometro_km": 12500.0,
  "km_calculado": 12500.0,
  "dir_formateada": "Av. Corrientes 1234, CABA",
  "activo": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T10:30:05Z"
}
```

## Personalización

### Cambiar URL de la API
En `app.js`, modifica la variable:
```javascript
const API_BASE_URL = 'http://127.0.0.1:8000/api';
```

### Personalizar Colores
En `index.html`, modifica las clases CSS:
```css
.status-online { color: #28a745; }
.status-offline { color: #dc3545; }
```

### Cambiar Frecuencia de Actualización
En `app.js`, modifica el intervalo:
```javascript
setInterval(() => {
    // ... código de actualización
}, 30000); // 30 segundos
```

## Solución de Problemas

### Error de CORS
- Agrega la configuración CORS mencionada arriba
- O usa un servidor web local para servir los archivos

### API no responde
- Verifica que Django esté ejecutándose
- Comprueba la URL en `app.js`
- Revisa la consola del navegador para errores

### Mapa no se carga
- Verifica conexión a internet
- Comprueba que Leaflet se cargue correctamente

### Datos no se actualizan
- Verifica que la API devuelva datos válidos
- Revisa la consola para errores de JavaScript

## Tecnologías Utilizadas

- **HTML5** - Estructura
- **CSS3** - Estilos y diseño responsivo
- **Bootstrap 5** - Framework CSS
- **JavaScript ES6+** - Lógica de la aplicación
- **Leaflet** - Mapas interactivos
- **Fetch API** - Comunicación con la API REST

## Soporte

Para soporte o reportar problemas:
1. Verifica que todos los archivos estén presentes
2. Comprueba la consola del navegador para errores
3. Asegúrate de que la API Django esté funcionando correctamente
4. Verifica la configuración de CORS si es necesario

---

**Desarrollado para WayGPS** 🚗📍
