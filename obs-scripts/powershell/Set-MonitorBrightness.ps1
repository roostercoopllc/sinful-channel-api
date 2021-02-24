function Set-MonitorBrighness {
[CmdletBinding()]
param (
[ValidateRange(0,100)]
[int]$brightness
)            

$mymonitor = Get-WmiObject -Namespace rootwmi -Class WmiMonitorBrightnessMethods
$mymonitor.wmisetbrightness(5,$brightness)
}