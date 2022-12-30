
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

        if ($VrJob.State -ne "Running") {
            Write-Host "Oh no! Restarting adb logcat"
            $VrJob = adb logcat -s VrApi > logcat_VrApi.log &
        }
        if ($HostJob.State -ne "Running") {
            Write-Host "Oh no! Restarting python script"
            $HostJob = python .\sample-host-metrics.py &
        }

        adb shell "cat /proc/uptime" >> uptime.log
        adb shell "cat /proc/net/dev" >> net_dev.log
        adb shell "cat /proc/meminfo" >> meminfo.log
        adb shell "cat /proc/stat" >> stat.log
        adb shell "cat /proc/loadavg" >> loadavg.log

        adb shell "dumpsys battery" >> battery.log
        adb shell "dumpsys OVRRemoteService" >> OVRRemoteService.log
        adb shell "dumpsys CompanionService" >> CompanionService.log

        $End = [System.Diagnostics.Stopwatch]::GetTimestamp()
        Do {
        $i = $i + 1
        $Next = $Start + ($i * $Freq)
        $Sleep = $Next - $End
        } While($Sleep -lt 0)
        [System.Threading.Thread]::Sleep($Sleep * (1000.0 / $Freq))
    }
}
finally {
    Write-Host "Stopping VR monitor..."
    Stop-Job $VrJob
    Write-Host "Stopping host monitor..."
    Stop-Job $HostJob
}
