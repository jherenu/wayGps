╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                SISTEMA DE AUTENTICACIÓN WAYGPS - DOCUMENTACIÓN            ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

================================================================================
DESCRIPCIÓN DEL SISTEMA
================================================================================

Sistema completo de autenticación, autorización, roles y perfiles para WayGPS.

CARACTERÍSTICAS:
✓ Sistema de login/logout
✓ Gestión de roles y permisos
✓ Perfiles de acceso por módulo
✓ Permisos por entidad (CRUD)
✓ Bloqueo por intentos fallidos
✓ Sesiones de usuario con auditoría
✓ Preparado para 2FA (futuro)
✓ Multi-empresa (futuro)

================================================================================
ESTRUCTURA DE TABLAS CREADAS
================================================================================

1. USUARIOS (users + perfil_usuario)
   - Extiende el modelo User de Django
   - Campos adicionales: teléfono, documento, empresa
   - Relación con Rol
   - Campos de seguridad: intentos_fallidos, bloqueado_hasta
   - Preparado para 2FA

2. ROLES (roles)
   - Define el tipo de usuario (Superadmin, Supervisor, Operador, etc.)
   - Tiene permisos generales (crear, editar, eliminar, ver_todo)
   - Se relaciona con Perfiles (qué módulos puede ver)
   - Se relaciona con PermisoEntidad (qué puede hacer en cada entidad)
   - Tipo de empresa: EP, ET, INTERNO

3. PERFILES (perfiles)
   - Define los módulos del sistema (Dashboard, Móviles, Equipos, etc.)
   - Cada perfil representa una sección del menú
   - Se asignan a Roles
   - Orden de visualización

4. PERMISOS_ENTIDAD (permisos_entidad)
   - Define qué puede hacer un Rol en cada entidad
   - Acciones: ver, crear, editar, eliminar, exportar
   - Granularidad fina de permisos
   - Relación Rol -> Entidad

5. SESIONES_USUARIO (sesiones_usuario)
   - Auditoría de sesiones
   - Token, IP, User Agent
   - Fecha inicio, último acceso, fin
   - Control de sesiones activas

================================================================================
ROLES CREADOS POR DEFECTO
================================================================================

1. SUPER ADMINISTRADOR (superadmin)
   - Acceso TOTAL a todo el sistema
   - Todos los perfiles disponibles
   - Todos los permisos en todas las entidades
   - Tipo: INTERNO

2. SUPERVISOR DE FLOTA (supervisor)
   - Perfiles: Dashboard, Móviles, Viajes, Reportes
   - Puede crear y editar (no eliminar)
   - Puede ver todo
   - Tipo: INTERNO

3. OPERADOR (operador)
   - Perfiles: Dashboard, Móviles, Reportes
   - Solo lectura (no puede crear/editar/eliminar)
   - Puede ver todo
   - Tipo: INTERNO

================================================================================
PERFILES CREADOS POR DEFECTO
================================================================================

1. Dashboard (dashboard)          - Icono: bi-speedometer2
2. Móviles (moviles)              - Icono: bi-truck
3. Equipos GPS (equipos)          - Icono: bi-cpu
4. Personas/Conductores (personas) - Icono: bi-people
5. Zonas/Geocercas (zonas)        - Icono: bi-geo-alt
6. Viajes (viajes)                - Icono: bi-signpost
7. Reportes (reportes)            - Icono: bi-graph-up
8. Usuarios (usuarios)            - Icono: bi-person-gear
9. Empresas (empresas)            - Icono: bi-building
10. Configuración (configuracion) - Icono: bi-gear

================================================================================
SUPERUSUARIO POR DEFECTO
================================================================================

CREDENCIALES:
  Username: admin
  Email:    admin@waygps.com
  Password: admin123

⚠️ IMPORTANTE: 
   - Cambiar la contraseña inmediatamente en producción
   - Crear usuarios específicos para cada persona
   - No compartir credenciales de superusuario

================================================================================
COMANDOS ÚTILES
================================================================================

INICIALIZAR SISTEMA:
  python manage.py init_auth_data

