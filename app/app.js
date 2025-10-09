// Configuración de la API (desde config.js)
const API_BASE_URL = WAYGPS_CONFIG.API_BASE_URL;
const MOVILES_API_URL = getApiUrl();

// Variables globales
let movilesData = [];
let mapaPrincipal = null;
let mapaDashboard = null;
let markers = [];
let currentSection = 'dashboard';

// Inicialización cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    console.log('WayGPS Frontend iniciado');
    initializeApp();
});

// Función principal de inicialización
async function initializeApp() {
    try {
        debugLog('Iniciando aplicación WayGPS');
        await loadMoviles();
        initializeMaps();
        setupEventListeners();
        updateDashboard();
        debugLog('Aplicación inicializada correctamente');
    } catch (error) {
        console.error('Error al inicializar la aplicación:', error);
        showAlert('Error al cargar los datos', 'danger');
    }
}

// Cargar datos de móviles desde la API
async function loadMoviles() {
    try {
        showLoading(true);
        const response = await fetch(MOVILES_API_URL);
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        movilesData = await response.json();
        debugLog(`Cargados ${movilesData.length} móviles`);
        
        // Actualizar estadísticas del dashboard
        updateDashboardStats();
        
        // Actualizar tabla si estamos en la sección de móviles
        if (currentSection === 'moviles') {
            updateMovilesTable();
        }
        
        // Actualizar mapas si están inicializados
        if (mapaPrincipal) {
            updateMapaPrincipal();
        }
        if (mapaDashboard) {
            updateMapaDashboard();
        }
        
    } catch (error) {
        console.error('Error al cargar móviles:', error);
        showAlert('Error al cargar los datos de móviles', 'danger');
    } finally {
        showLoading(false);
    }
}

// Mostrar/ocultar indicador de carga
function showLoading(show) {
    const loadingElements = document.querySelectorAll('.loading');
    loadingElements.forEach(el => {
        el.style.display = show ? 'block' : 'none';
    });
}

// Actualizar estadísticas del dashboard
function updateDashboardStats() {
    const totalMoviles = movilesData.length;
    const movilesOnline = movilesData.filter(m => isOnline(m)).length;
    const movilesConIgnicion = movilesData.filter(m => m.ignicion === true).length;
    
    // Calcular velocidad promedio de móviles en movimiento
    const velocidades = movilesData
        .filter(m => m.ultima_velocidad_kmh && m.ultima_velocidad_kmh > 0)
        .map(m => parseFloat(m.ultima_velocidad_kmh));
    
    const velocidadPromedio = velocidades.length > 0 
        ? (velocidades.reduce((a, b) => a + b, 0) / velocidades.length).toFixed(1)
        : 0;

    document.getElementById('total-moviles').textContent = totalMoviles;
    document.getElementById('moviles-online').textContent = movilesOnline;
    document.getElementById('moviles-ignicion').textContent = movilesConIgnicion;
    document.getElementById('velocidad-promedio').textContent = `${velocidadPromedio} km/h`;
}

// Verificar si un móvil está en línea
function isOnline(movil) {
    if (!movil.fecha_recepcion) return false;
    
    const ultimaRecepcion = new Date(movil.fecha_recepcion);
    const ahora = new Date();
    const diferenciaMinutos = (ahora - ultimaRecepcion) / (1000 * 60);
    
    return diferenciaMinutos <= WAYGPS_CONFIG.STATUS.ONLINE_THRESHOLD_MINUTES;
}

// Mostrar secciones del menú
function showSection(section) {
    // Ocultar todas las secciones
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(sec => sec.style.display = 'none');
    
    // Mostrar la sección seleccionada
    document.getElementById(`${section}-section`).style.display = 'block';
    
    // Actualizar menú activo
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Actualizar título
    const titles = {
        'dashboard': 'Dashboard',
        'moviles': 'Móviles',
        'mapa': 'Mapa',
        'reportes': 'Reportes'
    };
    document.getElementById('page-title').textContent = titles[section];
    
    currentSection = section;
    
    // Cargar datos específicos de la sección
    switch(section) {
        case 'moviles':
            updateMovilesTable();
            break;
        case 'mapa':
            if (!mapaPrincipal) {
                initializeMapaPrincipal();
            }
            updateMapaPrincipal();
            break;
    }
}

