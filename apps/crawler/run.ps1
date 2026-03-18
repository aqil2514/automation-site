$PYTHON = "./venv/Scripts/python.exe"
$WATCH = "watchmedo auto-restart --patterns='*.py' --recursive --"

function Start-Dev {
    Write-Host "Starting Development Mode (Auto-reload)..." -ForegroundColor Cyan
    Invoke-Expression "$WATCH $PYTHON -m src.app.main"
}

function Start-Run {
    Write-Host "Starting Production Mode..." -ForegroundColor Green
    Invoke-Expression "$PYTHON -m src.app.main"
}

function Start-Clean{
    Write-Host "Clean All Python Cache" -ForegroundColor Blue
    Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
    Write-Host "Done!" -ForegroundColor Blue
}

if ($args[0] -eq "dev") { Start-Dev }
elseif ($args[0] -eq "run") { Start-Run }
elseif ($args[0] -eq "clean") {Start-Clean}
else {
    Write-Host "Usage: ./run.ps1 [dev|run]" -ForegroundColor Yellow
}