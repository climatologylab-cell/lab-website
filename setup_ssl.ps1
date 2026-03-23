# ================================================================
# setup_ssl.ps1 - Deploy Manual GlobalSign SSL Certificates + Nginx
# Run this AFTER git pull on the EC2 server.
# ================================================================
# CERTIFICATE FILES REQUIRED (place in same folder or pass as params):
#   1. certificate.crt    - Your domain certificate (from GlobalSign)
#   2. intermediate.crt   - GlobalSign GCC R6 AlphaSSL CA 2025
#   3. cross.crt          - GlobalSign Cross Certificate R3-R6
#   4. root.crt           - GlobalSign Root R6
#   5. private.key        - Your private key (generated with CSR)
# ================================================================

param(
    [string]$Domain = "climatologylab.iitr.ac.in",
    [string]$ProjectDir = "C:\ClimatologyLab",
    [string]$NginxDir = "C:\nginx",
    [string]$NssmDir = "C:\nssm",

    # Path to your certificate files (default: same folder as this script)
    [string]$CertDir = $PSScriptRoot,

    # Individual cert filenames (change these if your filenames differ)
    [string]$DomainCert = "certificate.crt",
    [string]$IntermCert = "intermediate.crt",
    [string]$CrossCert = "cross.crt",
    [string]$RootCert = "root.crt",
    [string]$PrivateKey = "private.key"
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Climatology Lab SSL & Nginx Setup"       -ForegroundColor Cyan
Write-Host "  Domain: $Domain"                         -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# -------------------------------------------------------------------
# STEP 1: Verify all certificate files exist
# -------------------------------------------------------------------
Write-Host "`n[1/6] Verifying certificate files..." -ForegroundColor Yellow

$files = @{
    "Domain Certificate" = Join-Path $CertDir $DomainCert
    "Intermediate CA"    = Join-Path $CertDir $IntermCert
    "Cross Certificate"  = Join-Path $CertDir $CrossCert
    "Root Certificate"   = Join-Path $CertDir $RootCert
    "Private Key"        = Join-Path $CertDir $PrivateKey
}

$allFound = $true
foreach ($name in $files.Keys) {
    if (Test-Path $files[$name]) {
        Write-Host "  [OK] $name -> $($files[$name])" -ForegroundColor Green
    }
    else {
        Write-Host "  [MISSING] $name -> $($files[$name])" -ForegroundColor Red
        $allFound = $false
    }
}

if (-not $allFound) {
    Write-Host "`nERROR: One or more certificate files are missing." -ForegroundColor Red
    Write-Host "Place all cert files in: $CertDir" -ForegroundColor Yellow
    Write-Host "Or pass -CertDir <path_to_certs> when running this script." -ForegroundColor Yellow
    exit 1
}

# -------------------------------------------------------------------
# STEP 2: Create SSL directory and build the certificate chain bundle
# -------------------------------------------------------------------
Write-Host "`n[2/6] Building certificate chain bundle..." -ForegroundColor Yellow

$sslDir = Join-Path $NssmDir "ssl"
if (-not (Test-Path $sslDir)) {
    New-Item -ItemType Directory -Path $sslDir -Force | Out-Null
    Write-Host "  Created SSL directory: $sslDir" -ForegroundColor Green
}

# Nginx requires a SINGLE bundled file in this order:
#   1. Your domain certificate
#   2. Intermediate CA (GlobalSign GCC R6 AlphaSSL CA 2025)
#   3. Cross Certificate (GlobalSign Cross R3-R6)
#   4. Root (GlobalSign R6)
$bundlePath = Join-Path $sslDir "certificate.crt"
$keyPath = Join-Path $sslDir "private.key"

$domainContent = Get-Content -Path $files["Domain Certificate"] -Raw
$intermContent = Get-Content -Path $files["Intermediate CA"]    -Raw
$crossContent = Get-Content -Path $files["Cross Certificate"]  -Raw
$rootContent = Get-Content -Path $files["Root Certificate"]   -Raw

# Ensure each cert ends with a newline before concatenation
$bundle = $domainContent.TrimEnd() + "`n" +
$intermContent.TrimEnd() + "`n" +
$crossContent.TrimEnd() + "`n" +
$rootContent.TrimEnd() + "`n"

Set-Content -Path $bundlePath -Value $bundle -NoNewline
Write-Host "  Certificate chain bundle created: $bundlePath" -ForegroundColor Green

# Copy private key
Copy-Item -Path $files["Private Key"] -Destination $keyPath -Force
Write-Host "  Private key copied to: $keyPath" -ForegroundColor Green

# -------------------------------------------------------------------
# STEP 3: Download and Install Nginx (if not present)
# -------------------------------------------------------------------
Write-Host "`n[3/6] Checking Nginx installation..." -ForegroundColor Yellow
if (-not (Test-Path $NginxDir)) {
    $nginxUrl = "https://nginx.org/download/nginx-1.24.0.zip"
    $zipPath = Join-Path $env:TEMP "nginx.zip"
    Write-Host "  Downloading Nginx..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $nginxUrl -OutFile $zipPath
    Expand-Archive -Path $zipPath -DestinationPath "C:\" -Force
    Rename-Item "C:\nginx-1.24.0" $NginxDir
    Remove-Item $zipPath -Force
    Write-Host "  Nginx installed at $NginxDir" -ForegroundColor Green
}
else {
    Write-Host "  Nginx already installed at $NginxDir" -ForegroundColor Green
}

# -------------------------------------------------------------------
# STEP 4: Copy Nginx config
# -------------------------------------------------------------------
Write-Host "`n[4/6] Deploying Nginx config..." -ForegroundColor Yellow
$confSrc = Join-Path $ProjectDir "nginx.conf"
$confDest = Join-Path $NginxDir "conf\nginx.conf"

if (Test-Path $confSrc) {
    Copy-Item $confSrc $confDest -Force
    Write-Host "  nginx.conf copied to $confDest" -ForegroundColor Green
}
else {
    Write-Host "  ERROR: nginx.conf not found in $ProjectDir" -ForegroundColor Red
    exit 1
}

# Test nginx config before restarting
$nginxExe = Join-Path $NginxDir "nginx.exe"
Write-Host "  Testing Nginx config syntax..." -ForegroundColor Yellow
$testResult = & $nginxExe -t 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  Nginx config is valid!" -ForegroundColor Green
}
else {
    Write-Host "  WARNING: Nginx config test output:" -ForegroundColor Yellow
    Write-Host $testResult -ForegroundColor Red
}

