# WAY Project - Guía para Desarrolladores Frontend

## Estructura del Proyecto
app/
├── templates/
│   ├── base.html          # Template base (NO MODIFICAR)
│   ├── index.html         # Página de inicio
│   └── [nuevas páginas]   # Tus nuevas páginas aquí
├── static/
│   ├── css/
│   │   └── style.css      # CSS base (puedes agregar más)
│   ├── js/
│   │   └── main.js        # JS base (puedes agregar más)
│   └── img/               # Imágenes aquí
└── wayproject/
├── urls.py            # URLs (coordinar con backend)
└── views.py           # Vistas (coordinar con backend)

## Para Desarrolladores Frontend

### 1. Crear una nueva página
1. Crear archivo HTML en `app/templates/`
2. Usar `{% extends 'base.html' %}` como primera línea
3. Coordinar con backend para agregar URL y vista

### 2. Ejemplo de nueva página
```html
{% extends 'base.html' %}

{% block title %}Mi Nueva Página{% endblock %}

{% block content %}
<div class="container">
    <h1>Mi contenido aquí</h1>
</div>
{% endblock %}
eof
### 3. Deploy de cambios
```bash
# En el servidor
cd /root/django-docker-project
git pull origin main
docker compose restart web

- pgAdmin: ssh -L 5050:localhost:5050 root@vps-5273003-x.dattaweb.com luego http://localhost:5050/
