# Cisco STIG Compliance Checker - Quick Reference Guide

## Quick Start Commands

### Initial Setup
```bash
# Navigate to project directory
cd "E:\01- Chrome Downloads\cisco-stig-compliance"

# Activate virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
ansible-galaxy collection install -r requirements.yml
```

### Daily Operations

#### Run Compliance Check
```bash
# Check all devices
ansible-playbook compliance-check.yml

# Check specific device
ansible-playbook compliance-check.yml --limit switch01.example.com

# Check specific group
ansible-playbook compliance-check.yml --limit cisco_ios_switches

# Dry run (no actual connections)
ansible-playbook compliance-check.yml --check
```

#### Run Remediation
```bash
# Remediate with approval prompt
ansible-playbook remediation.yml

# Dry run remediation (show what would change)
ansible-playbook remediation.yml -e "remediation_mode=dry_run"

# Auto-remediate without approval (USE WITH CAUTION)
ansible-playbook remediation.yml -e "require_approval=false"

# Remediate specific device
ansible-playbook remediation.yml --limit router01.example.com
```

#### View Reports
```bash
# Open latest report
start reports/latest/inventory_report.html  # Windows
open reports/latest/inventory_report.html   # Mac
xdg-open reports/latest/inventory_report.html  # Linux

# List all reports
ls -lh reports/

# View specific device report
cat reports/latest/device_reports/switch01.example.com.json | jq .
```

### Scheduling

#### Setup Scheduled Checks
```bash
# Setup daily checks
./scripts/schedule_compliance_check.sh daily setup

# Setup weekly checks
./scripts/schedule_compliance_check.sh weekly setup

# Setup monthly checks
./scripts/schedule_compliance_check.sh monthly setup

# View cron jobs
crontab -l
```

#### Manual Scheduled Run
```bash
# Run as if it were a scheduled daily check
./scripts/schedule_compliance_check.sh daily run
```

### Maintenance

#### Update STIG Checklist
```bash
# Place new CKL file in current directory
cp /path/to/new_stig.ckl stig_checklists/current/

# Verify parsing
ansible-playbook compliance-check.yml --tags parse_stig --check
```

#### Cleanup Old Reports
```bash
# Cleanup daily reports older than 30 days
python scripts/cleanup_old_reports.py \
  --reports-dir reports \
  --schedule-type daily \
  --retention-days 30

# Cleanup all report types
python scripts/cleanup_old_reports.py --reports-dir reports
```

#### View Logs
```bash
# View Ansible log
tail -f logs/ansible.log

# View compliance check log
tail -f logs/compliance_checks.log

# View remediation log
tail -f logs/remediation.log

# View errors only
grep -i error logs/ansible.log
```

---

## Visual Workflows

### Compliance Check Workflow
```
┌─────────────────────────────────────────────────────────────┐
│ USER: ansible-playbook compliance-check.yml                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         v
        ┌────────────────────────────────┐
        │   1. Parse STIG Checklist      │
        │   (stig_parser role)           │
        │   - Read CKL XML file          │
        │   - Extract V-IDs & checks     │
        │   - Create requirements list   │
        └────────────┬───────────────────┘
                     │
                     v
        ┌────────────────────────────────┐
        │   2. Collect Device Configs    │
        │   (device_collector role)      │
        │   - Connect to devices         │
        │   - Get running-config         │
        │   - Execute show commands      │
        │   - Store configurations       │
        └────────────┬───────────────────┘
                     │
                     v
        ┌────────────────────────────────┐
        │   3. Execute Compliance Checks │
        │   (compliance_checker role)    │
        │   - Load STIG mappings         │
        │   - For each V-ID:             │
        │     • Apply check method       │
        │     • Evaluate result          │
        │     • Record finding           │
        │   - Calculate scores           │
        └────────────┬───────────────────┘
                     │
                     v
        ┌────────────────────────────────┐
        │   4. Generate Reports          │
        │   (report_generator role)      │
        │   - Aggregate all findings     │
        │   - Create device reports      │
        │   - Create inventory report    │
        │   - Generate HTML/JSON         │
        └────────────┬───────────────────┘
                     │
                     v
        ┌────────────────────────────────┐
        │   5. Send Notifications        │
        │   (notification role)          │
        │   - Email summary              │
        │   - POST to webhooks           │
        └────────────┬───────────────────┘
                     │
                     v
        ┌────────────────────────────────┐
        │   OUTPUT:                      │
        │   reports/{timestamp}/         │
        │   ├── device_reports/          │
        │   ├── inventory_report.html    │
        │   └── metadata.json            │
        └────────────────────────────────┘
```

