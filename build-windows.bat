@echo off
REM Install required Python packages
python -m pip install -r requirements.txt
python -m pip install pyinstaller

REM Create the build directory
if not exist build mkdir build

REM Create the work directory
if not exist build\work mkdir build\work

REM Create the spec directory
if not exist build\spec mkdir build\spec

REM Use PyInstaller to build the executable
pyinstaller --onefile --distpath build\ --workpath build\work\ --specpath build\spec\ --clean --noconfirm --log-level=WARN --name xplane-streamdeck.exe start.py

REM Copy the required files to the build directory
xcopy /E /I icons build\icons\
xcopy /E /I fonts build\fonts\
xcopy /E /I misc\LICENSE* build\
xcopy /E /I misc\*.lua build\misc\

copy config.yaml build\
copy secret.yaml build\
copy README.md build\
copy LICENSE build\

copy find_serial.py build\

REM Copy directories
xcopy /E /I 172SP build\172SP\
xcopy /E /I A320JARDesign build\A320JARDesign\
xcopy /E /I B737-800X build\B737-800X\

REM Remove the work and spec directories
rmdir /S /Q build\work
rmdir /S /Q build\spec

REM Now download and place HIDAPI DLLs next to the executable
REM Happy flying!
