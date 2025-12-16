@echo off
REM Docker Build and Run Script for AI Stock Market Hybrid Project (Windows)

echo 🐳 Building Docker image for AI Stock Market Hybrid Project...

REM Build the Docker image
docker build -t stock-market-hybrid-ai .

if %errorlevel% equ 0 (
    echo ✅ Docker image built successfully!
    echo.
    echo 🚀 Running container with demo data...
    echo    (Use 'docker run -it stock-market-hybrid-ai --help' to see all options)
    echo.
    
    REM Run the container with demo data
    docker run --rm stock-market-hybrid-ai
    
    echo.
    echo 💡 Usage examples:
    echo    # Run with demo data:
    echo    docker run --rm stock-market-hybrid-ai
    echo.
    echo    # Run with custom macro data:
    echo    docker run --rm stock-market-hybrid-ai --macro-json "{\"inflation_rate\":3.1,\"interest_rate\":5.25,\"unemployment_rate\":4.1,\"GDP_growth\":2.0,\"sp500_index\":4500}" --text "Tech earnings strong"
    echo.
    echo    # Run with custom text:
    echo    docker run --rm stock-market-hybrid-ai --text "Healthcare sector sees growth, oil prices stable"
    echo.
    echo    # Interactive mode:
    echo    docker run -it stock-market-hybrid-ai --help
    
) else (
    echo ❌ Docker build failed!
    exit /b 1
)
