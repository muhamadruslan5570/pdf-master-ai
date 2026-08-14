param (
    [int]$IntervalSeconds = 30
)

Write-Host "==========================================" -ForegroundColor Green
Write-Host " 🚀 Git Auto-Push Watcher Aktif...       " -ForegroundColor Yellow
Write-Host " Memantau perubahan kode di folder ini.  " -ForegroundColor Cyan
Write-Host " Tekan CTRL + C untuk menghentikan.     " -ForegroundColor Red
Write-Host "==========================================" -ForegroundColor Green

while ($true) {
    $status = git status --porcelain
    
    if ($status) {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Write-Host "[$timestamp] Perubahan terdeteksi! Mengirim ke GitHub..." -ForegroundColor Green
        
        git add .
        git commit -m "Auto-update: $timestamp"
        git push origin main
        
        Write-Host "[$timestamp] Selesai di-push ke GitHub!" -ForegroundColor Cyan
    }
    
    Start-Sleep -Seconds $IntervalSeconds
}
