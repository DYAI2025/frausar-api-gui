@echo off
echo 🔒 CSV-Tresor Build für Windows
echo ================================

echo 📦 Installiere Abhängigkeiten...
python -m pip install cryptography pyinstaller

echo 🔨 Baue CSV-Tresor.exe...
python -m PyInstaller --onefile --windowed --name "CSV-Tresor" --hidden-import cryptography --hidden-import tkinter --clean csv_tresor.py

echo 📦 Kopiere Datei...
copy dist\CSV-Tresor.exe CSV-Tresor.exe

echo 🧹 Räume auf...
rmdir /s /q build
rmdir /s /q dist
del CSV-Tresor.spec

echo ✅ Fertig! CSV-Tresor.exe wurde erstellt.
echo 💡 Einfach per Doppelklick starten!
pause 