// Actualizar tabla de móviles
function updateMovilesTable() {
    const tbody = document.getElementById('tbody-moviles');
    tbody.innerHTML = '';
    
    movilesData.forEach(movil => {
        const row = createMovilRow(movil);
        tbody.appendChild(row);
    });
}

// Crear fila de tabla para un móvil
function createMovilRow(movil) {
    const tr = document.createElement('tr');
    
    // Estado (online/offline)
    const online = isOnline(movil);
    const estadoIcon = online ? 
        '<i class="bi bi-wifi status-online"></i>' : 
        '<i class="bi bi-wifi-off status-offline"></i>';
    
    // Patente/Alias
    const identificacion = movil.alias || movil.patente || movil.codigo || 'Sin identificar';
    
    // Última posición
    const posicion = (movil.ultimo_lat && movil.ultimo_lon) ? 
        `${movil.ultimo_lat.toFixed(6)}, ${movil.ultimo_lon.toFixed(6)}` : 
        'Sin datos';
    
    // Velocidad
    const velocidad = movil.ultima_velocidad_kmh ? 
        `${movil.ultima_velocidad_kmh} km/h` : 
        'Sin datos';
    
    // Estado de encendido
    const encendido = movil.ignicion === true ? 
        '<span class="badge status-ignition-on">Encendido</span>' : 
        '<span class="badge status-ignition-off">Apagado</span>';
    
    // Batería
    const bateria = movil.bateria_pct ? 
        `${movil.bateria_pct}%` : 
        'Sin datos';
    
    // Última actualización
    const ultimaActualizacion = movil.fecha_recepcion ? 
        new Date(movil.fecha_recepcion).toLocaleString('es-ES') : 
        'Sin datos';
    
    tr.innerHTML = `
        <td>${estadoIcon}</td>
        <td><strong>${identificacion}</strong></td>
        <td>${movil.gps_id || 'Sin ID'}</td>
        <td><small>${posicion}</small></td>
        <td>${velocidad}</td>
        <td>${encendido}</td>
        <td>${bateria}</td>
        <td><small>${ultimaActualizacion}</small></td>
        <td>
            <button class="btn btn-sm btn-outline-primary" onclick="verDetalleMovil(${movil.id})" title="Ver detalles">
                <i class="bi bi-eye"></i>
            </button>
            <button class="btn btn-sm btn-outline-warning" onclick="editarMovil(${movil.id})" title="Editar">
                <i class="bi bi-pencil"></i>
            </button>
            <button class="btn btn-sm btn-outline-danger" onclick="eliminarMovil(${movil.id})" title="Eliminar">
                <i class="bi bi-trash"></i>
            </button>
        </td>
    `;
    
    return tr;
}

// Inicializar mapas
function initializeMaps() {
    // Mapa del dashboard
    if (document.getElementById('mapa-dashboard')) {
        const mapConfig = WAYGPS_CONFIG.MAP;
        mapaDashboard = L.map('mapa-dashboard').setView([mapConfig.DEFAULT_LAT, mapConfig.DEFAULT_LON], mapConfig.DEFAULT_ZOOM);
        L.tileLayer(mapConfig.TILE_PROVIDER, {
            attribution: mapConfig.ATTRIBUTION
        }).addTo(mapaDashboard);
    }
}

// Inicializar mapa principal
function initializeMapaPrincipal() {
    if (document.getElementById('mapa-principal')) {
        const mapConfig = WAYGPS_CONFIG.MAP;
        mapaPrincipal = L.map('mapa-principal').setView([mapConfig.DEFAULT_LAT, mapConfig.DEFAULT_LON], mapConfig.DEFAULT_ZOOM);
        L.tileLayer(mapConfig.TILE_PROVIDER, {
            attribution: mapConfig.ATTRIBUTION
        }).addTo(mapaPrincipal);
    }
}