CREAR SUPERUSUARIO ADICIONAL:
  python manage.py createsuperuser

VER USUARIOS:
  python manage.py shell
  >>> from django.contrib.auth.models import User
  >>> User.objects.all()

VER ROLES:
  >>> from authentication.models import Rol
  >>> Rol.objects.all()

VER PERFILES:
  >>> from authentication.models import Perfil
  >>> Perfil.objects.all()

================================================================================
API ENDPOINTS
================================================================================

AUTENTICACIÓN:
  POST   /api/auth/login/             - Login
  POST   /api/auth/logout/            - Logout
  GET    /api/auth/me/                - Perfil actual
  GET    /api/auth/permisos/          - Permisos del usuario
  POST   /api/auth/cambiar-password/  - Cambiar contraseña

ADMINISTRACIÓN:
  GET    /api/auth/usuarios/          - Lista de usuarios
  POST   /api/auth/usuarios/          - Crear usuario
  GET    /api/auth/usuarios/{id}/     - Detalle de usuario
  PUT    /api/auth/usuarios/{id}/     - Actualizar usuario
  DELETE /api/auth/usuarios/{id}/     - Eliminar usuario
  
  GET    /api/auth/roles/             - Lista de roles
  GET    /api/auth/perfiles/          - Lista de perfiles
  GET    /api/auth/permisos-entidad/  - Lista de permisos

================================================================================
FLUJO DE LOGIN
================================================================================

1. Usuario ingresa credenciales en /login/

2. Frontend envía POST a /api/auth/login/
   Body: { "username": "admin", "password": "admin123" }

3. Backend valida credenciales:
   - Verifica usuario existe
   - Verifica password correcto
   - Verifica no está bloqueado
   - Verifica está activo

4. Si es correcto:
   - Resetea intentos fallidos
   - Actualiza último login e IP
   - Crea/obtiene token de autenticación
   - Crea sesión en sesiones_usuario
   - Retorna: token, usuario, perfiles, permisos

5. Frontend guarda en localStorage/sessionStorage:
   - authToken
   - userData
   - userPermisos
   - userPerfiles

6. Redirige a /moviles/ (dashboard)

7. En cada página protegida:
   - Verifica token existe
   - Valida token con /api/auth/me/
   - Si es válido, muestra contenido
   - Si no, redirige a /login/

================================================================================
SISTEMA DE PERMISOS
================================================================================

NIVELES DE PERMISO:

1. SUPERUSUARIO (is_superuser = True)
   - Acceso total sin restricciones
   - Bypass de todos los checks de permisos

2. ROL CON es_superusuario = True
   - Acceso total (similar a superusuario)
   - Para administradores de empresa

3. PERFILES
   - Define QUÉ MÓDULOS puede ver el usuario
   - Ejemplo: Dashboard, Móviles, Reportes

4. PERMISOS DE ENTIDAD
   - Define QUÉ PUEDE HACER en cada entidad
   - Acciones: ver, crear, editar, eliminar, exportar
   - Granularidad fina

EJEMPLO DE VERIFICACIÓN:

```python
# En views.py
from authentication.models import PerfilUsuario

def mi_vista(request):
    perfil = request.user.perfil_usuario
    
    # Verificar si puede ver móviles
    if perfil.puede_acceder_entidad('moviles', 'ver'):
        # Mostrar móviles
        pass
    
    # Verificar si puede crear móviles
    if perfil.puede_acceder_entidad('moviles', 'crear'):
        # Permitir crear
        pass
```

EN FRONTEND (JavaScript):

```javascript
// Verificar si puede ver móviles
if (auth.tienePermiso('moviles', 'ver')) {
    // Mostrar sección de móviles
}

// Verificar si puede crear
if (auth.tienePermiso('moviles', 'crear')) {
    // Mostrar botón "Nuevo Móvil"
}

// Verificar si tiene acceso al perfil Dashboard
if (auth.tieneAccesoPerfil('dashboard')) {
    // Mostrar Dashboard en menú
}
```

