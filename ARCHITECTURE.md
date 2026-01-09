# Cisco STIG Compliance Checker - Architecture Documentation

## Project Overview

This Ansible project provides automated STIG (Security Technical Implementation Guide) compliance checking and remediation for Cisco network devices (switches and routers). The architecture supports both compliance-only auditing and automated remediation modes.

## Version Information
- **Project Version**: 1.0.0
- **Ansible Version**: 2.15+
- **Python Version**: 3.9+
- **Target Devices**: Cisco IOS, IOS-XE, NX-OS

---

## 1. Directory Structure

```
cisco-stig-compliance/
├── README.md                           # Project documentation and usage guide
├── ARCHITECTURE.md                     # This file - detailed architecture
├── requirements.txt                    # Python dependencies
├── requirements.yml                    # Ansible Galaxy dependencies
├── ansible.cfg                         # Ansible configuration
├── site.yml                            # Main orchestration playbook
├── compliance-check.yml                # Compliance checking playbook
├── remediation.yml                     # Remediation playbook
├── report-generation.yml               # Report generation playbook
│
├── inventory/                          # Inventory management
│   ├── production/
│   │   ├── hosts.yml                  # Production inventory
│   │   └── group_vars/
│   │       ├── all.yml                # Global variables
│   │       ├── cisco_ios.yml          # IOS-specific variables
│   │       ├── cisco_nxos.yml         # NX-OS-specific variables
│   │       └── vault.yml              # Encrypted credentials
│   ├── staging/
│   │   ├── hosts.yml
│   │   └── group_vars/
│   └── development/
│       ├── hosts.yml
│       └── group_vars/
│
├── roles/                              # Ansible roles
│   ├── stig_parser/                   # Parse CKL files and extract requirements
│   │   ├── defaults/
│   │   │   └── main.yml
│   │   ├── files/
│   │   ├── tasks/
│   │   │   ├── main.yml
│   │   │   ├── parse_ckl.yml
│   │   │   └── extract_checks.yml
│   │   ├── templates/
│   │   ├── vars/
│   │   │   └── main.yml
│   │   └── README.md
│   │
│   ├── device_collector/              # Collect device configurations
│   │   ├── defaults/
│   │   │   └── main.yml
│   │   ├── tasks/
│   │   │   ├── main.yml
│   │   │   ├── ios_collect.yml
│   │   │   ├── nxos_collect.yml
│   │   │   └── backup_config.yml
│   │   ├── templates/
│   │   └── README.md
│   │
│   ├── compliance_checker/            # Execute compliance checks
│   │   ├── defaults/
│   │   │   └── main.yml
│   │   ├── tasks/
│   │   │   ├── main.yml
│   │   │   ├── check_ios.yml
│   │   │   ├── check_nxos.yml
│   │   │   └── evaluate_findings.yml
│   │   ├── vars/
│   │   │   └── stig_mappings.yml
│   │   └── README.md
│   │
│   ├── remediation_engine/            # Apply remediation configurations
│   │   ├── defaults/
│   │   │   └── main.yml
│   │   ├── tasks/
│   │   │   ├── main.yml
│   │   │   ├── pre_remediation_checks.yml
│   │   │   ├── apply_ios_fixes.yml
│   │   │   ├── apply_nxos_fixes.yml
│   │   │   ├── verify_changes.yml
│   │   │   └── rollback.yml
│   │   ├── templates/
│   │   │   ├── ios_remediation.j2
│   │   │   └── nxos_remediation.j2
│   │   └── README.md
│   │
│   ├── report_generator/              # Generate compliance reports
│   │   ├── defaults/
│   │   │   └── main.yml
│   │   ├── tasks/
│   │   │   ├── main.yml
│   │   │   ├── prepare_data.yml
│   │   │   ├── generate_device_report.yml
│   │   │   ├── generate_inventory_report.yml
│   │   │   └── generate_executive_summary.yml
│   │   ├── templates/
│   │   │   ├── device_report.html.j2
│   │   │   ├── device_report.json.j2
│   │   │   ├── inventory_report.html.j2
│   │   │   ├── executive_summary.html.j2
│   │   │   └── compliance_dashboard.html.j2
│   │   └── README.md
│   │
│   └── notification/                   # Send notifications (email, webhook)
│       ├── defaults/
│       │   └── main.yml
│       ├── tasks/
│       │   ├── main.yml
│       │   ├── email_notification.yml
│       │   └── webhook_notification.yml
│       ├── templates/
│       │   └── email_template.j2
│       └── README.md
│
├── library/                            # Custom Ansible modules
│   ├── ckl_parser.py                  # Parse CKL XML files
│   ├── cisco_config_parser.py         # Parse Cisco configurations
│   ├── stig_compliance_checker.py     # STIG compliance evaluation
│   └── README.md
│
├── filter_plugins/                     # Custom Jinja2 filters
│   ├── stig_filters.py                # STIG-specific filters
│   ├── cisco_filters.py               # Cisco config parsing filters
│   └── report_filters.py              # Report formatting filters
│
├── stig_checklists/                    # STIG checklist files
│   ├── current/                       # Current active checklists
│   │   ├── Cisco_IOS_Switch_L2S_V2R8_STIG.ckl
│   │   ├── Cisco_IOS_Router_RTR_V2R8_STIG.ckl
│   │   └── Cisco_NX-OS_Switch_V2R4_STIG.ckl
│   ├── archive/                       # Previous versions
│   │   └── YYYY-MM-DD/
│   └── README.md                      # Instructions for updating
│
├── config_templates/                   # Device configuration templates
│   ├── ios/
│   │   ├── banner_template.j2
│   │   ├── aaa_template.j2
│   │   ├── logging_template.j2
│   │   └── snmp_template.j2
│   └── nxos/
│       ├── banner_template.j2
│       └── aaa_template.j2
│
├── reports/                            # Generated compliance reports
│   ├── YYYY-MM-DD_HH-MM-SS/           # Timestamped report directories
│   │   ├── device_reports/            # Individual device reports
│   │   │   ├── device1.example.com.html
│   │   │   ├── device1.example.com.json
│   │   │   ├── device2.example.com.html
│   │   │   └── device2.example.com.json
│   │   ├── inventory_report.html      # Full inventory report
│   │   ├── inventory_report.json      # Machine-readable inventory report
│   │   ├── executive_summary.html     # Executive summary
│   │   ├── compliance_dashboard.html  # Interactive dashboard
│   │   └── metadata.json              # Run metadata
│   ├── latest/                        # Symlink to most recent report
│   └── scheduled/                     # Scheduled scan reports
│       ├── daily/
│       ├── weekly/
│       └── monthly/
│
├── backups/                            # Device configuration backups
│   ├── YYYY-MM-DD/
│   │   ├── pre_remediation/
│   │   └── post_remediation/
│   └── latest/
│
├── logs/                               # Execution logs
│   ├── ansible.log                    # Ansible execution log
│   ├── compliance_checks.log          # Compliance checking log
│   ├── remediation.log                # Remediation actions log
│   └── scheduled_runs.log             # Scheduled execution log
│
├── scripts/                            # Utility scripts
│   ├── schedule_compliance_check.sh   # Cron/scheduled task setup
│   ├── compare_reports.py             # Compare two compliance reports
│   ├── update_stig_checklist.sh       # Update STIG checklist workflow
│   ├── validate_inventory.py          # Validate inventory file
│   └── cleanup_old_reports.py         # Cleanup old reports
│
├── tests/                              # Test suite
│   ├── unit/
│   │   ├── test_ckl_parser.py
│   │   └── test_cisco_config_parser.py
│   ├── integration/
│   │   ├── test_compliance_check.yml
│   │   └── test_remediation.yml
│   └── fixtures/
│       ├── sample_configs/
│       └── sample_ckl/
│
└── docs/                               # Additional documentation
    ├── USAGE.md                       # Usage guide
    ├── STIG_MAPPING.md                # STIG to check mapping
    ├── REMEDIATION_GUIDE.md           # Remediation procedures
    ├── TROUBLESHOOTING.md             # Common issues and solutions
    └── examples/
        ├── example_inventory.yml
        ├── example_group_vars.yml
        └── example_playbook_runs.md
```

