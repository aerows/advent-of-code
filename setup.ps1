# Create and activate Python virtual environment
Write-Output "Creating Python virtual environment..."
python -m venv .venv

# Activate virtual environment
if ($IsWindows) {
    .\.venv\Scripts\Activate.ps1
}
else {
    .\.venv\bin\Activate.ps1
}

# Install requirements
Write-Output "Installing requirements..."
python -m pip install -r requirements.txt
