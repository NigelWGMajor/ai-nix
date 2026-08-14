Write-Host "Configuring Ollama for fast Qwen2.5:3b-instruct..."

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
ollama pull qwen2.5-coder:3b-instruct

# Create optimized model
@"
FROM qwen2.5-coder:3b-instruct

PARAMETER num_ctx 4096
PARAMETER temperature 0.1
PARAMETER repeat_penalty 1.1
"@ | Set-Content "$env:TEMP\Modelfile"

ollama create qwen-coder-fast -f "$env:TEMP\Modelfile"

Write-Host ""
Write-Host *** "Model created."
Write-Host ""
Write-Host "*** Start server using:"
Write-Host "    ollama serve"
Write-Host ""
