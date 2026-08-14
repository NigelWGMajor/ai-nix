ollama run deepseek-coder-v2
Write-Host "Configuring Ollama for  deepseek-coder-v2 ..."

# Limit resource usage
[Environment]::SetEnvironmentVariable(
    "OLLAMA_MAX_LOADED_MODELS",
    "1",
    "User"
)

[Environment]::SetEnvironmentVariable(
    "OLLAMA_NUM_PARALLEL",
    "1",
    "User"
)

# Listen on all interfaces
[Environment]::SetEnvironmentVariable(
    "OLLAMA_HOST",
    "0.0.0.0:11434",
    "User"
)

# Pull model
ollama pull  deepseek-coder-v2

# Create optimized model
@"
FROM deepseek-coder-v2

PARAMETER num_ctx 4096
PARAMETER temperature 0.1
PARAMETER repeat_penalty 1.1
"@ | Set-Content "$env:TEMP\Modelfile"

ollama create deepseek-coder-fast -f "$env:TEMP\Modelfile"

Write-Host ""
Write-Host *** "Model created."
Write-Host ""
Write-Host "*** Start server using:"
Write-Host "    ollama serve"
Write-Host ""
