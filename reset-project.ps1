Set-Location -Path $PSScriptRoot

Write-Host "🧹 Cleaning project..."

# remove __pycache__ folders
Write-Host "🔍 Searching for __pycache__ folders..."
Get-ChildItem -Path . -Recurse -Directory -Filter '__pycache__' | ForEach-Object {
    Write-Host "🗑️  Removing $($_.FullName)"
    Remove-Item -Recurse -Force -Path $_.FullName
}
Write-Host "✅ Removed all __pycache__ folders."

# remove *.egg-info files/folders
Write-Host "🔍 Searching for *.egg-info files or folders..."
Get-ChildItem -Path . -Recurse -Force -Filter '*.egg-info' | ForEach-Object {
    Write-Host "🗑️  Removing $($_.FullName)"
    Remove-Item -Recurse -Force -Path $_.FullName
}
Write-Host "✅ Removed all *.egg-info files/folders."

# remove user-created folders
$folders = @(
    "tonic/images",
    "tonic/models",
    "tonic/predicted",
    "tonic/datasets"
)

foreach ($folder in $folders) {
    if (Test-Path $folder) {
        Remove-Item -Recurse -Force -Path $folder
        Write-Host "🗑️  Removed $folder"
    } else {
        Write-Host "ℹ️  $folder not found, skipping."
    }
}

Write-Host "✅ Cleanup complete."
