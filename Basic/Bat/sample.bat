@echo off

rem Bloomberg
start "" "C:\blp\Wintrv\wintrv.exe"

rem Excel
rem start "Excel" /B /max "C:\Program Files\Microsoft Office\Office15\EXCEL.EXE" /x "C:\Users\----\US.xlsm"
start "Excel" /B /max "EXCEL.EXE" /x "C:\Users\----\010_Bat\test_forBat.xlsx"

rem Chrome
rem start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" "https://www.nikkei.com/"
start "" "chrome.exe" "https://www.nikkei.com/"

rem Python
call C:\Users\----\activate.bat
cd C:\Users\----\020_Bat
python NQ.py

S:
cd S:\----\010_CFTC
python CFTC.py