---

## 2. Role Definitions and Responsibilities

### 2.1 stig_parser Role

**Purpose**: Parse STIG checklist (.ckl) files and extract compliance requirements.

**Responsibilities**:
- Parse XML-formatted CKL files
- Extract vulnerability IDs (V-IDs), rules, and check content
- Convert CKL format to Ansible-friendly data structures
- Support multiple STIG versions concurrently
- Cache parsed data for performance

**Key Tasks**:
- `parse_ckl.yml`: Parse XML structure of CKL files
- `extract_checks.yml`: Extract individual check requirements
- `validate_checklist.yml`: Validate CKL file integrity

**Input**: CKL files from `stig_checklists/current/`
**Output**: Structured YAML/JSON with STIG requirements

**Data Structure Output**:
```yaml
stig_requirements:
  - vuln_id: "V-220518"
    rule_id: "SV-220518r539432_rule"
    severity: "CAT2"
    group_title: "Cisco router must enforce approved authorizations"
    rule_title: "The Cisco router must be configured to enforce..."
    check_content: "Verify the router is configured to..."
    fix_text: "Configure the router to enforce..."
    cci: ["CCI-000213"]
    ios_check:
      command: "show running-config | include aaa"
      expected_pattern: "aaa new-model"
      evaluation_type: "contains"
```

### 2.2 device_collector Role

**Purpose**: Collect current configurations from Cisco devices.

**Responsibilities**:
- Connect to Cisco IOS/NX-OS devices
- Collect running configurations
- Execute show commands for STIG checks
- Backup configurations before remediation
- Handle connection timeouts and errors gracefully

**Key Tasks**:
- `ios_collect.yml`: Collect from IOS devices using cisco.ios modules
- `nxos_collect.yml`: Collect from NX-OS devices using cisco.nxos modules
- `backup_config.yml`: Backup configurations with timestamps

**Supported Commands**:
- `show running-config`
- `show version`
- `show users`
- `show logging`
- `show snmp`
- `show aaa`
- Custom commands per STIG requirement

**Output**:
- Device configurations stored in structured format
- Backup files in `backups/YYYY-MM-DD/`

### 2.3 compliance_checker Role

**Purpose**: Execute compliance checks against collected configurations.

**Responsibilities**:
- Compare device configurations against STIG requirements
- Evaluate compliance status (Compliant/Non-Compliant/Not Applicable)
- Generate finding details with evidence
- Support regex and exact matching
- Handle multi-line configuration checks

**Key Tasks**:
- `check_ios.yml`: IOS-specific compliance checks
- `check_nxos.yml`: NX-OS-specific compliance checks
- `evaluate_findings.yml`: Aggregate and classify findings

**Check Types**:
1. **Pattern Matching**: Regex patterns against config
2. **Command Output**: Execute show commands and evaluate
3. **Multi-line Context**: Check configuration blocks
4. **Negative Checks**: Ensure prohibited configs don't exist
5. **Value Comparison**: Compare actual vs required values

**Output Data Structure**:
```yaml
compliance_results:
  device: "switch01.example.com"
  timestamp: "2026-01-09T10:30:00Z"
  findings:
    - vuln_id: "V-220518"
      status: "Open"  # Open, NotAFinding, Not_Applicable
      severity: "CAT2"
      comments: "AAA authentication not configured"
      finding_details: |
        Expected: aaa new-model
        Found: <not configured>
      evidence: |
        show running-config | include aaa
        ! No output
```

### 2.4 remediation_engine Role

**Purpose**: Apply remediation configurations to non-compliant devices.

**Responsibilities**:
- Generate remediation commands based on findings
- Apply configurations safely with rollback capability
- Verify changes after application
- Log all changes for audit trail
- Support dry-run mode for testing

**Key Tasks**:
- `pre_remediation_checks.yml`: Validate before remediation
- `apply_ios_fixes.yml`: Apply IOS remediation commands
- `apply_nxos_fixes.yml`: Apply NX-OS remediation commands
- `verify_changes.yml`: Verify successful application
- `rollback.yml`: Rollback if verification fails

**Safety Features**:
- Configuration backup before changes
- Atomic transaction support (archive/rollback)
- Change validation
- Automatic rollback on failure
- Manual approval gate (optional)

**Remediation Workflow**:
1. Backup current configuration
2. Generate remediation commands from templates
3. Apply commands using cisco.ios.ios_config or cisco.nxos.nxos_config
4. Verify compliance after changes
5. Generate remediation report

### 2.5 report_generator Role

**Purpose**: Generate human-readable and machine-readable compliance reports.

**Responsibilities**:
- Generate individual device reports (HTML, JSON, PDF)
- Generate inventory-wide reports
- Create executive summaries
- Generate compliance dashboards
- Support multiple output formats

**Key Tasks**:
- `prepare_data.yml`: Aggregate and format data
- `generate_device_report.yml`: Individual device reports
- `generate_inventory_report.yml`: Full inventory report
- `generate_executive_summary.yml`: High-level summary

**Report Types**:

1. **Device Report** (HTML/JSON):
   - Device information
   - Overall compliance score
   - Findings by severity (CAT1, CAT2, CAT3)
   - Detailed finding information
   - Remediation recommendations

2. **Inventory Report** (HTML/JSON):
   - All devices in inventory
   - Compliance scores per device
   - Aggregate statistics
   - Trending data (if historical reports exist)

3. **Executive Summary** (HTML/PDF):
   - High-level compliance metrics
   - Risk assessment
   - Top vulnerabilities
   - Remediation priorities

4. **Compliance Dashboard** (HTML):
   - Interactive charts and graphs
   - Filterable findings table
   - Compliance trends over time

### 2.6 notification Role

**Purpose**: Send notifications about compliance status.

**Responsibilities**:
- Send email notifications
- POST to webhooks (Slack, Teams, etc.)
- Alert on critical findings
- Send scheduled report summaries

**Key Tasks**:
- `email_notification.yml`: Send email with SMTP
- `webhook_notification.yml`: POST to webhook URLs

---

## 3. STIG Parsing Architecture

### 3.1 CKL File Structure

