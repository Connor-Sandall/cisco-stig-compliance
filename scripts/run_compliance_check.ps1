<#
.SYNOPSIS
    STIG Compliance Check Wrapper Script for Windows

.DESCRIPTION
    Use this script to run compliance checks with common options

.EXAMPLE
    .\scripts\run_compliance_check.ps1                      # Check all devices
    .\scripts\run_compliance_check.ps1 -Daily               # Daily scheduled check
    .\scripts\run_compliance_check.ps1 -Weekly              # Weekly scheduled check
    .\scripts\run_compliance_check.ps1 -Monthly             # Monthly scheduled check
    .\scripts\run_compliance_check.ps1 -Host switch01       # Check specific host
    .\scripts\run_compliance_check.ps1 -Remediate           # Run remediation
    .\scripts\run_compliance_check.ps1 -DryRun              # Dry run remediation

.PARAMETER Daily
    Run daily scheduled compliance check

.PARAMETER Weekly
    Run weekly scheduled compliance check

.PARAMETER Monthly
    Run monthly scheduled compliance check

.PARAMETER TargetHost
    Check a specific host

.PARAMETER Remediate
    Run remediation mode

.PARAMETER DryRun
    Run in dry-run mode (no changes applied)

.PARAMETER StigFile
    Path to custom STIG checklist file

.PARAMETER NoApproval
    Skip approval prompts for remediation
#>

param(
    [switch]$Daily,
    [switch]$Weekly,
    [switch]$Monthly,
    [string]$TargetHost,
    [switch]$Remediate,
    [switch]$DryRun,
    [string]$StigFile,
    [switch]$NoApproval
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir

# Determine schedule type
$ScheduleType = "manual"
if ($Daily) { $ScheduleType = "daily" }
if ($Weekly) { $ScheduleType = "weekly" }
if ($Monthly) { $ScheduleType = "monthly" }

# Build extra vars
$ExtraVars = @()
$ExtraVars += "schedule_type=$ScheduleType"

if ($DryRun) {
    $ExtraVars += "dry_run=true"
}

if ($StigFile) {
    $ExtraVars += "stig_checklist_file=$StigFile"
}

if ($NoApproval) {
    $ExtraVars += "remediation_require_approval=false"
}

# Determine playbook
if ($Remediate) {
    $Playbook = "playbooks/remediation.yml"
} elseif ($TargetHost) {
    $Playbook = "playbooks/single_device_check.yml"
    $ExtraVars += "target_host=$TargetHost"
} elseif ($ScheduleType -ne "manual") {
    $Playbook = "playbooks/scheduled_check.yml"
} else {
    $Playbook = "playbooks/compliance_check.yml"
}

# Change to project directory
Set-Location $ProjectDir

# Build command
$ExtraVarsString = $ExtraVars -join " "
$Command = "ansible-playbook $Playbook"

if ($ExtraVarsString) {
    $Command += " -e `"$ExtraVarsString`""
}

# Log start
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "========================================"
Write-Host "$Timestamp - Starting compliance check"
Write-Host "Playbook: $Playbook"
Write-Host "Schedule: $ScheduleType"
Write-Host "Extra vars: $ExtraVarsString"
Write-Host "========================================"

# Run ansible playbook
Invoke-Expression $Command
$ExitCode = $LASTEXITCODE

# Log completion
Write-Host "========================================"
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "$Timestamp - Compliance check completed with exit code: $ExitCode"

exit $ExitCode
