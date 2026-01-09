# Cisco STIG Compliance Checker - Complete Project Structure

## Directory Tree with File Counts and Purposes

```
cisco-stig-compliance/                                    [ROOT]
│
├── README.md                                            [Project overview and quick start]
├── ARCHITECTURE.md                                       [Detailed architecture documentation]
├── PROJECT_STRUCTURE.md                                  [This file - complete structure]
├── LICENSE                                              [Project license]
├── .gitignore                                           [Git ignore patterns]
├── requirements.txt                                      [Python dependencies]
├── requirements.yml                                      [Ansible Galaxy dependencies]
├── ansible.cfg                                          [Ansible configuration]
│
├── playbooks/                                           [Main orchestration playbooks]
│   ├── site.yml                                         [Main entry point]
│   ├── compliance-check.yml                             [Compliance checking workflow]
│   ├── remediation.yml                                  [Remediation workflow]
│   ├── report-generation.yml                            [Report generation only]
│   └── test-notification.yml                            [Test notification setup]
│
├── inventory/                                           [Device inventory management - 15-20 files]
│   │
│   ├── production/                                      [Production environment]
│   │   ├── hosts.yml                                   [Production device inventory]
│   │   └── group_vars/
│   │       ├── all.yml                                 [Global variables for all devices]
│   │       ├── cisco_ios.yml                           [IOS-specific variables]
│   │       ├── cisco_ios_switches.yml                  [IOS switches variables]
│   │       ├── cisco_ios_routers.yml                   [IOS routers variables]
│   │       ├── cisco_nxos.yml                          [NX-OS-specific variables]
│   │       └── vault.yml                               [Encrypted credentials - ANSIBLE VAULT]
│   │
│   ├── staging/                                         [Staging environment]
│   │   ├── hosts.yml
│   │   └── group_vars/
│   │       ├── all.yml
│   │       ├── cisco_ios.yml
│   │       ├── cisco_nxos.yml
│   │       └── vault.yml
│   │
│   ├── development/                                     [Development/lab environment]
│   │   ├── hosts.yml
│   │   └── group_vars/
│   │       ├── all.yml
│   │       └── vault.yml
│   │
│   └── README.md                                        [Inventory documentation]
│
├── roles/                                               [Ansible roles - 6 main roles, ~60-80 files total]
│   │
│   ├── stig_parser/                                     [Parse STIG CKL files - ~12 files]
│   │   ├── defaults/
│   │   │   └── main.yml                                [Default variables]
│   │   ├── files/
│   │   │   └── schema_validator.py                    [CKL XML schema validator]
│   │   ├── tasks/
│   │   │   ├── main.yml                                [Main task entry point]
│   │   │   ├── parse_ckl.yml                           [Parse CKL XML structure]
│   │   │   ├── extract_checks.yml                      [Extract check requirements]
│   │   │   ├── validate_checklist.yml                  [Validate CKL integrity]
│   │   │   └── cache_parsed_data.yml                   [Cache parsing results]
│   │   ├── templates/
│   │   │   └── parsed_stig_output.j2                   [Template for parsed output]
│   │   ├── vars/
│   │   │   ├── main.yml                                [Role variables]
│   │   │   └── ckl_xpath_mappings.yml                  [XML XPath mappings]
│   │   ├── meta/
│   │   │   └── main.yml                                [Role metadata and dependencies]
│   │   └── README.md                                    [Role documentation]
│   │
│   ├── device_collector/                                [Collect device configs - ~15 files]
│   │   ├── defaults/
│   │   │   └── main.yml
│   │   ├── handlers/
│   │   │   └── main.yml                                [Event handlers]
│   │   ├── tasks/
│   │   │   ├── main.yml
│   │   │   ├── ios_collect.yml                         [Collect from IOS devices]
│   │   │   ├── ios_show_commands.yml                   [Execute IOS show commands]
│   │   │   ├── nxos_collect.yml                        [Collect from NX-OS devices]
│   │   │   ├── nxos_show_commands.yml                  [Execute NX-OS show commands]
│   │   │   ├── backup_config.yml                       [Backup configurations]
│   │   │   ├── parse_config.yml                        [Parse collected configs]
│   │   │   └── error_handling.yml                      [Handle collection errors]
│   │   ├── templates/
│   │   │   ├── show_commands_ios.j2                    [IOS show command list]
│   │   │   └── show_commands_nxos.j2                   [NX-OS show command list]
│   │   ├── vars/
│   │   │   └── main.yml
│   │   └── README.md
│   │
│   ├── compliance_checker/                              [Execute compliance checks - ~25 files]
│   │   ├── defaults/
│   │   │   └── main.yml
│   │   ├── tasks/
│   │   │   ├── main.yml
│   │   │   ├── check_ios.yml                           [IOS compliance checks]
│   │   │   ├── check_nxos.yml                          [NX-OS compliance checks]
│   │   │   ├── execute_single_check.yml                [Execute individual check]
│   │   │   ├── evaluate_findings.yml                   [Evaluate check results]
│   │   │   ├── calculate_scores.yml                    [Calculate compliance scores]
│   │   │   └── checks/                                 [Check method implementations]
│   │   │       ├── config_contains.yml                 [Exact string match check]
│   │   │       ├── config_regex.yml                    [Regex pattern check]
│   │   │       ├── config_value_comparison.yml         [Numeric value comparison]
│   │   │       ├── banner_check.yml                    [Banner content check]
│   │   │       ├── show_command.yml                    [Show command output check]
│   │   │       ├── multi_line_block.yml                [Multi-line config block check]
│   │   │       ├── negative_check.yml                  [Ensure config NOT present]
│   │   │       └── custom_script.yml                   [Custom Python check]
│   │   ├── vars/
│   │   │   ├── main.yml
│   │   │   ├── stig_mappings.yml                       [STIG V-ID to check mappings]
│   │   │   ├── ios_check_library.yml                   [IOS check definitions]
│   │   │   └── nxos_check_library.yml                  [NX-OS check definitions]
│   │   ├── filter_plugins/
│   │   │   └── compliance_filters.py                   [Custom Jinja2 filters]
│   │   └── README.md
│   │
│   ├── remediation_engine/                              [Apply remediation - ~18 files]
│   │   ├── defaults/
│   │   │   └── main.yml
│   │   ├── handlers/
│   │   │   └── main.yml
│   │   ├── tasks/
│   │   │   ├── main.yml
│   │   │   ├── generate_plan.yml                       [Generate remediation plan]
│   │   │   ├── pre_remediation_checks.yml              [Validate before remediation]
│   │   │   ├── apply_ios_fixes.yml                     [Apply IOS remediation]
│   │   │   ├── apply_nxos_fixes.yml                    [Apply NX-OS remediation]
│   │   │   ├── verify_changes.yml                      [Verify successful changes]
│   │   │   ├── rollback.yml                            [Rollback on failure]
│   │   │   └── post_remediation_verify.yml             [Post-remediation verification]
│   │   ├── templates/
│   │   │   ├── ios_remediation.j2                      [IOS remediation config template]
│   │   │   ├── nxos_remediation.j2                     [NX-OS remediation config template]
│   │   │   ├── remediation_plan.j2                     [Remediation plan format]
│   │   │   └── rollback_config.j2                      [Rollback config template]
│   │   ├── vars/
│   │   │   ├── main.yml
│   │   │   ├── remediation_mappings.yml                [V-ID to remediation mappings]
│   │   │   └── safety_checks.yml                       [Safety validation rules]
│   │   └── README.md
│   │
│   ├── report_generator/                                [Generate reports - ~15 files]
│   │   ├── defaults/
│   │   │   └── main.yml
│   │   ├── tasks/
│   │   │   ├── main.yml
│   │   │   ├── prepare_data.yml                        [Aggregate and format data]
│   │   │   ├── generate_device_report.yml              [Individual device report]
│   │   │   ├── generate_inventory_report.yml           [Full inventory report]
│   │   │   ├── generate_executive_summary.yml          [Executive summary]
│   │   │   ├── generate_comparison_report.yml          [Compare two reports]
│   │   │   └── export_formats.yml                      [Export to various formats]
│   │   ├── templates/
│   │   │   ├── device_report.html.j2                   [Device HTML report]
│   │   │   ├── device_report.json.j2                   [Device JSON report]
│   │   │   ├── inventory_report.html.j2                [Inventory HTML report]
│   │   │   ├── executive_summary.html.j2               [Executive summary HTML]
│   │   │   ├── compliance_dashboard.html.j2            [Interactive dashboard]
│   │   │   ├── email_report.html.j2                    [Email-friendly report]
│   │   │   └── styles/                                 [CSS styles]
│   │   │       ├── report.css                          [Main report styles]
│   │   │       └── dashboard.css                       [Dashboard styles]
│   │   ├── files/
│   │   │   ├── chart_generator.py                      [Generate charts/graphs]
│   │   │   └── pdf_converter.py                        [Convert HTML to PDF]
│   │   └── README.md
│   │
│   └── notification/                                    [Send notifications - ~10 files]
│       ├── defaults/
│       │   └── main.yml
│       ├── tasks/
│       │   ├── main.yml
│       │   ├── email_notification.yml                   [Send email notifications]
│       │   ├── webhook_notification.yml                 [POST to webhooks]
│       │   ├── slack_notification.yml                   [Slack-specific formatting]
│       │   └── teams_notification.yml                   [MS Teams-specific formatting]
│       ├── templates/
│       │   ├── email_template.j2                        [Email message template]
│       │   ├── slack_message.j2                         [Slack message format]
│       │   └── teams_message.j2                         [Teams message format]
│       ├── vars/
│       │   └── main.yml
│       └── README.md
│
├── library/                                             [Custom Ansible modules - ~8 files]
│   ├── __init__.py
│   ├── ckl_parser.py                                    [Parse CKL XML files]
│   ├── cisco_config_parser.py                           [Parse Cisco configurations]
│   ├── stig_compliance_checker.py                       [STIG compliance evaluation]
│   ├── config_differ.py                                 [Compare configurations]
│   ├── finding_evaluator.py                             [Evaluate findings]
│   ├── report_aggregator.py                             [Aggregate report data]
│   ├── test_ckl_parser.py                               [Unit tests for parser]
│   └── README.md
│
├── filter_plugins/                                      [Custom Jinja2 filters - ~5 files]
│   ├── __init__.py
│   ├── stig_filters.py                                  [STIG-specific filters]
│   ├── cisco_filters.py                                 [Cisco config parsing filters]
│   ├── report_filters.py                                [Report formatting filters]
│   └── date_filters.py                                  [Date/time formatting]
│
├── stig_checklists/                                     [STIG checklist files - managed by user]
│   │
│   ├── current/                                         [Current active checklists]
│   │   ├── Cisco_IOS_Switch_L2S_V2R8_STIG.ckl          [Layer 2 Switch STIG]
│   │   ├── Cisco_IOS_Router_RTR_V2R8_STIG.ckl          [Router STIG]
│   │   ├── Cisco_IOS_XE_Switch_L2S_V2R4_STIG.ckl       [IOS-XE Switch STIG]
│   │   └── Cisco_NX-OS_Switch_V2R4_STIG.ckl            [NX-OS Switch STIG]
│   │
│   ├── archive/                                         [Previous versions]
│   │   ├── 2025-12-15/                                 [Archived by date]
│   │   │   ├── Cisco_IOS_Switch_L2S_V2R7_STIG.ckl
│   │   │   └── Cisco_IOS_Router_RTR_V2R7_STIG.ckl
│   │   └── 2025-11-01/
│   │       └── Cisco_IOS_Switch_L2S_V2R6_STIG.ckl
│   │
│   ├── metadata/                                        [Checklist metadata]
│   │   ├── current_versions.yml                        [Track current versions]
│   │   └── changelog.md                                [Changelog for updates]
│   │
│   └── README.md                                        [Instructions for updating]
│
├── config_templates/                                    [Device configuration templates - ~20 files]
│   │
│   ├── ios/                                            [IOS templates]
│   │   ├── aaa/
│   │   │   ├── aaa_authentication.j2                   [AAA authentication config]
│   │   │   ├── aaa_authorization.j2                    [AAA authorization config]
│   │   │   └── aaa_accounting.j2                       [AAA accounting config]
│   │   ├── banner/
│   │   │   ├── banner_login.j2                         [Login banner]
│   │   │   ├── banner_motd.j2                          [MOTD banner]
│   │   │   └── banner_exec.j2                          [Exec banner]
│   │   ├── logging/
│   │   │   ├── logging_host.j2                         [Syslog server config]
│   │   │   └── logging_buffered.j2                     [Local logging config]
│   │   ├── snmp/
│   │   │   ├── snmp_v3.j2                              [SNMPv3 config]
│   │   │   └── snmp_acl.j2                             [SNMP ACL config]
│   │   ├── security/
│   │   │   ├── password_policy.j2                      [Password policy]
│   │   │   ├── service_config.j2                       [Service security]
│   │   │   └── timeout_config.j2                       [Timeout settings]
│   │   └── ntp/
│   │       └── ntp_config.j2                           [NTP configuration]
│   │
│   └── nxos/                                           [NX-OS templates]
│       ├── aaa/
│       │   ├── aaa_authentication.j2
│       │   └── aaa_authorization.j2
│       ├── banner/
│       │   └── banner_motd.j2
│       └── logging/
│           └── logging_host.j2
│
├── reports/                                             [Generated compliance reports - grows over time]
│   │
│   ├── 2026-01-09_10-30-00/                           [Timestamped report directory]
│   │   ├── device_reports/                            [Individual device reports]
│   │   │   ├── switch01.example.com.html
│   │   │   ├── switch01.example.com.json
│   │   │   ├── switch02.example.com.html
│   │   │   ├── switch02.example.com.json
│   │   │   ├── router01.example.com.html
│   │   │   └── router01.example.com.json
│   │   ├── inventory_report.html                      [Combined inventory report]
│   │   ├── inventory_report.json                      [Machine-readable inventory]
│   │   ├── executive_summary.html                     [Executive summary]
│   │   ├── compliance_dashboard.html                  [Interactive dashboard]
│   │   ├── metadata.json                              [Run metadata]
│   │   └── artifacts/                                 [Supporting files]
│   │       ├── device_configs/                        [Collected configurations]
│   │       ├── raw_findings/                          [Raw finding data]
│   │       └── charts/                                [Chart images]
│   │
│   ├── 2026-01-08_10-30-00/                           [Previous run]
│   ├── 2026-01-07_10-30-00/
│   │
│   ├── latest/                                         [Symlink to most recent report]
│   │
│   └── scheduled/                                      [Organized scheduled reports]
│       ├── daily/
│       │   ├── latest -> 2026-01-09/
│       │   ├── 2026-01-09/
│       │   ├── 2026-01-08/
│       │   └── 2026-01-07/
│       ├── weekly/
│       │   ├── latest -> 2026-W02/
│       │   ├── 2026-W02/
│       │   └── 2026-W01/
│       └── monthly/
│           ├── latest -> 2026-01/
│           ├── 2026-01/
│           └── 2025-12/
│
├── backups/                                             [Device configuration backups - grows over time]
│   ├── 2026-01-09/                                     [Daily backup directory]
│   │   ├── pre_remediation/                           [Before remediation]
│   │   │   ├── switch01.example.com.cfg
│   │   │   ├── switch02.example.com.cfg
│   │   │   └── router01.example.com.cfg
│   │   └── post_remediation/                          [After remediation]
│   │       ├── switch01.example.com.cfg
│   │       └── router01.example.com.cfg
│   ├── 2026-01-08/
│   └── latest/                                         [Symlink to most recent]
│
├── logs/                                                [Execution logs - ~5 main log files]
│   ├── ansible.log                                     [Main Ansible execution log]
│   ├── compliance_checks.log                           [Compliance checking log]
│   ├── remediation.log                                 [Remediation actions log]
│   ├── scheduled_runs.log                              [Scheduled execution log]
│   ├── errors.log                                      [Error log]
│   └── archive/                                        [Archived logs]
│       ├── 2026-01/
│       └── 2025-12/
│
├── scripts/                                             [Utility scripts - ~10 files]
│   ├── schedule_compliance_check.sh                    [Setup/run scheduled checks]
│   ├── compare_reports.py                              [Compare two compliance reports]
│   ├── update_stig_checklist.sh                        [Update STIG checklist workflow]
│   ├── validate_inventory.py                           [Validate inventory file]
│   ├── cleanup_old_reports.py                          [Cleanup old reports]
│   ├── export_to_csv.py                                [Export report data to CSV]
│   ├── generate_metrics.py                             [Generate compliance metrics]
│   ├── test_connectivity.sh                            [Test device connectivity]
│   ├── backup_project.sh                               [Backup entire project]
│   └── README.md
│
├── tests/                                               [Test suite - ~15-20 files]
│   ├── unit/                                           [Unit tests]
│   │   ├── __init__.py
│   │   ├── test_ckl_parser.py                         [Test CKL parser]
│   │   ├── test_cisco_config_parser.py                [Test config parser]
│   │   ├── test_compliance_checker.py                 [Test compliance logic]
│   │   └── test_report_generator.py                   [Test report generation]
│   │
│   ├── integration/                                    [Integration tests]
│   │   ├── test_compliance_check.yml                  [Test full compliance check]
│   │   ├── test_remediation.yml                       [Test remediation workflow]
│   │   ├── test_report_generation.yml                 [Test report generation]
│   │   └── test_scheduling.yml                        [Test scheduling]
│   │
│   ├── fixtures/                                       [Test data]
│   │   ├── sample_configs/                            [Sample device configs]
│   │   │   ├── ios_switch_config.txt
│   │   │   ├── ios_router_config.txt
│   │   │   └── nxos_switch_config.txt
│   │   ├── sample_ckl/                                [Sample CKL files]
│   │   │   └── sample_ios_stig.ckl
│   │   └── expected_results/                          [Expected test results]
│   │       └── sample_findings.json
│   │
│   ├── pytest.ini                                      [Pytest configuration]
│   └── README.md
│
├── docs/                                                [Documentation - ~8 files]
│   ├── USAGE.md                                        [Comprehensive usage guide]
│   ├── STIG_MAPPING.md                                 [STIG to check mapping reference]
│   ├── REMEDIATION_GUIDE.md                            [Remediation procedures guide]
│   ├── TROUBLESHOOTING.md                              [Common issues and solutions]
│   ├── SCHEDULING_SETUP.md                             [Scheduling setup guide]
│   ├── API_REFERENCE.md                                [Custom module API reference]
│   ├── CONTRIBUTING.md                                 [Contribution guidelines]
│   └── examples/                                       [Example configurations]
│       ├── example_inventory.yml                      [Example inventory file]
│       ├── example_group_vars.yml                     [Example group variables]
│       ├── example_playbook_runs.md                   [Example playbook executions]
│       └── example_custom_checks.yml                  [Example custom check definitions]
│
├── cache/                                               [Ansible cache directory]
│   ├── facts/                                          [Cached facts]
│   └── parsed_stigs/                                   [Cached parsed STIG data]
│
└── .vscode/                                             [VS Code configuration (optional)]
    ├── settings.json                                    [Editor settings]
    ├── extensions.json                                  [Recommended extensions]
    └── launch.json                                      [Debug configurations]
```

