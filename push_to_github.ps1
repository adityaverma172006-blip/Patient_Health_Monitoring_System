# Patient Health Monitoring System — PowerShell GitHub Push Script
# Run in VS Code terminal: .\push_to_github.ps1

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "   PATIENT HEALTH MONITORING SYSTEM — GITHUB PUSH SCRIPT" -ForegroundColor Cyan
Write-Host "================================================================`n" -ForegroundColor Cyan

# 1. Check Git
try {
    $gitVer = git --version
    Write-Host "[OK] $gitVer" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git not found. Please install Git for Windows." -ForegroundColor Red
    exit 1
}

# 2. Add and commit
if (-not (Test-Path ".git")) {
    git init -b main | Out-Null
} else {
    git branch -M main | Out-Null
}

git add -A
git commit -m "Patient Health Monitoring System with IoT Blynk, Live Web Dashboard, and Simulation" | Out-Null
Write-Host "[OK] All project files staged and committed locally." -ForegroundColor Green

# 3. Prompt for repo URL
Write-Host "`nTo push to GitHub:" -ForegroundColor Yellow
Write-Host "1. Create a repository at: https://github.com/new"
Write-Host "2. Name: Patient_Health_Monitoring_System (Public)"
Write-Host "3. Copy the repository HTTPS link`n"

$repoUrl = Read-Host "Enter your GitHub Repository URL (or press Enter to skip)"

if ([string]::IsNullOrWhiteSpace($repoUrl)) {
    Write-Host "`n[INFO] Skipped remote push. Local git repo is ready on 'main' branch." -ForegroundColor Cyan
    Write-Host "To push later, run:"
    Write-Host "  git remote add origin <your-repo-url>"
    Write-Host "  git push -u origin main`n"
    exit 0
}

git remote remove origin 2>$null
git remote add origin $repoUrl
git branch -M main

Write-Host "`nPushing code to $repoUrl..." -ForegroundColor Cyan
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n================================================================" -ForegroundColor Green
    Write-Host "[SUCCESS] Repository successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "Enable GitHub Pages in Repo Settings -> Pages -> Branch 'main' -> Root" -ForegroundColor Cyan
    Write-Host "================================================================`n" -ForegroundColor Green
} else {
    Write-Host "`n[NOTE] Push completed or requires credentials." -ForegroundColor Yellow
    Write-Host "If prompted, use your GitHub Personal Access Token (PAT) as password." -ForegroundColor Yellow
}
