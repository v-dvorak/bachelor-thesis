# requires PowerShell 5.0+
param (
    [Parameter(Mandatory = $true)]
    [string]$Python
)

# switch to script directory
Set-Location -Path $PSScriptRoot

Write-Host "🐍 Creating virtual environment..."
& $Python -m venv .venv

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create virtual environment"
    exit 1
}

Write-Host "🐍 Updating pip..."
& .\.venv\Scripts\pip.exe install --upgrade pip

Write-Host "✅ Virtual environment created at .\.venv"

Write-Host "📦 Installing StaLiX..."
Set-Location -Path "stalix"
& ..\.venv\Scripts\pip.exe install -e .[viz]
Set-Location -Path ..

Write-Host "📦 Installing od-tools..."
Set-Location -Path "od-tools"
& ..\.venv\Scripts\pip.exe install -e .
Set-Location -Path ..

Write-Host "📦 Installing TonIC dependencies..."
Set-Location -Path "tonic"
& ..\.venv\Scripts\pip.exe install -r requirements.txt
Set-Location -Path ..

Write-Host "🐍 Verifying installation..."
& .\.venv\Scripts\python.exe -c "import odtools, stalix; print('✅ Libraries od-tools and StaLiX are importable.')"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Import test failed. Please check installation."
    exit 1
}

Write-Host "🎉 Done!"
