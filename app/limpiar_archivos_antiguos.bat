@echo off
echo ========================================
echo Limpieza de archivos antiguos - WayGPS
echo ========================================
echo.
echo Este script eliminara los archivos antiguos de la raiz:
echo - index.html
echo - app.js
echo - styles.css
echo - config.js
echo.
echo ADVERTENCIA: Asegurate de que la nueva estructura funcione correctamente antes de ejecutar este script!
echo.
echo ========================================
echo.

:menu
echo Opciones:
echo 1. Eliminar archivos antiguos
echo 2. Mover archivos antiguos a carpeta "backup"
echo 3. Cancelar
echo.
set /p opcion="Selecciona una opcion (1, 2 o 3): "

if "%opcion%"=="1" goto eliminar
if "%opcion%"=="2" goto backup
if "%opcion%"=="3" goto cancelar
echo Opcion invalida. Intenta de nuevo.
echo.
goto menu

:eliminar
echo.
echo Eliminando archivos antiguos...
if exist index.html del index.html && echo - index.html eliminado
if exist app.js del app.js && echo - app.js eliminado
if exist styles.css del styles.css && echo - styles.css eliminado
if exist config.js del config.js && echo - config.js eliminado (el de la raiz)
echo.
echo Archivos eliminados exitosamente!
goto fin

:backup
echo.
echo Creando carpeta backup...
if not exist backup mkdir backup
echo Moviendo archivos a backup...
if exist index.html move index.html backup\index.html.bak && echo - index.html movido
if exist app.js move app.js backup\app.js.bak && echo - app.js movido
if exist styles.css move styles.css backup\styles.css.bak && echo - styles.css movido
if exist config.js move config.js backup\config.js.bak && echo - config.js movido
echo.
echo Archivos movidos a carpeta backup/ exitosamente!
echo Puedes eliminar la carpeta backup/ cuando estes seguro.
goto fin

:cancelar
echo.
echo Operacion cancelada.
goto fin

:fin
echo.
echo ========================================
echo Proceso completado
echo ========================================
pause

