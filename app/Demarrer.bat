@echo off
REM ============================================================
REM  Lumiere du Soleil - Application S&E
REM  Double-cliquez sur ce fichier pour demarrer l'application.
REM  Fermez cette fenetre (ou Ctrl+C) pour l'arreter.
REM ============================================================
cd /d "%~dp0"
echo.
echo   Demarrage de l'application S^&E...
echo   Votre navigateur va s'ouvrir sur http://127.0.0.1:8000/
echo.
start "" http://127.0.0.1:8000/admin/
".venv\Scripts\python.exe" manage.py runserver
pause
