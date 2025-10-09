@echo off
echo ========================================
echo Instalacion de django-cors-headers
echo ========================================
echo.

echo Instalando dependencias...
pip install django-cors-headers
echo.

echo ========================================
echo Instalacion completada!
echo ========================================
echo.
echo Ahora debes reiniciar tu servidor Django:
echo 1. Presiona Ctrl+C en la terminal donde corre Django
echo 2. Ejecuta: python manage.py runserver
echo.

pause
