@echo off
echo.
echo -----------------------------------------------------------------------------------------------
echo Activando entorno virtual de Python
call venv\Scripts\activate.bat
@echo Entorno virtual activado. Escribe 'deactivate' para salir
cd mysite
python manage.py runserver
@cmd /k