### Remediation Workflow
```
┌─────────────────────────────────────────────────────────────┐
│ USER: ansible-playbook remediation.yml                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         v
        ┌────────────────────────────────┐
        │   1. Pre-Remediation Check     │
        │   - Run compliance check       │
        │   - Identify non-compliant     │
        │   - Filter remediable items    │
        └────────────┬───────────────────┘
                     │
                     v
        ┌────────────────────────────────┐
        │   2. Backup Configuration      │
        │   - Connect to device          │
        │   - Save running-config        │
        │   - Store: backups/{date}/     │
        │             pre_remediation/   │
        └────────────┬───────────────────┘
                     │
                     v
        ┌────────────────────────────────┐
        │   3. Generate Remediation Plan │
        │   - Map findings to fixes      │
        │   - Load config templates      │
        │   - Generate commands          │
        │   - Display plan to user       │
        └────────────┬───────────────────┘
                     │
                     v
        ┌────────────────────────────────┐
        │   4. Approval Gate             │
        │   [PAUSE] User reviews plan    │
        │   Proceed? (yes/no)            │
        └────────────┬───────────────────┘
                     │ yes
                     v
        ┌────────────────────────────────┐
        │   5. Apply Remediation         │
        │   - Apply config commands      │
        │   - Verify each change         │
        │   - Log all actions            │
        └────────────┬───────────────────┘
                     │
                     v
        ┌────────────────────────────────┐
        │   6. Post-Remediation Check    │
        │   - Run compliance check again │
        │   - Compare before/after       │
        │   - Verify improvements        │
        └────────────┬───────────────────┘
                     │
                     v
        ┌────────────────────────────────┐
        │   7. Generate Report           │
        │   - Show changes made          │
        │   - Display score improvement  │
        │   - List remaining issues      │
        └────────────────────────────────┘

        If any step fails:
        ┌────────────────────────────────┐
        │   ROLLBACK                     │
        │   - Restore backup config      │
        │   - Verify restoration         │
        │   - Report failure             │
        └────────────────────────────────┘
```

### Data Flow: STIG CKL to Device Check
```
STIG CKL File (XML)
│
├─ <VULN>
│  ├─ Vuln_Num: V-220518
│  ├─ Severity: medium
│  ├─ Rule_Title: "AAA must be configured"
│  ├─ Check_Content: "Verify aaa new-model..."
│  └─ Fix_Text: "Configure aaa new-model"
│
│  ckl_parser.py (library module)
│         ↓
│  Parsed STIG Data (YAML/JSON)
│         ↓
│
├─ stig_requirements:
│  ├─ vuln_id: V-220518
│  ├─ severity: CAT2
│  ├─ rule_title: "AAA must be configured"
│  ├─ check_content: "Verify aaa new-model..."
│  └─ fix_text: "Configure aaa new-model"
│
│  COMBINED WITH
│
├─ stig_mappings.yml
│  ├─ V-220518:
│  │  ├─ check_method: "config_contains"
│  │  ├─ required_config: ["aaa new-model"]
│  │  └─ applicable_platforms: ["ios"]
│
│         ↓
│  compliance_checker role
│         ↓
│
├─ Device Configuration
│  (from device_collector)
│  ├─ Running config text
│  └─ Show command output
│
│         ↓
│  Check Execution
│         ↓
│
├─ Finding Result
│  ├─ vuln_id: V-220518
│  ├─ status: "Open" or "NotAFinding"
│  ├─ finding_details: "AAA new-model: Not Found"
│  ├─ evidence: <config excerpt>
│  └─ check_date: "2026-01-09T10:30:00Z"
│
│         ↓
│  Report Generator
│         ↓
│
└─ HTML/JSON Report
   ├─ Compliance Score: 78%
   ├─ Open Findings: 15
   └─ Compliant: 53
```

---

## File Locations Reference

### Configuration Files
| File | Location | Purpose |
|------|----------|---------|
| Ansible Config | `ansible.cfg` | Ansible settings |
| Python Deps | `requirements.txt` | Python packages |
| Ansible Deps | `requirements.yml` | Ansible collections |
| Inventory | `inventory/production/hosts.yml` | Device list |
| Credentials | `inventory/production/group_vars/vault.yml` | Encrypted secrets |
| Variables | `inventory/production/group_vars/all.yml` | Global settings |

### STIG Files
| File Type | Location | Purpose |
|-----------|----------|---------|
| Current CKL | `stig_checklists/current/*.ckl` | Active STIG checklists |
| Archived CKL | `stig_checklists/archive/{date}/*.ckl` | Previous versions |
| Mappings | `roles/compliance_checker/vars/stig_mappings.yml` | V-ID to check mapping |

