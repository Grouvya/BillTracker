# Quick Git Setup Script
# Run this in your current PowerShell session to use Git without restarting

# Refresh PATH environment variable
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host "✅ Git is now available in this session!" -ForegroundColor Green
Write-Host ""

# Verify Git is working
git --version

Write-Host ""
Write-Host "You can now run Git commands. Example:" -ForegroundColor Cyan
Write-Host "  git init" -ForegroundColor Yellow
Write-Host "  git add ." -ForegroundColor Yellow
Write-Host "  git commit -m 'Initial commit'" -ForegroundColor Yellow