CKL (Checklist) files are XML-based with the following structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CHECKLIST>
  <ASSET>
    <ROLE>None</ROLE>
    <ASSET_TYPE>Computing</ASSET_TYPE>
    <HOST_NAME></HOST_NAME>
  </ASSET>
  <STIGS>
    <iSTIG>
      <STIG_INFO>
        <SI_DATA>
          <SID_NAME>version</SID_NAME>
          <SID_DATA>2</SID_DATA>
        </SI_DATA>
        <SI_DATA>
          <SID_NAME>releaseinfo</SID_NAME>
          <SID_DATA>Release: 8 Benchmark Date: 26 Jul 2023</SID_DATA>
        </SI_DATA>
      </STIG_INFO>
      <VULN>
        <STIG_DATA>
          <VULN_ATTRIBUTE>Vuln_Num</VULN_ATTRIBUTE>
          <ATTRIBUTE_DATA>V-220518</ATTRIBUTE_DATA>
        </STIG_DATA>
        <STIG_DATA>
          <VULN_ATTRIBUTE>Severity</VULN_ATTRIBUTE>
          <ATTRIBUTE_DATA>medium</ATTRIBUTE_DATA>
        </STIG_DATA>
        <STIG_DATA>
          <VULN_ATTRIBUTE>Rule_Title</VULN_ATTRIBUTE>
          <ATTRIBUTE_DATA>The Cisco router must...</ATTRIBUTE_DATA>
        </STIG_DATA>
        <STIG_DATA>
          <VULN_ATTRIBUTE>Check_Content</VULN_ATTRIBUTE>
          <ATTRIBUTE_DATA>Review the router configuration...</ATTRIBUTE_DATA>
        </STIG_DATA>
        <STIG_DATA>
          <VULN_ATTRIBUTE>Fix_Text</VULN_ATTRIBUTE>
          <ATTRIBUTE_DATA>Configure the router...</ATTRIBUTE_DATA>
        </STIG_DATA>
        <STATUS>Not_Reviewed</STATUS>
        <FINDING_DETAILS></FINDING_DETAILS>
        <COMMENTS></COMMENTS>
      </VULN>
    </iSTIG>
  </STIGS>
</CHECKLIST>
```

### 3.2 Custom CKL Parser Module

**Location**: `library/ckl_parser.py`

**Functionality**:
```python
#!/usr/bin/env python3
"""
Custom Ansible module to parse STIG CKL files.

DOCUMENTATION:
module: ckl_parser
short_description: Parse STIG CKL XML files
description:
  - Parses STIG checklist (.ckl) XML files
  - Extracts vulnerability information and check requirements
  - Converts to Ansible-friendly data structures
options:
  ckl_file:
    description: Path to CKL file
    required: true
    type: path
  extract_checks:
    description: Extract check content for automation
    required: false
    default: true
    type: bool
"""

# Module implementation:
# 1. Parse XML using xml.etree.ElementTree
# 2. Extract VULN elements
# 3. Parse STIG_DATA elements within each VULN
# 4. Extract key attributes: Vuln_Num, Severity, Rule_Title,
#    Check_Content, Fix_Text, CCI_REF
# 5. Return structured data to Ansible
```

**Usage in Playbook**:
```yaml
- name: Parse STIG checklist
  ckl_parser:
    ckl_file: "{{ stig_checklist_path }}"
    extract_checks: true
  register: stig_data

- name: Display parsed STIG requirements
  debug:
    var: stig_data.vulnerabilities
```

### 3.3 STIG Mapping Configuration

**Location**: `roles/compliance_checker/vars/stig_mappings.yml`

This file maps STIG vulnerability IDs to automated check procedures:

```yaml
stig_check_mappings:
  # AAA Authentication
  V-220518:
    name: "AAA new-model required"
    applicable_platforms: ["ios", "ios-xe"]
    check_method: "config_contains"
    config_section: "aaa"
    required_config:
      - "aaa new-model"
    severity: "CAT2"

  V-220519:
    name: "AAA authentication login default group"
    applicable_platforms: ["ios", "ios-xe"]
    check_method: "config_regex"
    config_section: "aaa"
    required_pattern: "aaa authentication login default group \\S+ local"
    severity: "CAT2"

  # Banner Configuration
  V-220520:
    name: "Standard login banner"
    applicable_platforms: ["ios", "ios-xe", "nxos"]
    check_method: "banner_check"
    banner_type: "login"
    required_elements:
      - "authorized use only"
      - "monitoring"
      - "unauthorized access prohibited"
    case_sensitive: false
    severity: "CAT2"

  # Password Policy
  V-220650:
    name: "Minimum password length"
    applicable_platforms: ["ios", "ios-xe"]
    check_method: "config_value_comparison"
    command: "show running-config | include password"
    required_config: "security passwords min-length 15"
    evaluation: "min_value"
    min_value: 15
    severity: "CAT2"
```

### 3.4 Check Method Types

The compliance checker supports multiple check methods:

1. **config_contains**: Exact string match in configuration
2. **config_regex**: Regular expression pattern matching
3. **config_value_comparison**: Compare numeric values (min/max)
4. **banner_check**: Validate banner content
5. **show_command**: Execute show command and parse output
6. **multi_line_block**: Check multi-line configuration blocks
7. **negative_check**: Ensure config does NOT contain something
8. **custom_script**: Execute custom Python check logic

---

## 4. Compliance Checking Workflow

### 4.1 Overall Process Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMPLIANCE CHECK WORKFLOW                     │
└─────────────────────────────────────────────────────────────────┘

1. INITIALIZATION
   ├── Load inventory
   ├── Parse STIG checklist (CKL file)
   ├── Load STIG mappings
   └── Initialize result structures

2. DEVICE COLLECTION (Parallel per device)
   ├── Connect to device
   ├── Collect running configuration
   ├── Execute show commands
   ├── Store configuration locally
   └── Handle connection errors

3. COMPLIANCE CHECKING (Per device)
   ├── Load device configuration
   ├── Iterate through STIG requirements
   │   ├── Identify applicable checks
   │   ├── Execute check method
   │   ├── Evaluate result
   │   └── Record finding
   └── Generate device compliance summary

4. REPORT GENERATION
   ├── Aggregate all device results
   ├── Generate device reports
   ├── Generate inventory report
   ├── Generate executive summary
   └── Store reports with timestamp

5. NOTIFICATION (Optional)
   ├── Send email notifications
   └── POST to webhooks
```

### 4.2 Compliance Check Implementation

**Main Playbook**: `compliance-check.yml`

```yaml
---
- name: Cisco STIG Compliance Check
  hosts: all
  gather_facts: no
  vars:
    compliance_mode: "check_only"
    stig_checklist: "{{ stig_checklists_dir }}/current/{{ stig_version }}.ckl"
    report_timestamp: "{{ lookup('pipe', 'date +%Y-%m-%d_%H-%M-%S') }}"
    report_dir: "{{ reports_dir }}/{{ report_timestamp }}"

  tasks:
    - name: Create report directory
      file:
        path: "{{ report_dir }}/device_reports"
        state: directory
        mode: '0755'
      delegate_to: localhost
      run_once: yes

    - name: Parse STIG checklist
      include_role:
        name: stig_parser
      run_once: yes
      delegate_to: localhost

    - name: Collect device configurations
      include_role:
        name: device_collector

    - name: Execute compliance checks
      include_role:
        name: compliance_checker

    - name: Generate reports
      include_role:
        name: report_generator
      run_once: yes
      delegate_to: localhost

    - name: Send notifications
      include_role:
        name: notification
      when: notification_enabled | default(false)
      run_once: yes
      delegate_to: localhost
```