# -------------------------------------------------------------------
# STEP 5: Register/Restart Nginx as a Windows Service via NSSM
# -------------------------------------------------------------------
Write-Host "`n[5/6] Setting up Nginx Windows Service..." -ForegroundColor Yellow
$nssmExe = Join-Path $NssmDir "nssm.exe"
if (-not (Test-Path $nssmExe)) {
    Write-Host "  ERROR: NSSM not found at $nssmExe. Run install_service.ps1 first!" -ForegroundColor Red
    exit 1
}

$svcName = "NginxService"
$existingSvc = Get-Service -Name $svcName -ErrorAction SilentlyContinue

if ($existingSvc) {
    Write-Host "  Restarting existing NginxService..." -ForegroundColor Yellow
    & $nssmExe restart $svcName
}
else {
    Write-Host "  Installing NginxService..." -ForegroundColor Yellow
    & $nssmExe install $svcName $nginxExe
    & $nssmExe set $svcName AppDirectory $NginxDir
    & $nssmExe start $svcName
}

Write-Host "  NginxService is running!" -ForegroundColor Green

# -------------------------------------------------------------------
# STEP 6: Open Port 443 in Windows Firewall
# -------------------------------------------------------------------
Write-Host "`n[6/6] Checking Windows Firewall for Port 443..." -ForegroundColor Yellow
$ruleName = "Allow HTTPS (Port 443)"
if (-not (Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue)) {
    New-NetFirewallRule -DisplayName $ruleName -Direction Inbound -Protocol TCP -LocalPort 443 -Action Allow
    Write-Host "  Firewall rule created for Port 443" -ForegroundColor Green
}
else {
    Write-Host "  Firewall rule for Port 443 already exists" -ForegroundColor Green
}

# -------------------------------------------------------------------
# SUMMARY
# -------------------------------------------------------------------
Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "  SETUP COMPLETE!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Certificate Bundle : $bundlePath" -ForegroundColor White
Write-Host "Private Key        : $keyPath"    -ForegroundColor White
Write-Host ""
Write-Host "REMAINING AWS STEPS:" -ForegroundColor Yellow
Write-Host "  1. Go to AWS Console -> EC2 -> Security Groups"
Write-Host "  2. Add Inbound Rule: Type=HTTPS, Port=443, Source=0.0.0.0/0"
Write-Host ""
Write-Host "TEST YOUR SSL:" -ForegroundColor Yellow
Write-Host "  https://www.ssllabs.com/ssltest/analyze.html?d=$Domain"
Write-Host ""
Write-Host "If Nginx fails to start, check logs at:"
Write-Host "  $NginxDir\logs\error.log" -ForegroundColor White
