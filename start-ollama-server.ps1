Write-Host "Starting Ollama..."

Start-Process ollama -ArgumentList "serve"

Start-Sleep -Seconds 5

Write-Host ""
Write-Host "Models available:"
ollama list