### 4.3 Check Execution Logic

**File**: `roles/compliance_checker/tasks/check_ios.yml`

```yaml
---
- name: Execute IOS compliance checks
  block:
    - name: Initialize findings list
      set_fact:
        device_findings: []

    - name: Iterate through STIG requirements
      include_tasks: execute_single_check.yml
      loop: "{{ stig_requirements }}"
      loop_control:
        loop_var: stig_item
      when:
        - "'ios' in stig_item.applicable_platforms"
        - stig_item.enabled | default(true)

    - name: Calculate compliance score
      set_fact:
        compliance_score: "{{ (device_findings | selectattr('status', 'equalto', 'NotAFinding') | list | length / device_findings | length * 100) | round(2) }}"

    - name: Save findings to file
      copy:
        content: "{{ {'device': inventory_hostname, 'findings': device_findings, 'score': compliance_score} | to_nice_json }}"
        dest: "{{ report_dir }}/device_reports/{{ inventory_hostname }}.json"
      delegate_to: localhost
```

**File**: `roles/compliance_checker/tasks/execute_single_check.yml`

```yaml
---
- name: Execute single STIG check
  block:
    - name: Set check variables
      set_fact:
        check_mapping: "{{ stig_check_mappings[stig_item.vuln_id] }}"
        check_result: {}

    - name: Execute check based on method
      include_tasks: "checks/{{ check_mapping.check_method }}.yml"

    - name: Record finding
      set_fact:
        device_findings: "{{ device_findings + [check_result] }}"

  rescue:
    - name: Record check error
      set_fact:
        device_findings: "{{ device_findings + [{
          'vuln_id': stig_item.vuln_id,
          'status': 'Error',
          'comments': 'Check execution failed: ' ~ ansible_failed_result.msg
        }] }}"
```

### 4.4 Example Check Implementation

**File**: `roles/compliance_checker/tasks/checks/config_contains.yml`

```yaml
---
- name: Check if configuration contains required string
  block:
    - name: Search for required configuration
      set_fact:
        config_found: "{{ check_mapping.required_config | select('in', device_config) | list | length == check_mapping.required_config | length }}"

    - name: Determine finding status
      set_fact:
        check_result:
          vuln_id: "{{ stig_item.vuln_id }}"
          rule_title: "{{ stig_item.rule_title }}"
          severity: "{{ stig_item.severity }}"
          status: "{{ 'NotAFinding' if config_found else 'Open' }}"
          finding_details: |
            Check: {{ check_mapping.name }}
            Required: {{ check_mapping.required_config | join(', ') }}
            Found: {{ 'Yes' if config_found else 'No' }}
          evidence: "{{ device_config | select('match', check_mapping.config_section) | list | join('\n') }}"
          check_date: "{{ ansible_date_time.iso8601 }}"
```

---

## 5. Report System Organization

### 5.1 Report Directory Structure

```
reports/
├── 2026-01-09_10-30-00/              # Timestamped report directory
│   ├── device_reports/                # Individual device reports
│   │   ├── switch01.example.com.html
│   │   ├── switch01.example.com.json
│   │   ├── switch02.example.com.html
│   │   ├── switch02.example.com.json
│   │   ├── router01.example.com.html
│   │   └── router01.example.com.json
│   ├── inventory_report.html         # Combined inventory report
│   ├── inventory_report.json         # Machine-readable inventory
│   ├── executive_summary.html        # Executive summary
│   ├── executive_summary.pdf         # PDF version (optional)
│   ├── compliance_dashboard.html     # Interactive dashboard
│   ├── metadata.json                 # Run metadata
│   └── artifacts/                    # Supporting files
│       ├── device_configs/           # Collected configurations
│       ├── raw_findings/             # Raw finding data
│       └── charts/                   # Chart images
├── latest/                            # Symlink to most recent
└── scheduled/                         # Organized scheduled reports
    ├── daily/
    │   ├── 2026-01-09/
    │   ├── 2026-01-08/
    │   └── 2026-01-07/
    ├── weekly/
    │   ├── 2026-W02/
    │   └── 2026-W01/
    └── monthly/
        ├── 2026-01/
        └── 2025-12/
```

### 5.2 Report Templates

#### Device Report Template

**File**: `roles/report_generator/templates/device_report.html.j2`

```jinja2
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>STIG Compliance Report - {{ device_name }}</title>
    <style>
        /* CSS styling for professional report layout */
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #2c3e50; color: white; padding: 20px; }
        .score-box { display: inline-block; padding: 20px; margin: 10px; border-radius: 5px; }
        .compliant { background: #27ae60; color: white; }
        .non-compliant { background: #e74c3c; color: white; }
        .partial { background: #f39c12; color: white; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #34495e; color: white; }
        .cat1 { border-left: 5px solid #e74c3c; }
        .cat2 { border-left: 5px solid #f39c12; }
        .cat3 { border-left: 5px solid #3498db; }
        .finding-open { color: #e74c3c; font-weight: bold; }
        .finding-closed { color: #27ae60; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>STIG Compliance Report</h1>
        <h2>{{ device_name }}</h2>
        <p>Report Generated: {{ report_date }}</p>
        <p>STIG Version: {{ stig_version }}</p>
    </div>

    <div class="summary">
        <h2>Compliance Summary</h2>
        <div class="score-box {{ 'compliant' if compliance_score >= 90 else ('partial' if compliance_score >= 70 else 'non-compliant') }}">
            <h3>Overall Score</h3>
            <h1>{{ compliance_score }}%</h1>
        </div>

        <table>
            <tr>
                <th>Metric</th>
                <th>Count</th>
                <th>Percentage</th>
            </tr>
            <tr>
                <td>Total Checks</td>
                <td>{{ total_checks }}</td>
                <td>100%</td>
            </tr>
            <tr class="finding-closed">
                <td>Compliant (Not a Finding)</td>
                <td>{{ compliant_count }}</td>
                <td>{{ (compliant_count / total_checks * 100) | round(2) }}%</td>
            </tr>
            <tr class="finding-open">
                <td>Non-Compliant (Open)</td>
                <td>{{ open_count }}</td>
                <td>{{ (open_count / total_checks * 100) | round(2) }}%</td>
            </tr>
            <tr>
                <td>Not Applicable</td>
                <td>{{ na_count }}</td>
                <td>{{ (na_count / total_checks * 100) | round(2) }}%</td>
            </tr>
        </table>

        <h3>Findings by Severity</h3>
        <table>
            <tr>
                <th>Severity</th>
                <th>Open</th>
                <th>Closed</th>
                <th>Total</th>
            </tr>
            <tr class="cat1">
                <td>CAT I (High)</td>
                <td>{{ cat1_open }}</td>
                <td>{{ cat1_closed }}</td>
                <td>{{ cat1_total }}</td>
            </tr>
            <tr class="cat2">
                <td>CAT II (Medium)</td>
                <td>{{ cat2_open }}</td>
                <td>{{ cat2_closed }}</td>
                <td>{{ cat2_total }}</td>
            </tr>
            <tr class="cat3">
                <td>CAT III (Low)</td>
                <td>{{ cat3_open }}</td>
                <td>{{ cat3_closed }}</td>
                <td>{{ cat3_total }}</td>
            </tr>
        </table>
    </div>

    <div class="findings">
        <h2>Detailed Findings</h2>

        {% for finding in findings %}
        <div class="finding {{ finding.severity | lower }}">
            <h3>{{ finding.vuln_id }} - {{ finding.rule_title }}</h3>
            <table>
                <tr>
                    <td><strong>Severity:</strong></td>
                    <td>{{ finding.severity }}</td>
                </tr>
                <tr>
                    <td><strong>Status:</strong></td>
                    <td class="{{ 'finding-open' if finding.status == 'Open' else 'finding-closed' }}">
                        {{ finding.status }}
                    </td>
                </tr>
                <tr>
                    <td><strong>Check Content:</strong></td>
                    <td>{{ finding.check_content }}</td>
                </tr>
                <tr>
                    <td><strong>Finding Details:</strong></td>
                    <td><pre>{{ finding.finding_details }}</pre></td>
                </tr>
                <tr>
                    <td><strong>Evidence:</strong></td>
                    <td><pre>{{ finding.evidence }}</pre></td>
                </tr>
                {% if finding.status == 'Open' %}
                <tr>
                    <td><strong>Remediation:</strong></td>
                    <td>{{ finding.fix_text }}</td>
                </tr>
                {% endif %}
            </table>
        </div>
        {% endfor %}
    </div>

    <div class="footer">
        <p>Generated by Cisco STIG Compliance Checker</p>
        <p>Report Location: {{ report_path }}</p>
    </div>
</body>
</html>
```