================================================================================
SEGURIDAD IMPLEMENTADA
================================================================================

1. BLOQUEO POR INTENTOS FALLIDOS:
   - Después de 5 intentos fallidos
   - Bloquea por 30 minutos
   - Campo: bloqueado_hasta

2. CONTRASEÑAS:
   - Hasheadas con PBKDF2 (Django default)
   - Mínimo 8 caracteres
   - No se almacenan en texto plano
   - Input type="password" (oculto)

3. TOKENS DE AUTENTICACIÓN:
   - Token único por usuario
   - Se envía en header: Authorization: Token <token>
   - Se invalida en logout
   - Se regenera al cambiar contraseña

4. AUDITORÍA:
   - Registro de cada sesión
   - IP y User Agent
   - Fecha de inicio y fin
   - Últimas actividades

5. VALIDACIONES:
   - Usuario debe estar activo (is_active=True)
   - No debe estar bloqueado
   - Token debe ser válido
   - Permisos verificados en cada acción

================================================================================
PREPARADO PARA 2FA (FUTURO)
================================================================================

Campos ya incluidos en PerfilUsuario:
  - two_factor_enabled (Boolean)
  - two_factor_secret (String)

Para implementar en el futuro:
1. Usar biblioteca como pyotp o django-otp
2. Generar QR code para autenticadores (Google Authenticator, Authy)
3. Verificar código en login
4. Códigos de respaldo

================================================================================
PREPARADO PARA MULTI-EMPRESA (FUTURO)
================================================================================

Campos ya incluidos:
  - empresa (String)
  - empresa_id (Integer)
  - tipo_empresa en Rol (EP, ET, INTERNO)

Cuando implementes empresas:
1. Crear modelo Empresa
2. Cambiar empresa_id a ForeignKey
3. Filtrar datos por empresa del usuario
4. Jerarquía: EP (proveedora) -> ET (cliente)

================================================================================
CÓMO USAR EL SISTEMA
================================================================================

1. ACCEDER AL SISTEMA:
   http://127.0.0.1:8000/
   o
   http://127.0.0.1:8000/login/

2. INICIAR SESIÓN:
   Username: admin
   Password: admin123

3. SERÁ REDIRIGIDO A:
   http://127.0.0.1:8000/moviles/

4. VERÁ:
   - Dashboard con datos
   - Nombre de usuario en sidebar
   - Botón "Cerrar Sesión"
   - Todas las opciones (es superusuario)

5. CERRAR SESIÓN:
   - Clic en botón "Cerrar Sesión"
   - Será redirigido a /login/

================================================================================
CREAR NUEVOS USUARIOS
================================================================================

OPCIÓN 1 - Admin de Django:

1. http://127.0.0.1:8000/admin/
2. Login con superusuario
3. Users -> Add User
4. Completar datos
5. En "Perfil de Usuario": asignar Rol

OPCIÓN 2 - API:

```bash
POST /api/auth/usuarios/
Headers: Authorization: Token <token>
Body: {
    "username": "usuario1",
    "email": "usuario1@example.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "password": "password123",
    "password_confirm": "password123",
    "rol_id": 2,  # ID del rol
    "is_active": true
}
```

OPCIÓN 3 - Shell de Django:

```python
python manage.py shell

from django.contrib.auth.models import User
from authentication.models import Rol

# Crear usuario
user = User.objects.create_user(
    username='operador1',
    email='operador1@waygps.com',
    password='password123',
    first_name='Juan',
    last_name='García'
)

# Asignar rol
rol_operador = Rol.objects.get(codigo='operador')
user.perfil_usuario.rol = rol_operador
user.perfil_usuario.save()
```

================================================================================
ESTRUCTURA DE ARCHIVOS
================================================================================

authentication/
├── models.py                   - Modelos (Usuario, Rol, Perfil, Permisos)
├── serializers.py              - Serializers para API
├── views.py                    - Vistas de login/logout/permisos
├── urls.py                     - URLs de la API
├── admin.py                    - Configuración del admin
├── management/
│   └── commands/
│       └── init_auth_data.py  - Comando para inicializar datos
└── migrations/
    └── 0001_initial.py        - Migración inicial

