# Quick Reference Guide

## Common Commands

### Compliance Checks

```bash
# Check all devices
ansible-playbook playbooks/compliance_check.yml

# Check single device
ansible-playbook playbooks/single_device_check.yml -e "target_host=switch01"

# Check with custom STIG file
ansible-playbook playbooks/compliance_check.yml -e "stig_checklist_file=path/to/file.ckl"

# Check only critical (CAT I) findings
ansible-playbook playbooks/compliance_check.yml -e "stig_severity_filter=['CAT_I']"

# Check specific host group
ansible-playbook playbooks/compliance_check.yml --limit cisco_routers
```

### Remediation

```bash
# Remediate with prompts
ansible-playbook playbooks/remediation.yml

# Dry run (show changes only)
ansible-playbook playbooks/remediation.yml -e "dry_run=true"

# Auto-approve (no prompts)
ansible-playbook playbooks/remediation.yml -e "remediation_require_approval=false"

# Single device remediation
ansible-playbook playbooks/remediation.yml --limit router01
```

### Scheduling (Windows PowerShell)

```powershell
# Setup daily check
.\scripts\setup_schedule.ps1 -Daily

# Setup all schedules
.\scripts\setup_schedule.ps1 -All

# View schedules
.\scripts\setup_schedule.ps1 -Show

# Remove all schedules
.\scripts\setup_schedule.ps1 -Remove
```

### Scheduling (Linux/macOS Bash)

```bash
# Setup daily check
./scripts/setup_schedule.sh --daily

# Setup all schedules
./scripts/setup_schedule.sh --all

# View schedules
./scripts/setup_schedule.sh --show

# Remove all schedules
./scripts/setup_schedule.sh --remove
```

## Wrapper Script Options

### Windows (run_compliance_check.ps1)

```powershell
.\scripts\run_compliance_check.ps1                      # All devices
.\scripts\run_compliance_check.ps1 -Daily               # Daily schedule
.\scripts\run_compliance_check.ps1 -Weekly              # Weekly schedule
.\scripts\run_compliance_check.ps1 -Monthly             # Monthly schedule
.\scripts\run_compliance_check.ps1 -TargetHost switch01 # Single device
.\scripts\run_compliance_check.ps1 -Remediate           # Run remediation
.\scripts\run_compliance_check.ps1 -DryRun              # Dry run
.\scripts\run_compliance_check.ps1 -NoApproval          # Skip prompts
.\scripts\run_compliance_check.ps1 -StigFile "path"     # Custom STIG
```

### Linux/macOS (run_compliance_check.sh)

```bash
./scripts/run_compliance_check.sh                       # All devices
./scripts/run_compliance_check.sh --daily               # Daily schedule
./scripts/run_compliance_check.sh --weekly              # Weekly schedule
./scripts/run_compliance_check.sh --monthly             # Monthly schedule
./scripts/run_compliance_check.sh --host switch01       # Single device
./scripts/run_compliance_check.sh --remediate           # Run remediation
./scripts/run_compliance_check.sh --dry-run             # Dry run
./scripts/run_compliance_check.sh --no-approval         # Skip prompts
./scripts/run_compliance_check.sh --stig-file "path"    # Custom STIG
```

## Report Locations

| Report Type | Location |
|-------------|----------|
| Latest Consolidated | `reports/latest/consolidated_report.html` |
| Latest Executive | `reports/latest/executive_summary.html` |
| Daily Reports | `reports/daily/YYYY-MM-DD/` |
| Weekly Reports | `reports/weekly/YYYY-MM-DD/` |
| Monthly Reports | `reports/monthly/YYYY-MM-DD/` |
| Manual Reports | `reports/manual/YYYY-MM-DD/` |
| Report Index | `reports/index.html` |

## File Locations

| File Type | Location |
|-----------|----------|
| Device Inventory | `inventories/production/hosts.yml` |
| Credentials | `group_vars/vault.yml` |
| Global Settings | `group_vars/all.yml` |
| STIG Checklists | `stig_checklists/current/` |
| Config Backups | `backups/<hostname>/` |
| Ansible Logs | `logs/ansible.log` |
| Scheduled Logs | `logs/cron_*.log` |

## Useful Ansible Commands

```bash
# List all hosts
ansible-inventory --list

# Ping all devices
ansible cisco_devices -m ping

# Run ad-hoc command
ansible cisco_devices -m cisco.ios.ios_command -a "commands='show version'"

# View vault contents
ansible-vault view group_vars/vault.yml

# Edit vault
ansible-vault edit group_vars/vault.yml

# Check playbook syntax
ansible-playbook playbooks/compliance_check.yml --syntax-check

# List tasks in playbook
ansible-playbook playbooks/compliance_check.yml --list-tasks
```

## Severity Levels

| Category | Severity | Description |
|----------|----------|-------------|
| CAT I | High | Critical vulnerabilities, must fix immediately |
| CAT II | Medium | Significant vulnerabilities, fix as soon as possible |
| CAT III | Low | Minor vulnerabilities, fix when practical |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error during execution |
| 2 | Playbook/syntax error |
| 4 | Some hosts unreachable |
| 5 | Some hosts had failures |
