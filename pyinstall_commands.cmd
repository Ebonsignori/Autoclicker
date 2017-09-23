pyinstaller --onefile --nowindow --clean ^
--icon=".\img\icon.ico" ^
--paths=".\img:.\sounds" --distpath=".\build\dist" --workpath=".\build\build" ^
--name="Auto[Click]Mate" .\main.py