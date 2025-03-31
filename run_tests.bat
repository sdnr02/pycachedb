@echo off
REM run_tests.bat - Run all unit tests from the root directory

echo Running all unit tests...
python -m unittest discover -s tests -v

REM Store the exit code
set EXIT_CODE=%ERRORLEVEL%

echo.
if %EXIT_CODE% EQU 0 (
    echo All tests passed!
) else (
    echo Some tests failed!
)

REM Exit with the same code as the test runner
exit /b %EXIT_CODE%