Write-Host "Building Q-Slidee EXE..." -ForegroundColor Cyan

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

& .\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
pip install -r requirements-dev.txt

pyinstaller --noconfirm --clean q-slidee.spec

Write-Host "Done. EXE output: dist\\Q-Slidee.exe" -ForegroundColor Green
