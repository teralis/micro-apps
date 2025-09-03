@echo off
title WhatsApp Photo Extractor
echo.
echo Starting WhatsApp Photo Extractor...
echo.

REM Check if Python script exists
if not exist "whatsapp_photo_extractor.py" (
    echo Error: whatsapp_photo_extractor.py not found!
    echo Please make sure this batch file is in the same folder as the Python script.
    pause
    exit /b 1
)

REM Run the Python script in interactive mode
python whatsapp_photo_extractor.py --interactive

echo.
echo Process completed!
echo Press any key to close this window...
pause >nul