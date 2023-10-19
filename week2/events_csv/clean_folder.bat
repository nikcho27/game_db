@echo off

::This is for testing only. 
:: Change to curr dir
cd /d "%~dp0"

:: Get script name
set script_name=%~n0

:: Delete all files in the current folder except the script itself
for %%i in (*) do (
    if not "%%i"=="%script_name%.bat" (
        del /q "%%i"
    )
)

:: Print done
echo Done:]