#### Inventory Report Template

**File**: `roles/report_generator/templates/inventory_report.html.j2`

Includes:
- Summary table of all devices
- Compliance score per device
- Heat map visualization
- Aggregated statistics
- Top vulnerabilities across inventory
- Trend analysis (if historical data available)

#### Executive Summary Template

**File**: `roles/report_generator/templates/executive_summary.html.j2`

Includes:
- High-level metrics (1-page summary)
- Compliance percentage
- Critical findings requiring immediate attention
- Risk assessment
- Remediation timeline recommendations

### 5.3 Report Generation Logic

**File**: `roles/report_generator/tasks/generate_device_report.yml`

```yaml
---
- name: Generate device compliance report
  block:
    - name: Load device findings
      set_fact:
        device_data: "{{ lookup('file', report_dir ~ '/device_reports/' ~ inventory_hostname ~ '.json') | from_json }}"

    - name: Calculate report metrics
      set_fact:
        total_checks: "{{ device_data.findings | length }}"
        compliant_count: "{{ device_data.findings | selectattr('status', 'equalto', 'NotAFinding') | list | length }}"
        open_count: "{{ device_data.findings | selectattr('status', 'equalto', 'Open') | list | length }}"
        na_count: "{{ device_data.findings | selectattr('status', 'equalto', 'Not_Applicable') | list | length }}"
        cat1_open: "{{ device_data.findings | selectattr('severity', 'equalto', 'CAT1') | selectattr('status', 'equalto', 'Open') | list | length }}"
        cat1_closed: "{{ device_data.findings | selectattr('severity', 'equalto', 'CAT1') | selectattr('status', 'equalto', 'NotAFinding') | list | length }}"
        cat1_total: "{{ device_data.findings | selectattr('severity', 'equalto', 'CAT1') | list | length }}"

    - name: Generate HTML report
      template:
        src: device_report.html.j2
        dest: "{{ report_dir }}/device_reports/{{ inventory_hostname }}.html"
      delegate_to: localhost

    - name: Generate JSON report
      copy:
        content: "{{ device_data | to_nice_json }}"
        dest: "{{ report_dir }}/device_reports/{{ inventory_hostname }}.json"
      delegate_to: localhost
```

### 5.4 Report Metadata

Each report directory includes a `metadata.json` file:

```json
{
  "report_id": "2026-01-09_10-30-00",
  "execution_start": "2026-01-09T10:30:00Z",
  "execution_end": "2026-01-09T10:45:23Z",
  "duration_seconds": 923,
  "stig_version": "Cisco_IOS_Switch_L2S_V2R8_STIG",
  "stig_release": "Release: 8 Benchmark Date: 26 Jul 2023",
  "inventory": {
    "total_devices": 25,
    "successful": 24,
    "failed": 1,
    "skipped": 0
  },
  "compliance_summary": {
    "overall_score": 78.5,
    "total_checks": 1250,
    "compliant": 981,
    "non_compliant": 189,
    "not_applicable": 80
  },
  "severity_breakdown": {
    "cat1_open": 5,
    "cat2_open": 84,
    "cat3_open": 100
  },
  "ansible_version": "2.15.3",
  "executed_by": "admin",
  "execution_mode": "compliance_check",
  "report_formats": ["html", "json"],
  "notifications_sent": true
}
```

---

## 6. Scheduling Implementation

### 6.1 Scheduling Script

**File**: `scripts/schedule_compliance_check.sh`

