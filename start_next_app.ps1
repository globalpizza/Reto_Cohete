# start_next_app.ps1 - Inicia la aplicación Next.js
# -----------------------------------------------------------------------------

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "               🚀 NEXT.JS ROCKET SIMULATOR 🚀" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio next_app
Set-Location -Path "next_app"

Write-Host "📂 Directorio actual: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# Verificar si node_modules existe
if (-not (Test-Path "node_modules")) {
    Write-Host "⚠️  node_modules no encontrado. Instalando dependencias..." -ForegroundColor Yellow
    Write-Host ""
    npm install
    Write-Host ""
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error al instalar dependencias." -ForegroundColor Red
        Write-Host "💡 Asegúrate de tener Node.js y npm instalados." -ForegroundColor Yellow
        Write-Host "   Descarga desde: https://nodejs.org/" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "✅ Dependencias instaladas correctamente" -ForegroundColor Green
    Write-Host ""
}

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "🚀 Iniciando servidor de desarrollo Next.js..." -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 URL: http://localhost:3000" -ForegroundColor Yellow
Write-Host "⏹️  Para detener: Presiona Ctrl+C" -ForegroundColor Yellow
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Iniciar el servidor de desarrollo
npm run dev
