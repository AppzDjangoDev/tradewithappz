# Start ngrok and get the URL
Start-Process -NoNewWindow -FilePath "ngrok.exe" -ArgumentList "http 8000" -RedirectStandardOutput ngrok.log

# Wait for ngrok to start and retrieve the URL
$ngrok_url = $null
while (-not $ngrok_url) {
    Start-Sleep -Seconds 1
    try {
        $ngrok_url = (Invoke-RestMethod http://127.0.0.1:4040/api/tunnels | Select-Object -ExpandProperty tunnels | Where-Object {$_.proto -eq 'https'}).public_url
    } catch {
        # Handle the case where the REST method fails (e.g., ngrok not yet started)
        $ngrok_url = $null
    }
}

# Print the new URL
Write-Output "Ngrok URL: $ngrok_url"

# Update or add the NGROK_URL in the .env file in the desired format
$env_file = ".env"
if (Test-Path $env_file) {
    $env_content = Get-Content $env_file
    if ($env_content -match 'NGROK_URL=') {
        $updated_env_content = $env_content -replace 'NGROK_URL=.*', "NGROK_URL=`"$ngrok_url`""
    } else {
        $updated_env_content = $env_content + "`r`nNGROK_URL=`"$ngrok_url`""
    }
    $updated_env_content | Set-Content $env_file
} else {
    "NGROK_URL=`"$ngrok_url`"" | Out-File $env_file
}

# Start the docker-compose services
Start-Process -NoNewWindow -FilePath "docker-compose.exe" -ArgumentList "up"

# Open URLs in Microsoft Edge and arrange the windows
Start-Process "msedge.exe" -ArgumentList $ngrok_url
Start-Sleep -Seconds 5 # Wait for Edge to start


# Get Edge processes
$ngrokEdge = Get-Process -Name msedge | Where-Object { $_.MainWindowTitle -match "ngrok" }

# Arrange Edge windows
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class WindowHelper {
    [DllImport("user32.dll")]
    public static extern bool SetWindowPos(IntPtr hWnd, IntPtr hWndInsertAfter, int X, int Y, int cx, int cy, uint uFlags);
}
"@

$SWP_NOSIZE = 0x0001
$SWP_NOMOVE = 0x0002
$HWND_TOP = [IntPtr]::Zero

$screenWidth = [System.Windows.SystemParameters]::PrimaryScreenWidth
$screenHeight = [System.Windows.SystemParameters]::PrimaryScreenHeight

# 20% width for ngrok
$ngrokWidth = [math]::Round($screenWidth * 0.2)
$ngrokHeight = $screenHeight
$ngrokX = 0
$ngrokY = 0

# Set window positions
[WindowHelper]::SetWindowPos($ngrokEdge.MainWindowHandle, $HWND_TOP, $ngrokX, $ngrokY, $ngrokWidth, $ngrokHeight, $SWP_NOSIZE -bor $SWP_NOMOVE)

# Print the ngrok URL in real-time (this keeps the script running and printing the URL)
while ($true) {
    Write-Output "Ngrok URL: $ngrok_url"
    Start-Sleep -Seconds 60
}