```bash
#!/bin/bash
#
# Cisco STIG Compliance Check Scheduler
# This script sets up scheduled compliance checks using cron (Linux) or Task Scheduler (Windows)
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ANSIBLE_PLAYBOOK="$PROJECT_DIR/compliance-check.yml"
INVENTORY="$PROJECT_DIR/inventory/production/hosts.yml"
LOG_DIR="$PROJECT_DIR/logs"
REPORT_BASE="$PROJECT_DIR/reports/scheduled"

# Configuration
SCHEDULE_TYPE="${1:-daily}"  # daily, weekly, monthly
NOTIFICATION_EMAIL="${2:-}"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_DIR/scheduled_runs.log"
}

# Create necessary directories
mkdir -p "$LOG_DIR"
mkdir -p "$REPORT_BASE/daily"
mkdir -p "$REPORT_BASE/weekly"
mkdir -p "$REPORT_BASE/monthly"

# Execute compliance check
execute_compliance_check() {
    local schedule_type="$1"
    local timestamp=$(date '+%Y-%m-%d_%H-%M-%S')
    local report_dir="$REPORT_BASE/$schedule_type/$timestamp"

    log "Starting $schedule_type compliance check..."

    # Run Ansible playbook
    ansible-playbook "$ANSIBLE_PLAYBOOK" \
        -i "$INVENTORY" \
        -e "report_dir=$report_dir" \
        -e "schedule_type=$schedule_type" \
        -e "notification_email=$NOTIFICATION_EMAIL" \
        >> "$LOG_DIR/scheduled_runs.log" 2>&1

    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        log "$schedule_type compliance check completed successfully"

        # Create symlink to latest report
        ln -sfn "$report_dir" "$REPORT_BASE/$schedule_type/latest"

        # Cleanup old reports (keep last 30 for daily, 12 for weekly, 12 for monthly)
        cleanup_old_reports "$schedule_type"
    else
        log "ERROR: $schedule_type compliance check failed with exit code $exit_code"
    fi

    return $exit_code
}

# Cleanup old reports
cleanup_old_reports() {
    local schedule_type="$1"
    local keep_count=30

    case "$schedule_type" in
        daily)   keep_count=30 ;;
        weekly)  keep_count=12 ;;
        monthly) keep_count=12 ;;
    esac

    cd "$REPORT_BASE/$schedule_type"

    # List directories (excluding 'latest' symlink), sort, keep only old ones
    ls -1dt */ 2>/dev/null | tail -n +$((keep_count + 1)) | while read -r dir; do
        log "Removing old report: $dir"
        rm -rf "$dir"
    done
}

# Setup cron job (Linux)
setup_cron() {
    local schedule_type="$1"
    local cron_schedule=""

    case "$schedule_type" in
        daily)
            cron_schedule="0 2 * * *"  # 2 AM daily
            ;;
        weekly)
            cron_schedule="0 2 * * 0"  # 2 AM every Sunday
            ;;
        monthly)
            cron_schedule="0 2 1 * *"  # 2 AM first day of month
            ;;
        *)
            echo "Invalid schedule type: $schedule_type"
            echo "Valid options: daily, weekly, monthly"
            exit 1
            ;;
    esac

    local cron_command="$SCRIPT_DIR/schedule_compliance_check.sh run $schedule_type"

    # Check if cron job already exists
    if crontab -l 2>/dev/null | grep -q "$cron_command"; then
        log "Cron job already exists for $schedule_type"
    else
        # Add cron job
        (crontab -l 2>/dev/null; echo "$cron_schedule $cron_command >> $LOG_DIR/cron.log 2>&1") | crontab -
        log "Cron job created for $schedule_type: $cron_schedule"
    fi
}

# Setup Windows Task Scheduler
setup_windows_task() {
    local schedule_type="$1"
    local task_name="CiscoSTIGCompliance_${schedule_type}"
    local schedule_modifier=""

    case "$schedule_type" in
        daily)
            schedule_modifier="DAILY"
            ;;
        weekly)
            schedule_modifier="WEEKLY"
            ;;
        monthly)
            schedule_modifier="MONTHLY"
            ;;
    esac

    # Create scheduled task using schtasks
    schtasks /Create /TN "$task_name" \
        /TR "bash $SCRIPT_DIR/schedule_compliance_check.sh run $schedule_type" \
        /SC "$schedule_modifier" \
        /ST 02:00 \
        /F

    log "Windows scheduled task created: $task_name"
}

# Main execution
main() {
    local action="${1:-setup}"
    local schedule_type="${2:-daily}"

    case "$action" in
        setup)
            log "Setting up $schedule_type scheduled compliance checks..."

            # Detect OS and setup appropriate scheduler
            if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
                setup_cron "$schedule_type"
            elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
                setup_windows_task "$schedule_type"
            else
                log "ERROR: Unsupported operating system: $OSTYPE"
                exit 1
            fi

            log "Scheduled $schedule_type compliance checks configured successfully"
            ;;

        run)
            execute_compliance_check "$schedule_type"
            ;;

        *)
            echo "Usage: $0 {setup|run} {daily|weekly|monthly} [notification_email]"
            exit 1
            ;;
    esac
}

main "$@"
```

### 6.2 Schedule Configuration

**File**: `inventory/production/group_vars/all.yml`

```yaml
---
# Scheduling configuration
scheduling:
  enabled: true

  # Daily compliance checks
  daily:
    enabled: true
    time: "02:00"  # 2 AM
    retain_reports: 30  # Keep last 30 daily reports

  # Weekly compliance checks
  weekly:
    enabled: true
    day: "sunday"  # Day of week
    time: "02:00"
    retain_reports: 12  # Keep last 12 weekly reports

  # Monthly compliance checks
  monthly:
    enabled: true
    day_of_month: 1  # First day of month
    time: "02:00"
    retain_reports: 12  # Keep last 12 monthly reports

# Notification settings
notification:
  enabled: true

  email:
    enabled: true
    smtp_server: "smtp.example.com"
    smtp_port: 587
    smtp_user: "compliance@example.com"
    smtp_password: "{{ vault_smtp_password }}"
    from_address: "cisco-stig-compliance@example.com"
    to_addresses:
      - "network-team@example.com"
      - "security-team@example.com"
    send_on:
      - "failure"  # Always send on failure
      - "critical_findings"  # Send if CAT1 findings exist
      - "weekly"  # Send weekly summary

  webhook:
    enabled: true
    slack_webhook_url: "{{ vault_slack_webhook }}"
    teams_webhook_url: "{{ vault_teams_webhook }}"
    send_on:
      - "failure"
      - "critical_findings"
```

### 6.3 Setup Instructions

**File**: `docs/SCHEDULING_SETUP.md`

```markdown
# Scheduling Setup Guide

## Quick Start

### Linux/macOS Setup

1. Configure notification settings in inventory:
   ```bash
   vi inventory/production/group_vars/all.yml
   ```

2. Setup daily checks:
   ```bash
   ./scripts/schedule_compliance_check.sh setup daily
   ```

3. Setup weekly checks:
   ```bash
   ./scripts/schedule_compliance_check.sh setup weekly
   ```

4. Setup monthly checks:
   ```bash
   ./scripts/schedule_compliance_check.sh setup monthly
   ```

5. Verify cron jobs:
   ```bash
   crontab -l
   ```

### Windows Setup

1. Open PowerShell as Administrator

2. Run setup script:
   ```powershell
   bash scripts/schedule_compliance_check.sh setup daily
   ```

3. Verify scheduled task:
   ```powershell
   schtasks /Query /TN "CiscoSTIGCompliance_daily"
   ```

## Manual Execution

Run compliance check manually:
```bash
./scripts/schedule_compliance_check.sh run daily network-admin@example.com
```

## Viewing Scheduled Reports

Reports are organized by schedule type:
```
reports/scheduled/
├── daily/
│   ├── latest/          <- Symlink to most recent
│   ├── 2026-01-09/
│   └── 2026-01-08/
├── weekly/
│   └── 2026-W02/
└── monthly/
    └── 2026-01/
```

## Troubleshooting

Check logs:
```bash
tail -f logs/scheduled_runs.log
```

Test email notifications:
```bash
ansible-playbook test-notification.yml -i inventory/production/hosts.yml
```
```

### 6.4 Report Retention Policy

**File**: `scripts/cleanup_old_reports.py`

