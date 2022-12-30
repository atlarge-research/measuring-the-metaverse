
# https://xkln.net/blog/powershell-sleep-duration-accuracy-and-windows-timers/

adb shell "cat /proc/version" > version.log
adb shell "cat /proc/cpuinfo" > cpuinfo.log

$VrJob = adb logcat -s VrApi > logcat_VrApi.log &
$HostJob = python .\sample-host-metrics.py &

$Freq = [System.Diagnostics.Stopwatch]::Frequency

$Start = [System.Diagnostics.Stopwatch]::GetTimestamp()
$i = 0

try {
    While ($True) {        
        [System.DateTime]::Now.ToString("HH:mm:ss.fff")

        adb shell "cat /proc/uptime" >> uptime.log
        adb shell "cat /proc/net/dev" >> net_dev.log
        adb shell "cat /proc/meminfo" >> meminfo.log
        adb shell "cat /proc/stat" >> stat.log
        adb shell "cat /proc/loadavg" >> loadavg.log
        adb shell "dumpsys battery" >> battery.log

        $End = [System.Diagnostics.Stopwatch]::GetTimestamp()
        $i = $i + 1
        $Next = $Start + ($i * $Freq)
        [System.Threading.Thread]::Sleep(($Next - $End) * (1000.0 / $Freq))
    }
}
finally {
    Write-Host "Stopping VR monitor..."
    Stop-Job $VrJob
    Write-Host "Stopping host monitor..."
    Stop-Job $HostJob
}
