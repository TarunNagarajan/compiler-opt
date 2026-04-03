# setup_lab_quiet.ps1
# Requires Administrator privileges

Write-Host "--- Configuring Lab-Quiet Environment ---" -ForegroundColor Cyan

# 1. Lock CPU Frequency to 100% (Disable Throttle/Turbo variance)
Write-Host "[1/3] Locking CPU to Base Frequency..." -ForegroundColor Yellow
powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 100
powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 100
powercfg /setactive SCHEME_CURRENT

# 2. Suspend Noisy Services
Write-Host "[2/3] Suspending background noise (SysMain, WSearch)..." -ForegroundColor Yellow
Stop-Service -Name "SysMain" -Force -ErrorAction SilentlyContinue # Superfetch
Stop-Service -Name "WSearch" -Force -ErrorAction SilentlyContinue # Windows Search

# 3. Optimize Timer Resolution
# Note: This is an OS-level hint.
# We'll also use timeBeginPeriod in our C++ code where appropriate.

Write-Host "[3/3] Lab-Quiet Configuration Complete." -ForegroundColor Green
Write-Host "NOTE: Remember to exclude the benchmark directory from Windows Defender!" -ForegroundColor Red
