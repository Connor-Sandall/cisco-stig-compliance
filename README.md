# Cisco STIG Compliance Checker

Automated Security Technical Implementation Guide (STIG) compliance checking and remediation for Cisco network devices using Ansible.

## Overview

This project provides a comprehensive, automated solution for:
- Parsing DISA STIG checklist (.ckl) files
- Checking Cisco devices (IOS, IOS-XE, NX-OS) for STIG compliance
- Generating professional HTML and JSON reports
- Optionally remediating non-compliant configurations
- Scheduling automated compliance scans
- Maintaining historical compliance data

## Key Features

- **Reusable STIG Parser** - Simply drop new .ckl files when DISA releases updates
- **Dual Operating Modes** - Compliance-only (read-only) or remediation (with safety mechanisms)
- **Comprehensive Reporting** - Device-level, inventory-wide, and executive summaries
- **Safety First** - Automatic backups, approval gates, dry-run mode, and rollback on failure
- **Scheduling Built-in** - Daily, weekly, or monthly automated scans with organized storage
- **Full Audit Trail** - Complete logs of all checks and changes

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Ansible 2.15 or higher
- SSH access to Cisco devices
- STIG checklist files (.ckl format) from [cyber.mil](https://public.cyber.mil/stigs/)

### Installation

```bash
# Clone or download this project
cd "E:\01- Chrome Downloads\cisco-stig-compliance"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
ansible-galaxy collection install -r requirements.yml
```

### Configuration

1. **Add your devices** to inventory:
   ```bash
   notepad inventory/production/hosts.yml
   ```

2. **Configure credentials** (encrypted):
   ```bash
   ansible-vault create inventory/production/group_vars/vault.yml
   ```
   Add:
   ```yaml
   vault_ansible_user: "admin"
   vault_ansible_password: "YourPassword"
   vault_enable_password: "YourEnablePassword"
   ```

3. **Add STIG checklists**:
   - Download .ckl files from [cyber.mil](https://public.cyber.mil/stigs/)
   - Place in `stig_checklists/current/`

### Basic Usage

```bash
# Run compliance check
ansible-playbook compliance-check.yml --ask-vault-pass

# View report
start reports/latest/inventory_report.html  # Windows
open reports/latest/inventory_report.html   # Mac

# Run remediation (with approval prompt)
ansible-playbook remediation.yml --ask-vault-pass

# Check specific device
ansible-playbook compliance-check.yml --limit switch01.example.com --ask-vault-pass

# Dry run (preview what would change)
ansible-playbook remediation.yml -e "remediation_mode=dry_run" --ask-vault-pass
```

## Documentation

### Architecture & Design
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Detailed technical architecture, role definitions, and implementation details
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Complete directory structure with all files and their purposes
- **[DIAGRAMS.md](DIAGRAMS.md)** - Visual workflow diagrams and system architecture illustrations

### Implementation & Operations
- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)** - Step-by-step implementation instructions (6-week timeline)
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Daily operations command reference and troubleshooting
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Executive overview and high-level summary

### Detailed Guides
- **[docs/USAGE.md](docs/USAGE.md)** - Comprehensive usage guide (to be created)
- **[docs/STIG_MAPPING.md](docs/STIG_MAPPING.md)** - STIG check mapping reference (to be created)
- **[docs/REMEDIATION_GUIDE.md](docs/REMEDIATION_GUIDE.md)** - Remediation procedures (to be created)
- **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Common issues and solutions (to be created)

## Project Structure

```
cisco-stig-compliance/
├── README.md                          This file
├── ARCHITECTURE.md                    Detailed architecture
├── PROJECT_STRUCTURE.md               Complete directory structure
├── IMPLEMENTATION_GUIDE.md            Implementation instructions
├── QUICK_REFERENCE.md                 Command reference
├── PROJECT_SUMMARY.md                 Executive overview
├── DIAGRAMS.md                        Visual diagrams
│
├── ansible.cfg                        Ansible configuration
├── requirements.txt                   Python dependencies
├── requirements.yml                   Ansible Galaxy dependencies
│
├── compliance-check.yml               Main compliance check playbook
├── remediation.yml                    Remediation playbook
├── report-generation.yml              Report generation playbook
│
├── inventory/                         Device inventories
├── roles/                             Ansible roles (core logic)
├── library/                           Custom Ansible modules
├── filter_plugins/                    Custom Jinja2 filters
├── stig_checklists/                   STIG .ckl files (user-managed)
├── config_templates/                  Remediation templates
├── scripts/                           Utility scripts
├── tests/                             Test suite
├── docs/                              Additional documentation
│
├── reports/                           Generated reports (not in git)
├── backups/                           Config backups (not in git)
└── logs/                              Execution logs (not in git)
```

## How It Works

### 1. STIG Parsing
- Reads XML-formatted CKL files from `stig_checklists/current/`
- Extracts vulnerability IDs (V-IDs), rules, and check procedures
- No code changes needed when STIG updates - just replace the .ckl file

### 2. Compliance Checking
- Connects to devices via SSH using Ansible
- Collects running configurations and executes show commands
- Evaluates each STIG requirement against device configuration
- Records findings: Compliant, Non-Compliant, or Not Applicable

### 3. Report Generation
- **Device Reports**: Individual compliance report per device (HTML + JSON)
- **Inventory Report**: All devices summarized in one report
- **Executive Summary**: High-level metrics for management
- Reports stored in timestamped directories

### 4. Remediation (Optional)
- Identifies non-compliant configurations
- Generates remediation commands from templates
- Backs up configuration before changes
- Applies fixes with verification
- Automatically rolls back on failure

### 5. Scheduling
- Automated daily, weekly, or monthly scans
- Reports organized by schedule type
- Automatic cleanup of old reports
- Email and webhook notifications

## Example Workflows

### Daily Operations

**Check compliance across all devices:**
```bash
ansible-playbook compliance-check.yml --ask-vault-pass
```

**View latest report:**
```bash
start reports/latest/inventory_report.html
```

**Fix critical issues on specific device:**
```bash
ansible-playbook remediation.yml --limit router01.example.com --ask-vault-pass
```

### Scheduled Operations

**Setup daily automated checks:**
```bash
./scripts/schedule_compliance_check.sh daily setup
```

**View scheduled reports:**
```bash
start reports/scheduled/daily/latest/inventory_report.html
```

### STIG Updates

**When DISA releases new STIG version:**
```bash
# 1. Download new .ckl file from cyber.mil
# 2. Copy to project
cp ~/Downloads/Cisco_IOS_Switch_L2S_V2R9_STIG.ckl stig_checklists/current/

# 3. Old version automatically archived
# 4. Run compliance check with new STIG
ansible-playbook compliance-check.yml \
  -e "stig_version=Cisco_IOS_Switch_L2S_V2R9_STIG" \
  --ask-vault-pass
```

## Supported Devices

### Currently Supported
- Cisco IOS Switches (Layer 2 Switch STIG)
- Cisco IOS Routers (Router STIG)
- Cisco IOS-XE Switches
- Cisco NX-OS Switches

### Easy to Extend
The architecture supports adding new device types by:
1. Adding device group to inventory
2. Creating collection tasks for the device type
3. Adding check mappings for device-specific STIGs

## Report Examples

### Device Report
Shows compliance status for a single device:
- Overall compliance score (percentage)
- Findings by severity (CAT I, CAT II, CAT III)
- Detailed finding information with evidence
- Remediation recommendations

### Inventory Report
Shows compliance across all devices:
- Compliance score per device
- Aggregate statistics
- Top vulnerabilities across inventory
- Devices requiring attention

### Executive Summary
High-level overview for management:
- Overall compliance percentage
- Risk assessment
- Critical findings requiring immediate action
- Compliance trends over time

## Security Considerations

### Credential Management
- All credentials stored in Ansible Vault (encrypted)
- Vault password not stored in repository
- Support for separate vault files per environment
- Service accounts with minimal required permissions

### Access Control
- Reports directory protected (contains sensitive data)
- Backups protected (contain full device configurations)
- Complete audit trail for all actions
- Optional approval gates for production remediation

### Network Security
- SSH key authentication supported
- All connections encrypted
- Jump host support for isolated networks
- No credentials in logs or reports

## Performance

### Small Environment (10-50 devices)
- Compliance check: 5-10 minutes
- Storage: ~500 MB/month with daily checks
- Configuration: Default settings

### Medium Environment (50-200 devices)
- Compliance check: 15-30 minutes
- Storage: ~2 GB/month with daily checks
- Configuration: Increase forks to 20-30

### Large Environment (200+ devices)
- Compliance check: 30-60 minutes
- Storage: ~5 GB/month with daily checks
- Configuration: Increase forks to 50+, consider batching

## Troubleshooting

### Cannot connect to devices
```bash
# Test connectivity
ansible all -i inventory/production/hosts.yml -m ping --ask-vault-pass

# Verify credentials
ansible all -i inventory/production/hosts.yml \
  -m cisco.ios.ios_command \
  -a "commands='show version'" \
  --ask-vault-pass
```

### CKL parsing fails
```bash
# Validate XML
xmllint --noout stig_checklists/current/*.ckl

# Test parser
python library/ckl_parser.py stig_checklists/current/your_stig.ckl
```

### Reports not generated
```bash
# Check permissions
chmod -R 755 reports/

# Test report generation
ansible-playbook report-generation.yml -vvv --ask-vault-pass
```

For more troubleshooting, see [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

## Maintenance

### Regular Tasks
- **Weekly**: Review compliance reports
- **Monthly**: Cleanup old reports and logs
- **Quarterly**: Update STIG checklists (as DISA releases them)
- **Quarterly**: Update Python and Ansible dependencies

### Cleanup Commands
```bash
# Remove old reports (keep last 30 days)
python scripts/cleanup_old_reports.py \
  --reports-dir reports \
  --schedule-type daily \
  --retention-days 30

# Archive logs
tar -czf logs/archive/$(date +%Y-%m).tar.gz logs/*.log

# Update dependencies
pip install --upgrade -r requirements.txt
ansible-galaxy collection install -r requirements.yml --upgrade
```

## Contributing

This project follows standard Ansible best practices:
- Use roles for logical separation
- Keep secrets in Vault
- Document all custom modules
- Test changes in development environment first
- Update STIG mappings when checks change

## Resources

### STIG Resources
- **DISA STIG Library**: https://public.cyber.mil/stigs/
- **STIG Viewer Tool**: https://public.cyber.mil/stigs/srg-stig-tools/

### Ansible Resources
- **Ansible Documentation**: https://docs.ansible.com/
- **Cisco IOS Module**: https://docs.ansible.com/ansible/latest/collections/cisco/ios/
- **Cisco NX-OS Module**: https://docs.ansible.com/ansible/latest/collections/cisco/nxos/

### Project Documentation
Start with these documents in order:
1. **PROJECT_SUMMARY.md** - High-level overview
2. **ARCHITECTURE.md** - Detailed design
3. **IMPLEMENTATION_GUIDE.md** - Step-by-step setup
4. **QUICK_REFERENCE.md** - Daily operations

## Support

### Documentation
- Check the `docs/` directory for detailed guides
- Review `logs/` for execution details
- Consult STIG resources at cyber.mil

### Common Issues
See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for troubleshooting tips

## License

[Add your license here]

## Authors

DevOps Engineering Team

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-09 | Initial architecture and implementation |

---

## Quick Links

- [Architecture Details](ARCHITECTURE.md)
- [Complete File Structure](PROJECT_STRUCTURE.md)
- [Implementation Guide](IMPLEMENTATION_GUIDE.md)
- [Command Reference](QUICK_REFERENCE.md)
- [Visual Diagrams](DIAGRAMS.md)
- [Project Summary](PROJECT_SUMMARY.md)

---

**Project Location**: `E:\01- Chrome Downloads\cisco-stig-compliance`

**Contact**: [Add contact information]

**Last Updated**: 2026-01-09
