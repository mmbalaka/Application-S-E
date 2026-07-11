@echo off
REM ============================================================
REM  Lumiere du Soleil - Application S&E
REM  Double-cliquez sur ce fichier pour demarrer l'application.
REM  Fermez cette fenetre (ou Ctrl+C) pour l'arreter.
REM ============================================================
cd /d "%~dp0"
title Lumiere du Soleil - Application S&E

REM Verifier que l'environnement Python existe
if not exist ".venv\Scripts\python.exe" (
  echo.
  echo   ERREUR : l'environnement Python est introuvable.
  echo   Contactez le support technique.
  echo.
  pause
  exit /b 1
)

echo.
echo   ================================================
echo     Demarrage de l'application Lumiere du Soleil
echo   ================================================
echo.
echo   Patientez quelques secondes...
echo   Votre navigateur va s'ouvrir automatiquement.
echo.
echo   IMPORTANT : laissez cette fenetre OUVERTE.
echo   Pour arreter l'application : fermez cette fenetre.
echo.

REM Ouvrir le navigateur APRES un court delai (le temps que le serveur demarre)
start "" cmd /c "timeout /t 5 >nul & start http://127.0.0.1:8000/"

REM Demarrer le serveur (occupe cette fenetre tant que l'application tourne)
".venv\Scripts\python.exe" manage.py runserver

REM Si le serveur s'arrete, garder la fenetre ouverte pour lire un eventuel message
echo.
echo   L'application est arretee.
pause
