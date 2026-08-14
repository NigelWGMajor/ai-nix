Write-Host ""
Write-Host "=== Ollama Processes ==="

Get-Process ollama -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "=== Loaded Models ==="

ollama ps

Write-Host ""
Write-Host "=== Installed Models ==="

ollama list
