<#
.SYNOPSIS
    Setup Scheduled Compliance Checks for Windows Task Scheduler

.DESCRIPTION
    Creates Windows Scheduled Tasks for daily, weekly, and monthly compliance checks

.EXAMPLE
    .\scripts\setup_schedule.ps1 -Daily     # Setup daily only
    .\scripts\setup_schedule.ps1 -All       # Setup all schedules
    .\scripts\setup_schedule.ps1 -Remove    # Remove all schedules
    .\scripts\setup_schedule.ps1 -Show      # Show current schedules
#>

param(
    [switch]$Daily,
    [switch]$Weekly,
    [switch]$Monthly,
    [switch]$All,
    [switch]$Remove,
    [switch]$Show
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir
$TaskPrefix = "CiscoSTIGCompliance"

function Setup-DailyTask {
    Write-Host "Setting up daily compliance check..."

    $Action = New-ScheduledTaskAction `
        -Execute "powershell.exe" `
        -Argument "-ExecutionPolicy Bypass -File `"$ProjectDir\scripts\run_compliance_check.ps1`" -Daily" `
        -WorkingDirectory $ProjectDir

    $Trigger = New-ScheduledTaskTrigger -Daily -At "6:00AM"

    $Settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable

    Register-ScheduledTask `
        -TaskName "$TaskPrefix-Daily" `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -Description "Daily STIG Compliance Check" `
        -Force

    Write-Host "Daily check scheduled for 6:00 AM"
}

function Setup-WeeklyTask {
    Write-Host "Setting up weekly compliance check..."

    $Action = New-ScheduledTaskAction `
        -Execute "powershell.exe" `
        -Argument "-ExecutionPolicy Bypass -File `"$ProjectDir\scripts\run_compliance_check.ps1`" -Weekly" `
        -WorkingDirectory $ProjectDir

    $Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At "6:00AM"

    $Settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable

    Register-ScheduledTask `
        -TaskName "$TaskPrefix-Weekly" `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -Description "Weekly STIG Compliance Check" `
        -Force

    Write-Host "Weekly check scheduled for Sundays at 6:00 AM"
}

function Setup-MonthlyTask {
    Write-Host "Setting up monthly compliance check..."

    $Action = New-ScheduledTaskAction `
        -Execute "powershell.exe" `
        -Argument "-ExecutionPolicy Bypass -File `"$ProjectDir\scripts\run_compliance_check.ps1`" -Monthly" `
        -WorkingDirectory $ProjectDir

    $Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -WeeksInterval 4 -At "6:00AM"

    $Settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable

    Register-ScheduledTask `
        -TaskName "$TaskPrefix-Monthly" `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -Description "Monthly STIG Compliance Check" `
        -Force

    Write-Host "Monthly check scheduled"
}

function Remove-AllTasks {
    Write-Host "Removing all scheduled compliance checks..."

    Get-ScheduledTask -TaskName "$TaskPrefix*" -ErrorAction SilentlyContinue | ForEach-Object {
        Unregister-ScheduledTask -TaskName $_.TaskName -Confirm:$false
        Write-Host "Removed: $($_.TaskName)"
    }

    Write-Host "All schedules removed"
}

function Show-Tasks {
    Write-Host "Current STIG Compliance Scheduled Tasks:"
    Write-Host "========================================="

    $Tasks = Get-ScheduledTask -TaskName "$TaskPrefix*" -ErrorAction SilentlyContinue

    if ($Tasks) {
        $Tasks | Format-Table TaskName, State, @{L='NextRunTime';E={($_ | Get-ScheduledTaskInfo).NextRunTime}} -AutoSize
    } else {
        Write-Host "No scheduled tasks found"
    }
}

# Main logic
if ($Daily) { Setup-DailyTask }
elseif ($Weekly) { Setup-WeeklyTask }
elseif ($Monthly) { Setup-MonthlyTask }
elseif ($All) {
    Setup-DailyTask
    Setup-WeeklyTask
    Setup-MonthlyTask
}
elseif ($Remove) { Remove-AllTasks }
elseif ($Show) { Show-Tasks }
else {
    Write-Host "STIG Compliance Schedule Setup"
    Write-Host "=============================="
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Daily    Setup daily check (6:00 AM)"
    Write-Host "  -Weekly   Setup weekly check (Sundays 6:00 AM)"
    Write-Host "  -Monthly  Setup monthly check"
    Write-Host "  -All      Setup all schedules"
    Write-Host "  -Remove   Remove all schedules"
    Write-Host "  -Show     Show current schedules"
    Write-Host ""
    Show-Tasks
}