### Output Files
| File Type | Location | Purpose |
|-----------|----------|---------|
| Device Report | `reports/{timestamp}/device_reports/{hostname}.html` | Single device compliance |
| Inventory Report | `reports/{timestamp}/inventory_report.html` | All devices summary |
| Latest Report | `reports/latest/` | Symlink to most recent |
| Daily Reports | `reports/scheduled/daily/{date}/` | Scheduled daily runs |
| Backups | `backups/{date}/pre_remediation/{hostname}.cfg` | Config backups |
| Logs | `logs/ansible.log` | Execution logs |

### Custom Code
| File Type | Location | Purpose |
|-----------|----------|---------|
| Custom Modules | `library/*.py` | Ansible modules |
| Filters | `filter_plugins/*.py` | Jinja2 filters |
| Scripts | `scripts/*.sh` or `*.py` | Utility scripts |
| Templates | `roles/*/templates/*.j2` | Jinja2 templates |

---

## Common Variables Reference

### Playbook Variables
```yaml
# Set in playbook or command line with -e

compliance_mode: "check_only"  # or "remediate"
remediation_mode: "auto"       # auto, interactive, dry_run
require_approval: true         # Prompt before remediation
backup_enabled: true           # Backup before changes
notification_enabled: true     # Send notifications

stig_version: "Cisco_IOS_Switch_L2S_V2R8_STIG"
report_timestamp: "2026-01-09_10-30-00"
report_dir: "reports/2026-01-09_10-30-00"
```

### Group Variables
```yaml
# Set in inventory/production/group_vars/all.yml

stig_checklists_dir: "E:/01- Chrome Downloads/cisco-stig-compliance/stig_checklists"
reports_dir: "E:/01- Chrome Downloads/cisco-stig-compliance/reports"
backups_dir: "E:/01- Chrome Downloads/cisco-stig-compliance/backups"

report_formats: [html, json]
backup_retention_days: 30
```

### Device Variables
```yaml
# Set in inventory per device

ansible_host: "10.1.1.10"       # Device IP
device_type: "cisco_ios"         # Device OS type
device_role: "access_switch"     # Device role
site: "headquarters"             # Site location
```

---

## Check Methods Reference

### Available Check Methods

| Method | Description | Example Use Case |
|--------|-------------|------------------|
| `config_contains` | Exact string match | Check if "aaa new-model" exists |
| `config_regex` | Regex pattern match | Match "aaa authentication login default group \S+" |
| `config_value_comparison` | Compare numeric values | Password length >= 15 |
| `banner_check` | Validate banner content | Login banner contains required text |
| `show_command` | Execute show command | Check "show users" output |
| `multi_line_block` | Check config blocks | Verify interface configuration |
| `negative_check` | Ensure NOT present | "no ip http server" must exist |
| `custom_script` | Custom Python logic | Complex validation |

### Example Check Mapping

```yaml
V-220518:
  name: "AAA new-model required"
  applicable_platforms: ["ios", "ios-xe"]
  check_method: "config_contains"
  config_section: "aaa"
  required_config:
    - "aaa new-model"
  severity: "CAT2"
  enabled: true
```

---

## Troubleshooting Quick Reference

### Issue: Cannot connect to devices

**Check:**
```bash
# Test connectivity
ansible all -i inventory/production/hosts.yml -m ping

# Verify credentials
ansible all -i inventory/production/hosts.yml -m cisco.ios.ios_command -a "commands='show version'"

# Check inventory
ansible-inventory -i inventory/production/hosts.yml --list
```

**Common Fixes:**
- Verify device IP addresses in `inventory/production/hosts.yml`
- Check credentials in `inventory/production/group_vars/vault.yml`
- Ensure SSH access enabled on devices
- Check firewall rules

### Issue: CKL parsing fails

**Check:**
```bash
# Validate XML
xmllint --noout stig_checklists/current/*.ckl

# Test parser manually
python library/ckl_parser.py stig_checklists/current/your_stig.ckl
```

**Common Fixes:**
- Ensure CKL file is valid XML
- Check file encoding (should be UTF-8)
- Verify CKL file format matches expected structure

### Issue: Reports not generated

**Check:**
```bash
# Verify report directory exists
ls -la reports/

# Check permissions
chmod -R 755 reports/

# Test report generation manually
ansible-playbook report-generation.yml -vvv
```

**Common Fixes:**
- Create reports directory: `mkdir -p reports`
- Fix permissions: `chmod -R 755 reports/`
- Install Jinja2: `pip install jinja2`

### Issue: Scheduled jobs not running

**Check:**
```bash
# View cron jobs
crontab -l

# Check cron log
grep CRON /var/log/syslog  # Linux
tail -f logs/scheduled_runs.log

# Test manual run
./scripts/schedule_compliance_check.sh daily run
```

