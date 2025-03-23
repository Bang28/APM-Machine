@echo off
cd /d C:\Users\ruri\Desktop\Projek\Analisis_Prediktif

echo Mengaktifkan virtual environment...
call venv\Scripts\activate

echo Menjalankan Django di mode production...
cd predictive_maintenance
set DJANGO_SETTINGS_MODULE=predictive_maintenance.settings
set PYTHONUNBUFFERED=1
python manage.py runserver 0.0.0.0:8000 --insecure

pause
