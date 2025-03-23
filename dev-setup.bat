@echo off
echo Setting up development environment for Book Summarizer...

REM Create directories if they don't exist
if not exist uploads mkdir uploads
if not exist outputs mkdir outputs

REM Check if Docker is installed
docker --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Docker is not installed or not in PATH. Please install Docker Desktop for Windows.
    exit /b 1
)

REM Check if Docker is running
docker info > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Docker does not seem to be running. Please start Docker Desktop.
    exit /b 1
)

echo Starting Ollama and Book Summarizer with Docker Compose...
docker-compose up -d

echo.
echo Setup complete! Your Book Summarizer app should be available at:
echo http://localhost:8501
echo.
echo To stop the services, run: docker-compose down