```python
#!/usr/bin/env python3
"""
Cleanup old compliance reports based on retention policy.
"""

import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import argparse
import json

def cleanup_reports(reports_dir, schedule_type, retention_days):
    """
    Remove reports older than retention period.

    Args:
        reports_dir: Base reports directory
        schedule_type: daily, weekly, or monthly
        retention_days: Number of days to retain
    """
    schedule_dir = Path(reports_dir) / "scheduled" / schedule_type

    if not schedule_dir.exists():
        print(f"Directory does not exist: {schedule_dir}")
        return

    cutoff_date = datetime.now() - timedelta(days=retention_days)
    removed_count = 0

    for item in schedule_dir.iterdir():
        if item.is_dir() and item.name != "latest":
            try:
                # Parse directory name as date
                if schedule_type == "weekly":
                    # Format: 2026-W02
                    year, week = item.name.split('-W')
                    dir_date = datetime.strptime(f"{year}-W{week}-1", "%Y-W%W-%w")
                else:
                    # Format: 2026-01-09
                    dir_date = datetime.strptime(item.name, "%Y-%m-%d")

                if dir_date < cutoff_date:
                    print(f"Removing old report: {item}")
                    shutil.rmtree(item)
                    removed_count += 1

            except (ValueError, OSError) as e:
                print(f"Error processing {item}: {e}")

    print(f"Removed {removed_count} old {schedule_type} reports")

def main():
    parser = argparse.ArgumentParser(description="Cleanup old compliance reports")
    parser.add_argument("--reports-dir", default="E:/01- Chrome Downloads/cisco-stig-compliance/reports",
                        help="Base reports directory")
    parser.add_argument("--schedule-type", choices=["daily", "weekly", "monthly"],
                        help="Schedule type to cleanup")
    parser.add_argument("--retention-days", type=int,
                        help="Number of days to retain")

    args = parser.parse_args()

    # Default retention policies
    retention_policies = {
        "daily": 30,
        "weekly": 84,   # ~12 weeks
        "monthly": 365  # ~12 months
    }

    if args.schedule_type:
        retention = args.retention_days or retention_policies[args.schedule_type]
        cleanup_reports(args.reports_dir, args.schedule_type, retention)
    else:
        # Cleanup all schedule types
        for schedule_type, retention in retention_policies.items():
            retention = args.retention_days or retention
            cleanup_reports(args.reports_dir, schedule_type, retention)

if __name__ == "__main__":
    main()
```

---

## 7. Key Configuration Files

### 7.1 Ansible Configuration

**File**: `ansible.cfg`

```ini
[defaults]
# Inventory
inventory = ./inventory/production/hosts.yml
host_key_checking = False

# Roles and collections
roles_path = ./roles
collections_paths = ./collections

# Connection settings
timeout = 60
forks = 10
gathering = explicit

# Privilege escalation
become = False
become_method = enable
become_ask_pass = False

# Logging
log_path = ./logs/ansible.log
display_skipped_hosts = False
display_ok_hosts = True

# Performance
pipelining = True
fact_caching = jsonfile
fact_caching_connection = ./cache/facts
fact_caching_timeout = 3600

# Callbacks
stdout_callback = yaml
callbacks_enabled = profile_tasks, timer

# SSH settings
[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=60s -o StrictHostKeyChecking=no
control_path_dir = ~/.ansible/cp
pipelining = True

# Connection plugins
[connection]
connection_timeout = 60

# Persistent connection
[persistent_connection]
connect_timeout = 60
command_timeout = 60
```

### 7.2 Python Requirements

**File**: `requirements.txt`

```txt
# Ansible and core dependencies
ansible>=2.15.0,<3.0.0
ansible-core>=2.15.0
ansible-pylibssh>=1.0.0

# Cisco collections dependencies
paramiko>=3.0.0
netmiko>=4.1.0
napalm>=4.0.0

# XML parsing for CKL files
lxml>=4.9.0
xmltodict>=0.13.0

# Report generation
jinja2>=3.1.0
markdown>=3.4.0
pdfkit>=1.0.0
weasyprint>=59.0

# Data processing
pyyaml>=6.0
jsonschema>=4.17.0
pandas>=2.0.0

# Notification
requests>=2.28.0
smtplib

# Utilities
python-dateutil>=2.8.0
pytz>=2023.3
colorlog>=6.7.0

# Testing
pytest>=7.3.0
pytest-ansible>=4.0.0
molecule>=5.0.0
```

### 7.3 Ansible Galaxy Requirements

**File**: `requirements.yml`

```yaml
---
collections:
  # Cisco collections
  - name: cisco.ios
    version: ">=5.0.0"

  - name: cisco.nxos
    version: ">=5.0.0"

  - name: cisco.iosxr
    version: ">=5.0.0"

  # Utility collections
  - name: ansible.utils
    version: ">=2.10.0"

  - name: ansible.netcommon
    version: ">=5.0.0"

  - name: community.general
    version: ">=7.0.0"

roles:
  # No external roles required - all custom roles included
```

### 7.4 Example Inventory

**File**: `inventory/production/hosts.yml`

```yaml
---
all:
  children:
    cisco_devices:
      children:
        cisco_ios_switches:
          hosts:
            switch01.example.com:
              ansible_host: 10.1.1.10
              device_type: "cisco_ios"
              device_role: "access_switch"
              site: "headquarters"

            switch02.example.com:
              ansible_host: 10.1.1.11
              device_type: "cisco_ios"
              device_role: "distribution_switch"
              site: "headquarters"

        cisco_ios_routers:
          hosts:
            router01.example.com:
              ansible_host: 10.1.2.10
              device_type: "cisco_ios"
              device_role: "edge_router"
              site: "headquarters"

        cisco_nxos_switches:
          hosts:
            datacenter-sw01.example.com:
              ansible_host: 10.2.1.10
              device_type: "cisco_nxos"
              device_role: "datacenter_switch"
              site: "datacenter"

  vars:
    # Connection parameters
    ansible_connection: ansible.netcommon.network_cli
    ansible_network_os: cisco.ios.ios
    ansible_user: "{{ vault_ansible_user }}"
    ansible_password: "{{ vault_ansible_password }}"
    ansible_become: yes
    ansible_become_method: enable
    ansible_become_password: "{{ vault_enable_password }}"

    # STIG configuration
    stig_checklists_dir: "E:/01- Chrome Downloads/cisco-stig-compliance/stig_checklists"
    reports_dir: "E:/01- Chrome Downloads/cisco-stig-compliance/reports"
    backups_dir: "E:/01- Chrome Downloads/cisco-stig-compliance/backups"
```

---

## 8. Remediation Mode Architecture

### 8.1 Remediation Workflow

```
┌────────────────────────────────────────────────────────────────┐
│                    REMEDIATION WORKFLOW                         │
└────────────────────────────────────────────────────────────────┘

1. PRE-REMEDIATION
   ├── Run compliance check
   ├── Identify non-compliant items
   ├── Filter remediable items
   ├── Backup current configuration
   └── Generate remediation plan

2. APPROVAL GATE (Optional)
   ├── Display remediation plan
   ├── Request user approval
   └── Abort if not approved

3. REMEDIATION EXECUTION
   ├── Apply fixes sequentially
   ├── Verify each change
   ├── Log all changes
   └── Handle failures gracefully

4. POST-REMEDIATION
   ├── Run compliance check again
   ├── Compare before/after results
   ├── Verify improvements
   └── Generate remediation report

5. ROLLBACK (If needed)
   ├── Detect failed remediation
   ├── Restore backed-up configuration
   ├── Verify restoration
   └── Report rollback status
```

### 8.2 Remediation Playbook

**File**: `remediation.yml`

