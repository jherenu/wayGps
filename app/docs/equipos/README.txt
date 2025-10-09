╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                  MÓDULO DE EQUIPOS GPS - DOCUMENTACIÓN                    ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

================================================================================
DESCRIPCIÓN
================================================================================

Módulo completo de gestión de Equipos GPS que se instalan en los vehículos.

CARACTERÍSTICAS:
✓ CRUD completo de equipos
✓ Gestión de estados (Operativo, Mantenimiento, Stock, Baja)
✓ Vinculación con móviles
✓ Filtros por estado y asignación
✓ Búsqueda por IMEI, serie, marca, modelo
✓ Mismo diseño que módulo de móviles
✓ Responsive y con autenticación

================================================================================
TABLA EXISTENTE: equipos_gps
================================================================================

La tabla equipos_gps ya existía en la base de datos con esta estructura:

CAMPOS:
- id (BigAutoField, PK)
- imei (CharField 15, UNIQUE, OBLIGATORIO)
- numero_serie (CharField 50, NULL)
- modelo (CharField 50, NULL)
- marca (CharField 50, NULL)
- estado (CharField 20, NULL)
- empresa (ForeignKey a empresas, NULL)
- fecha_instalacion (DateTime, NULL)
- created_at (DateTime, auto)
- updated_at (DateTime, auto)

CAMPO OBLIGATORIO:
  * IMEI (identificador único del equipo)

================================================================================
ESTADOS DE EQUIPOS
================================================================================

1. OPERATIVO
   - Equipo instalado y funcionando
   - Badge verde

2. EN MANTENIMIENTO
   - Equipo en reparación o actualización
   - Badge amarillo

3. EN STOCK
   - Equipo disponible sin asignar
   - Badge gris
   - Estado por defecto

4. DADO DE BAJA
   - Equipo fuera de servicio
   - Badge rojo

================================================================================
ARCHIVOS CREADOS
================================================================================

BACKEND:
  gps/models.py
  └─ class Equipo          ✓ Modelo basado en tabla existente
                            ✓ managed=False (no modifica la tabla)

  gps/serializers.py
  └─ EquipoSerializer      ✓ Serializer para API
                            ✓ Validación de IMEI único

  gps/views.py
  └─ EquipoViewSet         ✓ ViewSet para API REST
  └─ equipos_frontend()    ✓ Vista para frontend

  gps/urls.py
  └─ /api/equipos/         ✓ Endpoint API agregado

  gps/admin.py
  └─ EquipoAdmin           ✓ Admin de Django

FRONTEND:
  templates/equipos/
  └─ index.html            ✓ Página principal de equipos

  static/css/
  └─ equipos.css           ✓ Estilos específicos

  static/js/
  └─ equipos.js            ✓ Lógica JavaScript

MENÚ:
  templates/moviles/index.html
  └─ Link a Equipos GPS    ✓ Agregado en sidebar

================================================================================
API ENDPOINTS
================================================================================

GET    /api/equipos/           - Listar todos los equipos
POST   /api/equipos/           - Crear nuevo equipo
GET    /api/equipos/{id}/      - Obtener un equipo
PUT    /api/equipos/{id}/      - Actualizar equipo
DELETE /api/equipos/{id}/      - Eliminar equipo

EJEMPLO DE RESPUESTA:
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "imei": "123456789012345",
      "numero_serie": "SN001",
      "marca": "Teltonika",
      "modelo": "FMB920",
      "estado": "operativo",
      "empresa": null,
      "fecha_instalacion": "2025-01-15T10:00:00Z",
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-01-15T10:00:00Z",
      "movil_info": {
        "id": 1,
        "patente": "ABC123",
        "alias": "Camión 1"
      }
    }
  ]
}
```

================================================================================
USO DEL SISTEMA
================================================================================

1. ACCEDER:
   http://127.0.0.1:8000/equipos/

2. VER LISTA:
   - Tabla con todos los equipos
   - IMEI, marca, modelo, estado
   - Móvil asignado
   - Última comunicación

3. CREAR EQUIPO:
   - Clic en "Nuevo Equipo"
   - Completar IMEI (obligatorio)
   - Marca, modelo, serie (opcionales)
   - Seleccionar estado
   - Guardar

4. EDITAR EQUIPO:
   - Clic en ícono de lápiz
   - Modificar datos
   - Guardar

5. ELIMINAR EQUIPO:
   - Clic en ícono de basura
   - Confirmar eliminación

6. FILTRAR:
   - Por estado (Operativo, Mantenimiento, Stock, Baja)
   - Por asignación (Asignado, Sin Asignar)
   - Búsqueda por IMEI, serie, marca

================================================================================
INTEGRACIÓN CON MÓVILES
================================================================================

FUTURO - Asignación de Equipos a Móviles:

Cuando implementes la asignación completa:

1. En el formulario de Equipo, agregar selector de Móvil
2. En el formulario de Móvil, mostrar equipos asignados
3. Un equipo puede tener fecha_instalacion y fecha_desinstalacion
4. Historial de asignaciones

ACTUALMENTE:
- Campo 'movil' existe en el modelo pero está comentado
- Se mostrará cuando lo actives
- Relación: Equipo -> Móvil (FK)

================================================================================
PRÓXIMOS PASOS
================================================================================

1. ☑ Reiniciar servidor: python manage.py runserver

2. ☑ Acceder: http://127.0.0.1:8000/moviles/

3. ☑ Verás "Equipos GPS" en el menú lateral

4. ☑ Clic en "Equipos GPS"

5. ☑ Cargarán los equipos de la tabla equipos_gps

6. ☑ Crear, editar, eliminar equipos

PARA FUTURO:
7. ☐ Implementar asignación de equipos a móviles
8. ☐ Historial de instalaciones
9. ☐ Dashboard específico de equipos
10. ☐ Separar en perfil EP cuando implementes multi-empresa

================================================================================
NOTAS IMPORTANTES
================================================================================

TABLA EXISTENTE:
  ✓ El modelo usa managed=False
  ✓ Django NO modificará la estructura de la tabla
  ✓ Solo lee y escribe datos
  ✓ La tabla sigue siendo administrada por ti

RELACIÓN CON EMPRESA:
  ✓ Campo 'empresa' existe
  ✓ Apunta a tabla 'empresas'
  ✓ Se usará cuando implementes EP y ET

CAMPO IMEI:
  ✓ Obligatorio (required)
  ✓ Único (no puede haber duplicados)
  ✓ Max 15 caracteres
  ✓ Identificador principal del equipo

================================================================================

✅ Módulo de Equipos GPS creado y listo para usar!

🔗 Acceso: http://127.0.0.1:8000/equipos/
📊 API: http://127.0.0.1:8000/api/equipos/
📝 IMEI es obligatorio (marcado con *)

¡Reinicia el servidor y prueba el módulo de Equipos!

================================================================================