templates/authentication/
└── login.html                  - Página de login

static/js/
└── auth.js                     - Módulo JavaScript de autenticación

docs/authentication/
└── README.txt                  - Esta documentación

================================================================================
CONFIGURACIÓN EN SETTINGS.PY
================================================================================

INSTALLED_APPS:
  - 'rest_framework.authtoken'  ← Agregado
  - 'authentication'            ← Agregado

REST_FRAMEWORK:
  - TokenAuthentication
  - SessionAuthentication
  - IsAuthenticatedOrReadOnly

URLS:
  - /api/auth/                  ← Nueva ruta API
  - /login/                     ← Nueva página frontend

================================================================================
TESTING
================================================================================

1. VERIFICAR TABLAS CREADAS:
   ```
   python manage.py dbshell
   \dt
   ```
   
   Deberías ver:
   - perfiles
   - roles
   - permisos_entidad
   - perfil_usuario
   - sesiones_usuario

2. VERIFICAR DATOS INICIALES:
   ```
   python manage.py shell
   
   from authentication.models import Perfil, Rol
   print(Perfil.objects.count())  # 10
   print(Rol.objects.count())     # 3
   ```

3. PROBAR LOGIN:
   - Abrir: http://127.0.0.1:8000/login/
   - Ingresar: admin / admin123
   - Verificar redirección a /moviles/

4. PROBAR API:
   ```bash
   # Login
   curl -X POST http://127.0.0.1:8000/api/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'
   
   # Obtendrás un token
   
   # Usar token
   curl http://127.0.0.1:8000/api/auth/me/ \
     -H "Authorization: Token <tu_token>"
   ```

================================================================================
PERSONALIZACIÓN
================================================================================

AGREGAR NUEVO ROL:

1. Admin de Django: http://127.0.0.1:8000/admin/
2. Roles -> Add Rol
3. Completar datos
4. Asignar perfiles
5. Crear permisos de entidad

O via código:

```python
from authentication.models import Rol, Perfil, PermisoEntidad

# Crear rol
rol = Rol.objects.create(
    nombre='Cliente',
    codigo='cliente',
    tipo_empresa='ET',
    es_superusuario=False,
    puede_crear=False,
    puede_editar=False,
    puede_eliminar=False,
    puede_ver_todo=False
)

# Asignar perfiles
perfiles = Perfil.objects.filter(codigo__in=['dashboard', 'moviles'])
rol.perfiles.set(perfiles)

# Crear permisos
PermisoEntidad.objects.create(
    rol=rol,
    entidad='moviles',
    puede_ver=True,
    puede_crear=False,
    puede_editar=False,
    puede_eliminar=False,
    puede_exportar=False
)
```

AGREGAR NUEVO PERFIL:

```python
from authentication.models import Perfil

Perfil.objects.create(
    nombre='Mantenimiento',
    codigo='mantenimiento',
    descripcion='Gestión de mantenimiento de vehículos',
    icono='bi-tools',
    orden=11,
    activo=True
)
```

================================================================================
ROADMAP FUTURO
================================================================================

FASE 2 - MULTI-EMPRESA:
  □ Modelo Empresa (EP y ET)
  □ Jerarquía EP -> ET
  □ Filtrado de datos por empresa
  □ Pertenencia de móviles/equipos a empresas

FASE 3 - 2FA:
  □ Implementar pyotp o django-otp
  □ Generar QR codes
  □ Verificar códigos 2FA
  □ Códigos de respaldo

FASE 4 - RECUPERACIÓN DE CONTRASEÑA:
  □ Forgot password
  □ Envío de email con token
  □ Reset password

FASE 5 - PERMISOS GRANULARES:
  □ Permisos a nivel de campo
  □ Permisos por registro específico
  □ Filtros dinámicos por permisos

================================================================================

Sistema de autenticación creado y funcionando!

Para probar:
1. python manage.py runserver
2. http://127.0.0.1:8000/
3. Login con: admin / admin123

================================================================================