```yaml
---
- name: Cisco STIG Compliance Remediation
  hosts: all
  gather_facts: no
  vars:
    remediation_mode: "auto"  # auto, interactive, dry_run
    require_approval: true
    backup_before_remediation: true
    rollback_on_failure: true

  tasks:
    - name: Pre-remediation compliance check
      include_role:
        name: compliance_checker
      vars:
        check_phase: "pre_remediation"

    - name: Backup device configuration
      include_role:
        name: device_collector
      vars:
        backup_type: "pre_remediation"
      when: backup_before_remediation

    - name: Generate remediation plan
      include_role:
        name: remediation_engine
      vars:
        remediation_task: "generate_plan"

    - name: Display remediation plan
      debug:
        var: remediation_plan

    - name: Approval gate
      pause:
        prompt: "Review remediation plan above. Proceed with remediation? (yes/no)"
      register: approval
      when: require_approval and remediation_mode != "dry_run"

    - name: Apply remediation
      include_role:
        name: remediation_engine
      vars:
        remediation_task: "apply_fixes"
      when:
        - remediation_mode != "dry_run"
        - not require_approval or approval.user_input | lower == "yes"

    - name: Post-remediation compliance check
      include_role:
        name: compliance_checker
      vars:
        check_phase: "post_remediation"
      when: remediation_mode != "dry_run"

    - name: Generate remediation report
      include_role:
        name: report_generator
      vars:
        report_type: "remediation"

  rescue:
    - name: Rollback on failure
      include_role:
        name: remediation_engine
      vars:
        remediation_task: "rollback"
      when: rollback_on_failure
```

### 8.3 Safety Mechanisms

1. **Configuration Backup**: Always backup before changes
2. **Atomic Changes**: Use Cisco archive/rollback features
3. **Verification**: Verify each change before proceeding
4. **Approval Gates**: Optional human approval
5. **Dry Run Mode**: Test without applying changes
6. **Automatic Rollback**: Revert on failure
7. **Change Logging**: Audit trail of all changes

---

## 9. Usage Examples

### 9.1 Run Compliance Check

```bash
# Check all devices
ansible-playbook compliance-check.yml -i inventory/production/hosts.yml

# Check specific device
ansible-playbook compliance-check.yml -i inventory/production/hosts.yml --limit switch01.example.com

# Check with specific STIG version
ansible-playbook compliance-check.yml -i inventory/production/hosts.yml \
  -e "stig_version=Cisco_IOS_Switch_L2S_V2R9_STIG"

# Dry run (no actual connection)
ansible-playbook compliance-check.yml -i inventory/production/hosts.yml --check
```

### 9.2 Run Remediation

```bash
# Remediate all non-compliant findings (with approval)
ansible-playbook remediation.yml -i inventory/production/hosts.yml

# Remediate specific device
ansible-playbook remediation.yml -i inventory/production/hosts.yml --limit router01.example.com

# Dry run remediation (show what would be changed)
ansible-playbook remediation.yml -i inventory/production/hosts.yml \
  -e "remediation_mode=dry_run"

# Auto-remediate without approval (use with caution)
ansible-playbook remediation.yml -i inventory/production/hosts.yml \
  -e "require_approval=false"
```

### 9.3 Generate Reports Only

```bash
# Generate reports from existing compliance data
ansible-playbook report-generation.yml -i inventory/production/hosts.yml

# Generate specific report type
ansible-playbook report-generation.yml -i inventory/production/hosts.yml \
  -e "report_type=executive_summary"
```

### 9.4 Update STIG Checklist

```bash
# Update to new STIG version
./scripts/update_stig_checklist.sh Cisco_IOS_Switch_L2S_V2R9_STIG.ckl

# This will:
# 1. Archive current checklist
# 2. Copy new checklist to current/
# 3. Parse and validate new checklist
# 4. Update mapping files if needed
```

### 9.5 Compare Reports

```bash
# Compare two compliance reports
./scripts/compare_reports.py \
  --report1 reports/2026-01-08_10-00-00/inventory_report.json \
  --report2 reports/2026-01-09_10-00-00/inventory_report.json \
  --output reports/comparison_report.html
```

---

## 10. Extension Points

### 10.1 Adding New STIG Checks

1. Update STIG checklist in `stig_checklists/current/`
2. Add check mapping in `roles/compliance_checker/vars/stig_mappings.yml`
3. If needed, create custom check method in `roles/compliance_checker/tasks/checks/`

### 10.2 Supporting New Device Types

1. Add device type to inventory group
2. Create collection tasks in `roles/device_collector/tasks/`
3. Create compliance check tasks in `roles/compliance_checker/tasks/`
4. Add remediation templates in `config_templates/`

### 10.3 Custom Report Formats

1. Create new template in `roles/report_generator/templates/`
2. Add report generation task in `roles/report_generator/tasks/`
3. Update report playbook to include new format

### 10.4 Additional Notifications

1. Add notification method in `roles/notification/tasks/`
2. Create template if needed in `roles/notification/templates/`
3. Update notification configuration in group_vars

---

## 11. Security Considerations

### 11.1 Credential Management

- Store credentials in Ansible Vault
- Use separate vault files per environment
- Rotate credentials regularly
- Use service accounts with minimal permissions

### 11.2 Access Control

- Restrict access to inventory files
- Protect report directories
- Audit all remediation activities
- Implement approval workflows for production

### 11.3 Network Security

- Use SSH key authentication where possible
- Enable encrypted connections
- Implement network segmentation
- Use jump hosts for sensitive environments

### 11.4 Audit Trail

- Log all compliance checks
- Track all remediation actions
- Maintain configuration backups
- Store reports for compliance audits

---

## 12. Performance Optimization

### 12.1 Parallel Execution

- Use Ansible forks for parallel device checks
- Adjust `forks` setting in ansible.cfg based on infrastructure
- Consider network bandwidth and device load

### 12.2 Caching

- Cache STIG checklist parsing results
- Use Ansible fact caching
- Cache device configurations for multiple checks

### 12.3 Incremental Checks

- Skip compliant checks in subsequent runs
- Focus on previously non-compliant items
- Implement delta checking for large inventories

---

## 13. Troubleshooting

### 13.1 Common Issues

1. **Connection Timeout**
   - Increase timeout in ansible.cfg
   - Check network connectivity
   - Verify credentials

2. **CKL Parsing Errors**
   - Validate XML format
   - Check STIG version compatibility
   - Review parser logs

3. **Remediation Failures**
   - Review device logs
   - Check configuration syntax
   - Verify device capabilities

4. **Report Generation Issues**
   - Check disk space
   - Verify template syntax
   - Review Python dependencies

### 13.2 Debug Mode

```bash
# Run with verbose output
ansible-playbook compliance-check.yml -i inventory/production/hosts.yml -vvv

# Check specific task
ansible-playbook compliance-check.yml -i inventory/production/hosts.yml \
  --start-at-task="Execute compliance checks"

# Debug mode
ANSIBLE_DEBUG=1 ansible-playbook compliance-check.yml -i inventory/production/hosts.yml
```

---

## 14. Maintenance

### 14.1 Regular Tasks

- Update STIG checklists when new versions release
- Review and update STIG mappings
- Rotate logs and old reports
- Update Ansible and Python dependencies
- Review and update remediation templates

### 14.2 Health Checks

- Test scheduled jobs regularly
- Verify notification delivery
- Validate report generation
- Test backup/restore procedures

---

## 15. Support and Documentation

### 15.1 Additional Resources

- `docs/USAGE.md` - Detailed usage guide
- `docs/STIG_MAPPING.md` - STIG check mappings reference
- `docs/REMEDIATION_GUIDE.md` - Remediation procedures
- `docs/TROUBLESHOOTING.md` - Detailed troubleshooting guide

### 15.2 Contact

For issues, enhancements, or questions:
- Check documentation in `docs/`
- Review logs in `logs/`
- Consult STIG resources at cyber.mil

---

**Document Version**: 1.0.0
**Last Updated**: 2026-01-09
**Author**: DevOps Engineering Team
