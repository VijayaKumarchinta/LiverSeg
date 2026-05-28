<#
.SYNOPSIS
LiversegAI Deployment Preparation Script for Windows.
.DESCRIPTION
This script packages the application securely for production deployment.
It ensures sensitive files and development environments are NOT included in the final archive.
#>

Write-Host "Preparing LiversegAI for Production Deployment..."

$ReleaseDir = "liverseg_release"
$ReleaseZip = "liverseg_production.zip"

# Clean previous build if it exists
if (Test-Path $ReleaseDir) { 
    Write-Host "Cleaning up old release directory..."
    Remove-Item -Recurse -Force $ReleaseDir 
}
if (Test-Path $ReleaseZip) { 
    Write-Host "Removing old zip archive..."
    Remove-Item -Force $ReleaseZip 
}

New-Item -ItemType Directory -Force -Path $ReleaseDir | Out-Null

Write-Host "Filtering and copying source files..."

# Recursively fetch files, excluding git, node_modules, dist, python venv, and cache folders
$files = Get-ChildItem -Path . -Recurse | Where-Object {
    -not $_.PSIsContainer -and
    $_.FullName -notmatch '\\(\.git|node_modules|dist|venv|__pycache__|liverseg_release)(\\||$)' -and
    $_.Name -notmatch '^(\.env|\.env\.production|\.DS_Store|liverseg_production\.zip|deploy_prep\.ps1|deploy_prep\.sh)$'
}

$sourceRoot = (Get-Location).Path

foreach ($file in $files) {
    # Calculate target path relative to ReleaseDir
    $relativePath = $file.FullName.Substring($sourceRoot.Length).TrimStart('\')
    $targetPath = Join-Path $ReleaseDir $relativePath
    
    # Ensure parent directory exists
    $targetDir = Split-Path $targetPath
    if (-not (Test-Path $targetDir)) {
        New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
    }
    
    # Copy file
    Copy-Item -Path $file.FullName -Destination $targetPath -Force
}

Write-Host "Creating secure production zip..."
Compress-Archive -Path "$ReleaseDir\*" -DestinationPath $ReleaseZip -Force

# Cleanup temporary directory
Write-Host "Cleaning up temporary files..."
Remove-Item -Recurse -Force $ReleaseDir

Write-Host "========================================================="
Write-Host "✅ Deployment Package Ready: $ReleaseZip"
Write-Host "⚠️  REMINDER: Do NOT upload your .env files publicly."
Write-Host "   You must create a secure .env file on your production server."
Write-Host "========================================================="
