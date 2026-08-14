Write-Host "Stopping Ollama..."

Get-Process ollama -ErrorAction SilentlyContinue |
    Stop-Process -Force

Start-Sleep -Seconds 2

if (Get-Process ollama -ErrorAction SilentlyContinue)
{
    Write-Host "WARNING: Ollama still appears to be running."
}
else
{
    Write-Host "SUCCESS: Ollama stopped."
}