**Common Fixes:**
- Verify cron job exists: `crontab -l`
- Check script permissions: `chmod +x scripts/*.sh`
- Verify paths in cron job are absolute

---

## Performance Tuning

### Optimize for Large Inventories (100+ devices)

```yaml
# In ansible.cfg
[defaults]
forks = 50  # Increase parallel execution
timeout = 120  # Increase timeout
pipelining = True  # Reduce SSH overhead
fact_caching = jsonfile  # Cache facts
```

### Optimize for Slow Networks

```yaml
# In ansible.cfg
[defaults]
timeout = 300  # 5 minutes
forks = 5  # Reduce parallel connections

[persistent_connection]
connect_timeout = 120
command_timeout = 120
```

### Reduce Memory Usage

```yaml
# Run checks in batches
ansible-playbook compliance-check.yml --limit "cisco_ios_switches[0:10]"
ansible-playbook compliance-check.yml --limit "cisco_ios_switches[11:20]"
```

---

## Security Best Practices

### Credential Management
```bash
# Create encrypted vault
ansible-vault create inventory/production/group_vars/vault.yml

# Edit vault
ansible-vault edit inventory/production/group_vars/vault.yml

# Run playbook with vault
ansible-playbook compliance-check.yml --ask-vault-pass

# Use vault password file
echo "your_vault_password" > .vault_pass
chmod 600 .vault_pass
ansible-playbook compliance-check.yml --vault-password-file .vault_pass
```

### Access Control
```bash
# Restrict file permissions
chmod 600 inventory/production/group_vars/vault.yml
chmod 700 scripts/
chmod 755 reports/
chmod 755 backups/
```

### Audit Trail
```bash
# All actions logged to:
logs/ansible.log          # General Ansible log
logs/compliance_checks.log  # Compliance checks
logs/remediation.log       # Remediation actions
logs/scheduled_runs.log    # Scheduled execution
```

---

## Useful Commands Cheat Sheet

### Ansible Commands
```bash
# List inventory
ansible-inventory -i inventory/production/hosts.yml --graph

# Test connectivity
ansible all -i inventory/production/hosts.yml -m ping

# Run ad-hoc command
ansible all -i inventory/production/hosts.yml -m cisco.ios.ios_command -a "commands='show version'"

# Syntax check
ansible-playbook compliance-check.yml --syntax-check

# Dry run
ansible-playbook compliance-check.yml --check

# Verbose output
ansible-playbook compliance-check.yml -vvv

# Step through playbook
ansible-playbook compliance-check.yml --step

# Start at specific task
ansible-playbook compliance-check.yml --start-at-task="Execute compliance checks"
```

### Report Commands
```bash
# View latest report
cat reports/latest/inventory_report.json | jq .

# Count findings by severity
jq '[.findings[] | select(.severity == "CAT1")] | length' reports/latest/device_reports/*.json

# List non-compliant devices
jq -r 'select(.compliance_score < 90) | .device' reports/latest/device_reports/*.json

# Export to CSV
python scripts/export_to_csv.py --report reports/latest/inventory_report.json --output compliance.csv
```

### Maintenance Commands
```bash
# Cleanup reports older than 30 days
python scripts/cleanup_old_reports.py --reports-dir reports --schedule-type daily --retention-days 30

# Archive logs
tar -czf logs/archive/$(date +%Y-%m).tar.gz logs/*.log

# Backup project
./scripts/backup_project.sh

# Update dependencies
pip install --upgrade -r requirements.txt
ansible-galaxy collection install -r requirements.yml --upgrade
```

---

## Exit Codes

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success - all checks passed |
| 1 | Failure - general error |
| 2 | Host unreachable |
| 3 | Host failed compliance |
| 4 | Syntax error in playbook |
| 99 | Interrupted by user |

---

## Support and Resources

### Documentation
- Architecture: `ARCHITECTURE.md`
- Project Structure: `PROJECT_STRUCTURE.md`
- Implementation Guide: `IMPLEMENTATION_GUIDE.md`
- Usage Guide: `docs/USAGE.md`
- Troubleshooting: `docs/TROUBLESHOOTING.md`

### Logs
- Ansible: `logs/ansible.log`
- Compliance: `logs/compliance_checks.log`
- Remediation: `logs/remediation.log`
- Scheduled: `logs/scheduled_runs.log`

### External Resources
- STIG Downloads: https://public.cyber.mil/stigs/
- Ansible Docs: https://docs.ansible.com/
- Cisco IOS Module: https://docs.ansible.com/ansible/latest/collections/cisco/ios/

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-09 | Initial architecture |

---

**Quick Tip**: Bookmark this file for daily reference!

**Project Location**: E:\01- Chrome Downloads\cisco-stig-compliance