// Actualizar mapa principal
function updateMapaPrincipal() {
    if (!mapaPrincipal) return;
    
    // Limpiar marcadores existentes
    markers.forEach(marker => mapaPrincipal.removeLayer(marker));
    markers = [];
    
    // Agregar marcadores para cada móvil
    movilesData.forEach(movil => {
        if (movil.ultimo_lat && movil.ultimo_lon) {
            const online = isOnline(movil);
            const iconColor = online ? WAYGPS_CONFIG.STATUS.ONLINE_COLOR : WAYGPS_CONFIG.STATUS.OFFLINE_COLOR;
            
            // Crear ícono personalizado
            const icon = L.divIcon({
                className: 'custom-marker',
                html: `<div style="background-color: ${iconColor}; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>`,
                iconSize: [20, 20],
                iconAnchor: [10, 10]
            });
            
            const marker = L.marker([movil.ultimo_lat, movil.ultimo_lon], { icon })
                .addTo(mapaPrincipal)
                .bindPopup(createMovilPopup(movil));
            
            markers.push(marker);
        }
    });
    
    // Ajustar vista para mostrar todos los marcadores
    if (markers.length > 0) {
        const group = new L.featureGroup(markers);
        mapaPrincipal.fitBounds(group.getBounds().pad(0.1));
    }
}

// Actualizar mapa del dashboard
function updateMapaDashboard() {
    if (!mapaDashboard) return;
    
    // Limpiar marcadores existentes
    const existingMarkers = document.querySelectorAll('#mapa-dashboard .leaflet-marker-icon');
    existingMarkers.forEach(marker => marker.remove());
    
    // Agregar marcadores para móviles en línea
    const movilesOnline = movilesData.filter(m => isOnline(m));
    movilesOnline.forEach(movil => {
        if (movil.ultimo_lat && movil.ultimo_lon) {
            const marker = L.marker([movil.ultimo_lat, movil.ultimo_lon], {
                icon: L.divIcon({
                    className: 'custom-marker',
                    html: '<div style="background-color: green; width: 15px; height: 15px; border-radius: 50%; border: 2px solid white;"></div>',
                    iconSize: [15, 15],
                    iconAnchor: [7, 7]
                })
            }).addTo(mapaDashboard);
        }
    });
}

// Crear popup para marcador de móvil
function createMovilPopup(movil) {
    const online = isOnline(movil);
    const estado = online ? 'En línea' : 'Desconectado';
    const encendido = movil.ignicion ? 'Encendido' : 'Apagado';
    
    return `
        <div style="min-width: 200px;">
            <h6><strong>${movil.alias || movil.patente || 'Sin identificar'}</strong></h6>
            <p><strong>Estado:</strong> ${estado}<br>
            <strong>GPS ID:</strong> ${movil.gps_id || 'Sin ID'}<br>
            <strong>Velocidad:</strong> ${movil.ultima_velocidad_kmh || 0} km/h<br>
            <strong>Encendido:</strong> ${encendido}<br>
            <strong>Batería:</strong> ${movil.bateria_pct || 'N/A'}%</p>
            <small><strong>Última actualización:</strong><br>${movil.fecha_recepcion ? new Date(movil.fecha_recepcion).toLocaleString('es-ES') : 'Sin datos'}</small>
        </div>
    `;
}

// Configurar event listeners
function setupEventListeners() {
    // Filtros de búsqueda
    document.getElementById('filtro-busqueda').addEventListener('input', aplicarFiltros);
    document.getElementById('filtro-estado').addEventListener('change', aplicarFiltros);
    document.getElementById('filtro-encendido').addEventListener('change', aplicarFiltros);
    document.getElementById('filtro-tipo').addEventListener('change', aplicarFiltros);
}