## File Count Summary by Category

| Category | Approximate File Count | Purpose |
|----------|------------------------|---------|
| **Core Configuration** | 8-10 | Ansible config, requirements, main docs |
| **Inventory** | 15-20 | Device inventories and variables |
| **Roles** | 80-100 | All role files (tasks, templates, vars, etc.) |
| **Custom Modules** | 8-10 | Python modules for custom functionality |
| **Filter Plugins** | 5-7 | Jinja2 filters |
| **STIG Checklists** | 5-10 (user-managed) | CKL files from DISA |
| **Config Templates** | 20-30 | Jinja2 templates for remediation |
| **Scripts** | 10-12 | Utility bash/python scripts |
| **Tests** | 15-20 | Unit and integration tests |
| **Documentation** | 10-15 | User guides and references |
| **Generated Files** | Grows over time | Reports, backups, logs |
| **TOTAL (initial)** | ~180-250 files | Excludes generated reports/backups |

## Key Directory Purposes

### Source Code Directories (Version Controlled)

1. **inventory/** - Device inventory and configuration variables
2. **roles/** - Core automation logic organized by function
3. **library/** - Custom Python modules for specialized tasks
4. **filter_plugins/** - Custom Jinja2 filters for data transformation
5. **config_templates/** - Jinja2 templates for device configuration
6. **scripts/** - Utility scripts for maintenance and operations
7. **tests/** - Test suite for validation
8. **docs/** - User and developer documentation

### Data Directories (User-Managed)

9. **stig_checklists/** - STIG CKL files from DISA (user updates when new versions release)

### Output Directories (Generated, Not Version Controlled)

10. **reports/** - Generated compliance reports (HTML, JSON, PDF)
11. **backups/** - Device configuration backups
12. **logs/** - Execution logs and audit trails
13. **cache/** - Ansible cache for performance

## Critical Files Explained

### Root Level

- **ansible.cfg**: Ansible configuration - connection settings, paths, performance tuning
- **requirements.txt**: Python packages needed (lxml, jinja2, paramiko, etc.)
- **requirements.yml**: Ansible collections needed (cisco.ios, cisco.nxos)
- **site.yml**: Main playbook that orchestrates everything
- **compliance-check.yml**: Runs compliance checks without remediation
- **remediation.yml**: Applies fixes to non-compliant configurations

### Inventory

- **hosts.yml**: Lists all devices with connection info
- **group_vars/all.yml**: Variables applied to all devices
- **group_vars/vault.yml**: Encrypted credentials (use ansible-vault)

### Roles Structure

Each role follows Ansible best practices:
- **defaults/main.yml**: Default variable values (lowest precedence)
- **vars/main.yml**: Role variables (higher precedence)
- **tasks/main.yml**: Main task entry point
- **templates/**: Jinja2 templates for configs and reports
- **files/**: Static files needed by the role
- **handlers/main.yml**: Event handlers (like service restarts)
- **meta/main.yml**: Role metadata and dependencies

### Custom Modules (library/)

- **ckl_parser.py**: Parses XML CKL files from DISA into Ansible data structures
- **cisco_config_parser.py**: Parses Cisco show command output
- **stig_compliance_checker.py**: Core compliance evaluation logic
- **config_differ.py**: Compares configurations before/after
- **finding_evaluator.py**: Evaluates check results and determines status
- **report_aggregator.py**: Aggregates data from multiple devices

### STIG Checklists

CKL files are downloaded from cyber.mil STIG Library:
- User places new CKL files in `stig_checklists/current/`
- Old versions automatically moved to `archive/` with datestamp
- Project automatically detects and parses new checklists

### Reports

Reports are organized by:
- **Timestamp**: Each run creates a timestamped directory
- **Schedule Type**: Scheduled runs organized by daily/weekly/monthly
- **Device vs Inventory**: Individual device reports vs aggregate reports
- **Format**: HTML (human-readable), JSON (machine-readable), PDF (printable)

### Backups

Configuration backups are:
- **Timestamped**: Each day gets its own directory
- **Pre/Post Remediation**: Separate backups before and after changes
- **Per Device**: One file per device
- **Full Config**: Complete running-config, not just changed sections

## Workflow Through Directory Structure

### Compliance Check Workflow

```
1. User runs: ansible-playbook compliance-check.yml

2. Ansible reads:
   - ansible.cfg (configuration)
   - inventory/production/hosts.yml (device list)
   - inventory/production/group_vars/ (variables)

3. Role: stig_parser
   - Reads: stig_checklists/current/*.ckl
   - Uses: library/ckl_parser.py
   - Output: Parsed STIG requirements in memory

4. Role: device_collector
   - Connects to devices in inventory
   - Collects running-config and show commands
   - Stores: reports/{timestamp}/artifacts/device_configs/

5. Role: compliance_checker
   - Reads: roles/compliance_checker/vars/stig_mappings.yml
   - Uses: library/stig_compliance_checker.py
   - Evaluates each STIG requirement against device config
   - Stores: reports/{timestamp}/device_reports/*.json

6. Role: report_generator
   - Reads: All device findings
   - Uses: roles/report_generator/templates/*.j2
   - Generates: HTML, JSON reports in reports/{timestamp}/

7. Role: notification (optional)
   - Reads: Report summaries
   - Sends: Email or webhook notifications
```

### Remediation Workflow

```
1. User runs: ansible-playbook remediation.yml

2. Steps 1-5 same as compliance check

3. Role: remediation_engine
   - Reads: Non-compliant findings
   - Reads: config_templates/ios/*.j2 (or nxos)
   - Generates remediation commands
   - Backs up configs to: backups/{date}/pre_remediation/
   - Applies fixes using cisco.ios.ios_config
   - Verifies changes
   - Backs up configs to: backups/{date}/post_remediation/

4. Re-run compliance_checker to verify fixes

5. Generate remediation report showing before/after
```

### Scheduled Workflow

```
1. Cron/Task Scheduler runs: scripts/schedule_compliance_check.sh run daily

2. Script runs: ansible-playbook compliance-check.yml

3. Reports stored in: reports/scheduled/daily/{date}/

4. Script creates symlink: reports/scheduled/daily/latest -> {date}

5. Cleanup old reports: Keep last 30 daily, 12 weekly, 12 monthly

6. Notifications sent if configured
```

## Data Flow Diagram

```
STIG CKL File → ckl_parser.py → Parsed Requirements (YAML/JSON)
                                        ↓
Device Inventory → device_collector → Running Configs
                                        ↓
Parsed Requirements + Running Configs → compliance_checker → Findings
                                                                ↓
                                        ┌───────────────────────┴──────────────────────┐
                                        ↓                                              ↓
                            report_generator → Reports                    remediation_engine → Fixed Configs
                                        ↓                                              ↓
                            HTML/JSON/PDF Files                          Backup + Apply Changes
                                        ↓                                              ↓
                            notification → Email/Slack/Teams            Verify Changes
```

## Growth Over Time

### Initial Installation
- **~180-250 files**: Core project files
- **~50 MB**: Without reports or backups

### After 1 Month
- **~400-500 files**: Adding daily reports and backups
- **~500 MB - 1 GB**: Depending on inventory size

### After 1 Year (with cleanup)
- **~600-800 files**: Retained reports per policy
- **~2-5 GB**: With historical data

### Without Cleanup
- Files and disk usage grow linearly with each execution
- Use cleanup scripts regularly

## Maintenance Recommendations

### Regular Tasks

1. **Update STIG Checklists** (when DISA releases new versions)
   ```bash
   ./scripts/update_stig_checklist.sh path/to/new.ckl
   ```

2. **Cleanup Old Reports** (monthly)
   ```bash
   ./scripts/cleanup_old_reports.py
   ```

3. **Archive Old Logs** (monthly)
   ```bash
   tar -czf logs/archive/$(date +%Y-%m).tar.gz logs/*.log
   > logs/*.log  # Truncate
   ```

4. **Backup Project** (before major changes)
   ```bash
   ./scripts/backup_project.sh
   ```

5. **Update Dependencies** (quarterly)
   ```bash
   pip install --upgrade -r requirements.txt
   ansible-galaxy collection install -r requirements.yml --upgrade
   ```

### Version Control

**Include in Git:**
- All source code (roles, library, scripts)
- Documentation (docs/)
- Configuration templates (config_templates/)
- Inventory structure (but vault.yml encrypted)
- Tests (tests/)

**Exclude from Git (.gitignore):**
- Generated reports (reports/)
- Backups (backups/)
- Logs (logs/)
- Cache (cache/)
- STIG checklists (stig_checklists/ - user-managed)
- Python cache (__pycache__/)
- Virtual environments (venv/)

## Summary

This structure provides:

1. **Clear Separation**: Code vs data vs output
2. **Scalability**: Easy to add devices, checks, or report formats
3. **Maintainability**: Standard Ansible role structure
4. **Flexibility**: User updates STIGs without code changes
5. **Automation**: Scheduling and cleanup built-in
6. **Auditability**: Complete logs and backups
7. **Reusability**: Templates and modules reusable across devices

Total initial files: **~180-250**
Total with 1 month of daily runs: **~400-500**
Expected growth: **~20-30 files per day** (reports + backups + logs)