// Aplicar filtros a la tabla
function aplicarFiltros() {
    const busqueda = document.getElementById('filtro-busqueda').value.toLowerCase();
    const estado = document.getElementById('filtro-estado').value;
    const encendido = document.getElementById('filtro-encendido').value;
    const tipo = document.getElementById('filtro-tipo').value;
    
    const movilesFiltrados = movilesData.filter(movil => {
        // Filtro de búsqueda
        const coincideBusqueda = !busqueda || 
            (movil.patente && movil.patente.toLowerCase().includes(busqueda)) ||
            (movil.alias && movil.alias.toLowerCase().includes(busqueda)) ||
            (movil.codigo && movil.codigo.toLowerCase().includes(busqueda));
        
        // Filtro de estado
        const coincideEstado = !estado || 
            (estado === 'online' && isOnline(movil)) ||
            (estado === 'offline' && !isOnline(movil));
        
        // Filtro de encendido
        const coincideEncendido = !encendido || 
            (encendido === 'true' && movil.ignicion === true) ||
            (encendido === 'false' && movil.ignicion === false);
        
        // Filtro de tipo
        const coincideTipo = !tipo || movil.tipo_vehiculo === tipo;
        
        return coincideBusqueda && coincideEstado && coincideEncendido && coincideTipo;
    });
    
    // Actualizar tabla con datos filtrados
    const tbody = document.getElementById('tbody-moviles');
    tbody.innerHTML = '';
    
    movilesFiltrados.forEach(movil => {
        const row = createMovilRow(movil);
        tbody.appendChild(row);
    });
}

// Mostrar formulario de móvil
function mostrarFormularioMovil(movil = null) {
    const modal = new bootstrap.Modal(document.getElementById('modalMovil'));
    const titulo = document.getElementById('modalMovilTitulo');
    const form = document.getElementById('formMovil');
    
    // Limpiar formulario
    form.reset();
    
    if (movil) {
        // Editar móvil existente
        titulo.textContent = 'Editar Móvil';
        document.getElementById('movil-id').value = movil.id;
        document.getElementById('patente').value = movil.patente || '';
        document.getElementById('alias').value = movil.alias || '';
        document.getElementById('codigo').value = movil.codigo || '';
        document.getElementById('vin').value = movil.vin || '';
        document.getElementById('marca').value = movil.marca || '';
        document.getElementById('modelo').value = movil.modelo || '';
        document.getElementById('anio').value = movil.anio || '';
        document.getElementById('color').value = movil.color || '';
        document.getElementById('tipo-vehiculo').value = movil.tipo_vehiculo || '';
        document.getElementById('gps-id').value = movil.gps_id || '';
        document.getElementById('activo').checked = movil.activo !== false;
    } else {
        // Nuevo móvil
        titulo.textContent = 'Nuevo Móvil';
        document.getElementById('movil-id').value = '';
        document.getElementById('activo').checked = true;
    }
    
    modal.show();
}

// Guardar móvil
async function guardarMovil() {
    try {
        const form = document.getElementById('formMovil');
        const formData = new FormData(form);
        const movilId = document.getElementById('movil-id').value;
        
        const data = {
            patente: document.getElementById('patente').value,
            alias: document.getElementById('alias').value,
            codigo: document.getElementById('codigo').value,
            vin: document.getElementById('vin').value,
            marca: document.getElementById('marca').value,
            modelo: document.getElementById('modelo').value,
            anio: document.getElementById('anio').value ? parseInt(document.getElementById('anio').value) : null,
            color: document.getElementById('color').value,
            tipo_vehiculo: document.getElementById('tipo-vehiculo').value,
            gps_id: document.getElementById('gps-id').value,
            activo: document.getElementById('activo').checked
        };
        
        let response;
        if (movilId) {
            // Actualizar móvil existente
            response = await fetch(`${MOVILES_API_URL}${movilId}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
        } else {
            // Crear nuevo móvil
            response = await fetch(MOVILES_API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
        }
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        // Cerrar modal y recargar datos
        bootstrap.Modal.getInstance(document.getElementById('modalMovil')).hide();
        await loadMoviles();
        showAlert(movilId ? 'Móvil actualizado correctamente' : 'Móvil creado correctamente', 'success');
        
    } catch (error) {
        console.error('Error al guardar móvil:', error);
        showAlert('Error al guardar el móvil', 'danger');
    }
}

// Editar móvil
function editarMovil(id) {
    const movil = movilesData.find(m => m.id === id);
    if (movil) {
        mostrarFormularioMovil(movil);
    }
}

// Ver detalle de móvil
function verDetalleMovil(id) {
    const movil = movilesData.find(m => m.id === id);
    if (movil) {
        // Mostrar detalles en un modal o alert
        const detalles = `
            <strong>${movil.alias || movil.patente || 'Sin identificar'}</strong><br>
            <strong>Patente:</strong> ${movil.patente || 'Sin patente'}<br>
            <strong>GPS ID:</strong> ${movil.gps_id || 'Sin ID'}<br>
            <strong>Marca/Modelo:</strong> ${movil.marca || 'N/A'} ${movil.modelo || ''}<br>
            <strong>Año:</strong> ${movil.anio || 'N/A'}<br>
            <strong>Última posición:</strong> ${movil.ultimo_lat && movil.ultimo_lon ? `${movil.ultimo_lat}, ${movil.ultimo_lon}` : 'Sin datos'}<br>
            <strong>Velocidad:</strong> ${movil.ultima_velocidad_kmh || 0} km/h<br>
            <strong>Encendido:</strong> ${movil.ignicion ? 'Sí' : 'No'}<br>
            <strong>Batería:</strong> ${movil.bateria_pct || 'N/A'}%<br>
            <strong>Última actualización:</strong> ${movil.fecha_recepcion ? new Date(movil.fecha_recepcion).toLocaleString('es-ES') : 'Sin datos'}
        `;
        
        showAlert(detalles, 'info', true);
    }
}

// Eliminar móvil
async function eliminarMovil(id) {
    if (confirm('¿Está seguro de que desea eliminar este móvil?')) {
        try {
            const response = await fetch(`${MOVILES_API_URL}${id}/`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            
            await loadMoviles();
            showAlert('Móvil eliminado correctamente', 'success');
            
        } catch (error) {
            console.error('Error al eliminar móvil:', error);
            showAlert('Error al eliminar el móvil', 'danger');
        }
    }
}

// Actualizar dashboard
function updateDashboard() {
    // Mostrar móviles recientes
    const movilesRecientes = document.getElementById('moviles-recientes');
    const movilesOrdenados = movilesData
        .sort((a, b) => new Date(b.fecha_recepcion || 0) - new Date(a.fecha_recepcion || 0))
        .slice(0, 5);
    
    movilesRecientes.innerHTML = '';
    movilesOrdenados.forEach(movil => {
        const div = document.createElement('div');
        div.className = 'd-flex justify-content-between align-items-center mb-2';
        
        const online = isOnline(movil);
        const estadoIcon = online ? 
            '<i class="bi bi-wifi text-success"></i>' : 
            '<i class="bi bi-wifi-off text-danger"></i>';
        
        div.innerHTML = `
            <div>
                <strong>${movil.alias || movil.patente || 'Sin identificar'}</strong><br>
                <small class="text-muted">${movil.fecha_recepcion ? new Date(movil.fecha_recepcion).toLocaleString('es-ES') : 'Sin datos'}</small>
            </div>
            <div>${estadoIcon}</div>
        `;
        
        movilesRecientes.appendChild(div);
    });
}

// Refrescar datos
async function refreshData() {
    await loadMoviles();
    showAlert('Datos actualizados correctamente', 'success');
}

// Mostrar alertas
function showAlert(message, type = 'info', html = false) {
    // Crear elemento de alerta
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 400px;';
    
    if (html) {
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
    } else {
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
    }
    
    // Agregar al DOM
    document.body.appendChild(alertDiv);
    
    // Auto-remover después del tiempo configurado
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, WAYGPS_CONFIG.UI.ALERT_DURATION);
}

// Función para actualizar automáticamente
setInterval(() => {
    if (currentSection === 'dashboard' || currentSection === 'moviles' || currentSection === 'mapa') {
        loadMoviles();
    }
}, WAYGPS_CONFIG.AUTO_REFRESH_INTERVAL);

console.log('WayGPS Frontend cargado');
