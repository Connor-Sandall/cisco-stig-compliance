# Cisco STIG Compliance Checker - Implementation Guide

## Overview

This guide provides step-by-step instructions for implementing the Cisco STIG Compliance Checker project. Follow these phases in order for a successful deployment.

---

## Implementation Phases

### Phase 1: Project Setup (Week 1)
### Phase 2: Core Infrastructure (Week 2)
### Phase 3: Compliance Checking (Week 3)
### Phase 4: Remediation & Reports (Week 4)
### Phase 5: Scheduling & Operations (Week 5)
### Phase 6: Testing & Validation (Week 6)

---

## Phase 1: Project Setup (Week 1)

### Step 1.1: Create Base Directory Structure

```bash
# Create main project directory
mkdir -p "E:\01- Chrome Downloads\cisco-stig-compliance"
cd "E:\01- Chrome Downloads\cisco-stig-compliance"

# Create primary directories
mkdir -p inventory/{production,staging,development}/{group_vars,host_vars}
mkdir -p roles
mkdir -p library
mkdir -p filter_plugins
mkdir -p stig_checklists/{current,archive,metadata}
mkdir -p config_templates/{ios,nxos}
mkdir -p reports/{scheduled/{daily,weekly,monthly}}
mkdir -p backups
mkdir -p logs/{archive}
mkdir -p scripts
mkdir -p tests/{unit,integration,fixtures/{sample_configs,sample_ckl,expected_results}}
mkdir -p docs/examples
mkdir -p cache/{facts,parsed_stigs}
```

### Step 1.2: Create Core Configuration Files

**Create: ansible.cfg**

```bash
cat > ansible.cfg << 'EOF'
[defaults]
inventory = ./inventory/production/hosts.yml
host_key_checking = False
roles_path = ./roles
collections_paths = ./collections
timeout = 60
forks = 10
gathering = explicit
become = False
become_method = enable
log_path = ./logs/ansible.log
display_skipped_hosts = False
display_ok_hosts = True
pipelining = True
fact_caching = jsonfile
fact_caching_connection = ./cache/facts
fact_caching_timeout = 3600
stdout_callback = yaml
callbacks_enabled = profile_tasks, timer

[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=60s -o StrictHostKeyChecking=no
pipelining = True

[persistent_connection]
connect_timeout = 60
command_timeout = 60
EOF
```

**Create: requirements.txt**

```bash
cat > requirements.txt << 'EOF'
ansible>=2.15.0,<3.0.0
ansible-core>=2.15.0
paramiko>=3.0.0
netmiko>=4.1.0
lxml>=4.9.0
xmltodict>=0.13.0
jinja2>=3.1.0
pyyaml>=6.0
jsonschema>=4.17.0
requests>=2.28.0
python-dateutil>=2.8.0
pytz>=2023.3
colorlog>=6.7.0
pytest>=7.3.0
EOF
```

**Create: requirements.yml**

```bash
cat > requirements.yml << 'EOF'
---
collections:
  - name: cisco.ios
    version: ">=5.0.0"
  - name: cisco.nxos
    version: ">=5.0.0"
  - name: ansible.utils
    version: ">=2.10.0"
  - name: ansible.netcommon
    version: ">=5.0.0"
  - name: community.general
    version: ">=7.0.0"
EOF
```

**Create: .gitignore**

```bash
cat > .gitignore << 'EOF'
# Generated reports and data
reports/*
!reports/.gitkeep
backups/*
!backups/.gitkeep
logs/*
!logs/.gitkeep

# Cache
cache/
*.retry
__pycache__/
*.pyc
.pytest_cache/

# Virtual environments
venv/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Ansible
*.retry

# User-specific STIG checklists (managed separately)
stig_checklists/current/*.ckl
stig_checklists/archive/

# Sensitive data
inventory/*/group_vars/vault.yml
*.pem
*.key
EOF
```

### Step 1.3: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install Ansible collections
ansible-galaxy collection install -r requirements.yml
```

### Step 1.4: Create Initial Documentation

```bash
# Create README.md with project overview
cat > README.md << 'EOF'
# Cisco STIG Compliance Checker

Automated STIG compliance checking and remediation for Cisco network devices.

## Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Configure inventory: Edit `inventory/production/hosts.yml`
3. Add STIG checklists: Place .ckl files in `stig_checklists/current/`
4. Run compliance check: `ansible-playbook compliance-check.yml`

## Documentation

- [Architecture](ARCHITECTURE.md) - Detailed architecture and design
- [Project Structure](PROJECT_STRUCTURE.md) - Complete directory structure
- [Implementation Guide](IMPLEMENTATION_GUIDE.md) - This file
- [Usage Guide](docs/USAGE.md) - How to use the system

## Support

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common issues.
EOF
```

---

## Phase 2: Core Infrastructure (Week 2)

### Step 2.1: Create Inventory Structure

**Create: inventory/production/hosts.yml**

```yaml
---
all:
  children:
    cisco_devices:
      children:
        cisco_ios_switches:
          hosts:
            # Add your switches here
            # Example:
            # switch01.example.com:
            #   ansible_host: 10.1.1.10
            #   device_type: "cisco_ios"
            #   device_role: "access_switch"
            #   site: "headquarters"

        cisco_ios_routers:
          hosts:
            # Add your routers here

        cisco_nxos_switches:
          hosts:
            # Add your NX-OS switches here

  vars:
    ansible_connection: ansible.netcommon.network_cli
    ansible_network_os: cisco.ios.ios
    ansible_user: "{{ vault_ansible_user }}"
    ansible_password: "{{ vault_ansible_password }}"
    ansible_become: yes
    ansible_become_method: enable
    ansible_become_password: "{{ vault_enable_password }}"

    stig_checklists_dir: "E:/01- Chrome Downloads/cisco-stig-compliance/stig_checklists"
    reports_dir: "E:/01- Chrome Downloads/cisco-stig-compliance/reports"
    backups_dir: "E:/01- Chrome Downloads/cisco-stig-compliance/backups"
```

**Create: inventory/production/group_vars/all.yml**

```yaml
---
# Global variables for all devices

# STIG Configuration
stig_version: "Cisco_IOS_Switch_L2S_V2R8_STIG"
stig_checklist_path: "{{ stig_checklists_dir }}/current/{{ stig_version }}.ckl"

# Report Configuration
report_formats:
  - html
  - json

report_retention:
  adhoc: 30  # days
  daily: 30
  weekly: 84
  monthly: 365

# Backup Configuration
backup_enabled: true
backup_retention_days: 30

# Notification Configuration
notification:
  enabled: false
  email:
    enabled: false
    smtp_server: "smtp.example.com"
    smtp_port: 587
    from_address: "cisco-stig@example.com"
    to_addresses:
      - "network-team@example.com"
  webhook:
    enabled: false
    slack_webhook_url: ""

# Compliance Check Configuration
compliance_check:
  parallel_execution: true
  max_forks: 10
  timeout: 300

# Remediation Configuration
remediation:
  require_approval: true
  backup_before: true
  rollback_on_failure: true
  dry_run: false
```

**Create: inventory/production/group_vars/vault.yml**

```bash
# Create encrypted vault file
ansible-vault create inventory/production/group_vars/vault.yml

# Add the following content when prompted:
---
vault_ansible_user: "admin"
vault_ansible_password: "YourPasswordHere"
vault_enable_password: "YourEnablePasswordHere"
vault_smtp_password: "YourSMTPPasswordHere"
vault_slack_webhook: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### Step 2.2: Create Custom Ansible Modules

**Create: library/ckl_parser.py**

```python
#!/usr/bin/env python3
"""
Custom Ansible module to parse STIG CKL files.
"""

DOCUMENTATION = """
---
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

EXAMPLES = """
- name: Parse STIG checklist
  ckl_parser:
    ckl_file: "/path/to/checklist.ckl"
    extract_checks: true
  register: stig_data
"""

RETURN = """
stig_info:
  description: STIG metadata
  returned: always
  type: dict
vulnerabilities:
  description: List of STIG vulnerabilities
  returned: always
  type: list
"""

from ansible.module_utils.basic import AnsibleModule
import xml.etree.ElementTree as ET


def parse_ckl_file(ckl_file_path):
    """Parse CKL XML file and extract STIG data."""
    try:
        tree = ET.parse(ckl_file_path)
        root = tree.getroot()

        # Extract STIG metadata
        stig_info = {}
        stig_info_elem = root.find('.//STIG_INFO')
        if stig_info_elem:
            for si_data in stig_info_elem.findall('SI_DATA'):
                sid_name = si_data.find('SID_NAME')
                sid_data = si_data.find('SID_DATA')
                if sid_name is not None and sid_data is not None:
                    stig_info[sid_name.text] = sid_data.text

        # Extract vulnerabilities
        vulnerabilities = []
        for vuln in root.findall('.//VULN'):
            vuln_data = {}

            # Extract STIG_DATA elements
            for stig_data in vuln.findall('STIG_DATA'):
                attr = stig_data.find('VULN_ATTRIBUTE')
                data = stig_data.find('ATTRIBUTE_DATA')
                if attr is not None and data is not None:
                    vuln_data[attr.text] = data.text

            # Extract status and comments
            status = vuln.find('STATUS')
            if status is not None:
                vuln_data['STATUS'] = status.text

            finding_details = vuln.find('FINDING_DETAILS')
            if finding_details is not None:
                vuln_data['FINDING_DETAILS'] = finding_details.text

            comments = vuln.find('COMMENTS')
            if comments is not None:
                vuln_data['COMMENTS'] = comments.text

            vulnerabilities.append(vuln_data)

        return {
            'stig_info': stig_info,
            'vulnerabilities': vulnerabilities
        }

    except Exception as e:
        raise Exception(f"Failed to parse CKL file: {str(e)}")


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ckl_file=dict(type='path', required=True),
            extract_checks=dict(type='bool', default=True)
        ),
        supports_check_mode=True
    )

    ckl_file = module.params['ckl_file']

    try:
        result = parse_ckl_file(ckl_file)
        module.exit_json(
            changed=False,
            stig_info=result['stig_info'],
            vulnerabilities=result['vulnerabilities']
        )
    except Exception as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
```

**Create: library/cisco_config_parser.py**

```python
#!/usr/bin/env python3
"""
Custom Ansible module to parse Cisco device configurations.
"""

DOCUMENTATION = """
---
module: cisco_config_parser
short_description: Parse Cisco device configurations
description:
  - Parses Cisco IOS/NX-OS configuration text
  - Extracts specific configuration sections
  - Supports pattern matching and regex
options:
  config:
    description: Configuration text to parse
    required: true
    type: str
  section:
    description: Configuration section to extract (e.g., 'aaa', 'interface')
    required: false
    type: str
  pattern:
    description: Regex pattern to search for
    required: false
    type: str
"""

from ansible.module_utils.basic import AnsibleModule
import re


def parse_config_section(config_text, section=None):
    """Extract configuration section."""
    if not section:
        return config_text.split('\n')

    lines = config_text.split('\n')
    section_lines = []
    in_section = False

    for line in lines:
        if line.startswith(section):
            in_section = True
            section_lines.append(line)
        elif in_section:
            if line and not line.startswith(' '):
                # Exited section
                break
            section_lines.append(line)

    return section_lines


def search_pattern(config_text, pattern):
    """Search for pattern in configuration."""
    regex = re.compile(pattern, re.MULTILINE)
    matches = regex.findall(config_text)
    return matches


def main():
    module = AnsibleModule(
        argument_spec=dict(
            config=dict(type='str', required=True),
            section=dict(type='str', required=False),
            pattern=dict(type='str', required=False)
        ),
        supports_check_mode=True
    )

    config = module.params['config']
    section = module.params.get('section')
    pattern = module.params.get('pattern')

    try:
        result = {}

        if section:
            result['section_lines'] = parse_config_section(config, section)

        if pattern:
            result['matches'] = search_pattern(config, pattern)

        if not section and not pattern:
            result['lines'] = config.split('\n')

        module.exit_json(changed=False, **result)

    except Exception as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
```

### Step 2.3: Create Role Skeletons

```bash
# Create role skeletons
for role in stig_parser device_collector compliance_checker remediation_engine report_generator notification; do
    ansible-galaxy init "roles/$role"
done
```

---

## Phase 3: Compliance Checking (Week 3)

### Step 3.1: Implement stig_parser Role

**Create: roles/stig_parser/tasks/main.yml**

```yaml
---
- name: Parse STIG checklist
  include_tasks: parse_ckl.yml
  when: stig_checklist_path is defined

- name: Extract check requirements
  include_tasks: extract_checks.yml

- name: Cache parsed data
  include_tasks: cache_parsed_data.yml
  when: cache_enabled | default(true)
```

**Create: roles/stig_parser/tasks/parse_ckl.yml**

```yaml
---
- name: Verify CKL file exists
  stat:
    path: "{{ stig_checklist_path }}"
  register: ckl_file
  delegate_to: localhost

- name: Fail if CKL file not found
  fail:
    msg: "STIG checklist not found: {{ stig_checklist_path }}"
  when: not ckl_file.stat.exists

- name: Parse CKL file
  ckl_parser:
    ckl_file: "{{ stig_checklist_path }}"
    extract_checks: true
  register: parsed_stig
  delegate_to: localhost

- name: Set STIG facts
  set_fact:
    stig_info: "{{ parsed_stig.stig_info }}"
    stig_vulnerabilities: "{{ parsed_stig.vulnerabilities }}"
    cacheable: yes

- name: Display STIG information
  debug:
    msg: "Parsed STIG {{ stig_info.title | default('Unknown') }} - {{ stig_vulnerabilities | length }} checks"
```

**Create: roles/stig_parser/tasks/extract_checks.yml**

```yaml
---
- name: Extract actionable checks
  set_fact:
    stig_requirements: "{{ stig_requirements | default([]) + [item] }}"
  loop: "{{ stig_vulnerabilities }}"
  when:
    - item.Vuln_Num is defined
    - item.Rule_Title is defined
  delegate_to: localhost
  run_once: yes

- name: Display check count
  debug:
    msg: "Extracted {{ stig_requirements | length }} actionable checks"
  run_once: yes
```

### Step 3.2: Implement device_collector Role

**Create: roles/device_collector/tasks/main.yml**

```yaml
---
- name: Determine device OS
  set_fact:
    device_os: "{{ ansible_network_os | default('cisco.ios.ios') }}"

- name: Collect IOS device configuration
  include_tasks: ios_collect.yml
  when: "'ios' in device_os"

- name: Collect NX-OS device configuration
  include_tasks: nxos_collect.yml
  when: "'nxos' in device_os"

- name: Backup configuration
  include_tasks: backup_config.yml
  when: backup_enabled | default(true)
```

**Create: roles/device_collector/tasks/ios_collect.yml**

```yaml
---
- name: Gather IOS facts
  cisco.ios.ios_facts:
    gather_subset:
      - all
  register: ios_facts

- name: Collect running configuration
  cisco.ios.ios_command:
    commands:
      - show running-config
  register: running_config

- name: Execute show commands for STIG checks
  cisco.ios.ios_command:
    commands:
      - show version
      - show users
      - show logging
      - show snmp
      - show aaa sessions
      - show privilege
  register: show_commands

- name: Set device facts
  set_fact:
    device_config: "{{ running_config.stdout[0] }}"
    device_facts: "{{ ios_facts.ansible_facts }}"
    device_show_output: "{{ show_commands.stdout }}"
    cacheable: yes
```

### Step 3.3: Implement compliance_checker Role

**Create: roles/compliance_checker/vars/stig_mappings.yml**

```yaml
---
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
    enabled: true

  V-220519:
    name: "AAA authentication login"
    applicable_platforms: ["ios", "ios-xe"]
    check_method: "config_regex"
    config_section: "aaa"
    required_pattern: "aaa authentication login default group \\S+"
    severity: "CAT2"
    enabled: true

  # Banner Configuration
  V-220520:
    name: "Login banner configured"
    applicable_platforms: ["ios", "ios-xe", "nxos"]
    check_method: "banner_check"
    banner_type: "login"
    required_elements:
      - "authorized"
      - "monitoring"
    case_sensitive: false
    severity: "CAT2"
    enabled: true

  # Add more STIG checks here...
```

**Create: roles/compliance_checker/tasks/main.yml**

```yaml
---
- name: Initialize compliance check
  set_fact:
    device_findings: []
    check_start_time: "{{ ansible_date_time.iso8601 }}"

- name: Execute IOS compliance checks
  include_tasks: check_ios.yml
  when: "'ios' in ansible_network_os"

- name: Execute NX-OS compliance checks
  include_tasks: check_nxos.yml
  when: "'nxos' in ansible_network_os"

- name: Evaluate findings
  include_tasks: evaluate_findings.yml

- name: Save findings to file
  copy:
    content: "{{ device_findings | to_nice_json }}"
    dest: "{{ report_dir }}/device_reports/{{ inventory_hostname }}.json"
  delegate_to: localhost
```

**Create: roles/compliance_checker/tasks/check_ios.yml**

```yaml
---
- name: Execute IOS compliance checks
  include_tasks: execute_single_check.yml
  loop: "{{ stig_requirements }}"
  loop_control:
    loop_var: stig_item
  when:
    - stig_check_mappings[stig_item.Vuln_Num] is defined
    - "'ios' in stig_check_mappings[stig_item.Vuln_Num].applicable_platforms"
    - stig_check_mappings[stig_item.Vuln_Num].enabled | default(true)
```

**Create: roles/compliance_checker/tasks/execute_single_check.yml**

```yaml
---
- name: Get check mapping
  set_fact:
    check_mapping: "{{ stig_check_mappings[stig_item.Vuln_Num] }}"

- name: Execute check method
  include_tasks: "checks/{{ check_mapping.check_method }}.yml"
  when: check_mapping is defined
```

**Create: roles/compliance_checker/tasks/checks/config_contains.yml**

```yaml
---
- name: Check if configuration contains required strings
  set_fact:
    config_found: "{{ item in device_config }}"
  loop: "{{ check_mapping.required_config }}"
  register: config_checks

- name: Determine compliance status
  set_fact:
    is_compliant: "{{ config_checks.results | selectattr('ansible_facts.config_found', 'equalto', true) | list | length == check_mapping.required_config | length }}"

- name: Record finding
  set_fact:
    device_findings: "{{ device_findings + [{
      'vuln_id': stig_item.Vuln_Num,
      'rule_title': stig_item.Rule_Title,
      'severity': stig_item.Severity | upper,
      'status': 'NotAFinding' if is_compliant else 'Open',
      'finding_details': check_mapping.name ~ ' - Required: ' ~ (check_mapping.required_config | join(', ')) ~ ' - Found: ' ~ ('Yes' if is_compliant else 'No'),
      'check_content': stig_item.Check_Content | default(''),
      'fix_text': stig_item.Fix_Text | default(''),
      'check_date': ansible_date_time.iso8601
    }] }}"
```

---

## Phase 4: Remediation & Reports (Week 4)

### Step 4.1: Create Main Playbooks

**Create: compliance-check.yml**

```yaml
---
- name: Cisco STIG Compliance Check
  hosts: all
  gather_facts: no
  vars:
    compliance_mode: "check_only"
    report_timestamp: "{{ lookup('pipe', 'date +%Y-%m-%d_%H-%M-%S') }}"
    report_dir: "{{ reports_dir }}/{{ report_timestamp }}"

  pre_tasks:
    - name: Create report directory
      file:
        path: "{{ report_dir }}/device_reports"
        state: directory
        mode: '0755'
      delegate_to: localhost
      run_once: yes

  roles:
    - role: stig_parser
      delegate_to: localhost
      run_once: yes

    - role: device_collector

    - role: compliance_checker

  post_tasks:
    - name: Create latest symlink
      file:
        src: "{{ report_dir }}"
        dest: "{{ reports_dir }}/latest"
        state: link
        force: yes
      delegate_to: localhost
      run_once: yes

- name: Generate Compliance Reports
  hosts: localhost
  gather_facts: no
  vars:
    report_timestamp: "{{ lookup('pipe', 'date +%Y-%m-%d_%H-%M-%S') }}"
    report_dir: "{{ reports_dir }}/{{ report_timestamp }}"

  roles:
    - role: report_generator

    - role: notification
      when: notification.enabled | default(false)
```

### Step 4.2: Implement report_generator Role

**Create: roles/report_generator/templates/device_report.html.j2**

```jinja2
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>STIG Compliance Report - {{ device_name }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: #2c3e50;
            color: white;
            padding: 20px;
            border-radius: 5px;
        }
        .score-box {
            display: inline-block;
            padding: 30px;
            margin: 20px;
            border-radius: 10px;
            text-align: center;
            min-width: 150px;
        }
        .compliant { background: #27ae60; color: white; }
        .partial { background: #f39c12; color: white; }
        .non-compliant { background: #e74c3c; color: white; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #34495e;
            color: white;
        }
        .finding {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 5px solid;
        }
        .cat1 { border-left-color: #e74c3c; }
        .cat2 { border-left-color: #f39c12; }
        .cat3 { border-left-color: #3498db; }
        .status-open { color: #e74c3c; font-weight: bold; }
        .status-closed { color: #27ae60; font-weight: bold; }
        pre {
            background: #ecf0f1;
            padding: 10px;
            border-radius: 3px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>STIG Compliance Report</h1>
        <h2>{{ device_name }}</h2>
        <p>Report Generated: {{ report_date }}</p>
        <p>STIG Version: {{ stig_version }}</p>
    </div>

    <div class="score-box {{ 'compliant' if compliance_score >= 90 else ('partial' if compliance_score >= 70 else 'non-compliant') }}">
        <h3>Overall Compliance</h3>
        <h1>{{ compliance_score }}%</h1>
    </div>

    <table>
        <tr>
            <th>Status</th>
            <th>Count</th>
            <th>Percentage</th>
        </tr>
        <tr>
            <td class="status-closed">Compliant</td>
            <td>{{ compliant_count }}</td>
            <td>{{ (compliant_count / total_checks * 100) | round(1) }}%</td>
        </tr>
        <tr>
            <td class="status-open">Non-Compliant</td>
            <td>{{ open_count }}</td>
            <td>{{ (open_count / total_checks * 100) | round(1) }}%</td>
        </tr>
    </table>

    <h2>Findings by Severity</h2>
    <table>
        <tr>
            <th>Severity</th>
            <th>Open</th>
            <th>Closed</th>
        </tr>
        <tr class="cat1">
            <td>CAT I (High)</td>
            <td>{{ cat1_open }}</td>
            <td>{{ cat1_closed }}</td>
        </tr>
        <tr class="cat2">
            <td>CAT II (Medium)</td>
            <td>{{ cat2_open }}</td>
            <td>{{ cat2_closed }}</td>
        </tr>
        <tr class="cat3">
            <td>CAT III (Low)</td>
            <td>{{ cat3_open }}</td>
            <td>{{ cat3_closed }}</td>
        </tr>
    </table>

    <h2>Detailed Findings</h2>
    {% for finding in findings | sort(attribute='severity') %}
    <div class="finding {{ finding.severity | lower }}">
        <h3>{{ finding.vuln_id }} - {{ finding.rule_title }}</h3>
        <p><strong>Severity:</strong> {{ finding.severity }}</p>
        <p><strong>Status:</strong> <span class="{{ 'status-open' if finding.status == 'Open' else 'status-closed' }}">{{ finding.status }}</span></p>
        <p><strong>Finding Details:</strong></p>
        <pre>{{ finding.finding_details }}</pre>
        {% if finding.status == 'Open' %}
        <p><strong>Remediation:</strong></p>
        <pre>{{ finding.fix_text }}</pre>
        {% endif %}
    </div>
    {% endfor %}
</body>
</html>
```

**Create: roles/report_generator/tasks/main.yml**

```yaml
---
- name: Prepare report data
  include_tasks: prepare_data.yml

- name: Generate device reports
  include_tasks: generate_device_report.yml
  loop: "{{ groups['all'] }}"
  loop_control:
    loop_var: device_name

- name: Generate inventory report
  include_tasks: generate_inventory_report.yml
```

---

## Phase 5: Scheduling & Operations (Week 5)

### Step 5.1: Create Scheduling Script

**Create: scripts/schedule_compliance_check.sh**

```bash
#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Configuration
SCHEDULE_TYPE="${1:-daily}"
ACTION="${2:-setup}"

# Setup cron job
setup_cron() {
    local schedule_type="$1"
    local cron_schedule=""

    case "$schedule_type" in
        daily)
            cron_schedule="0 2 * * *"
            ;;
        weekly)
            cron_schedule="0 2 * * 0"
            ;;
        monthly)
            cron_schedule="0 2 1 * *"
            ;;
    esac

    echo "Setting up $schedule_type cron job: $cron_schedule"

    # Add cron job
    (crontab -l 2>/dev/null; echo "$cron_schedule cd \"$PROJECT_DIR\" && ./scripts/run_compliance.sh $schedule_type") | crontab -
}

# Execute compliance check
run_check() {
    local schedule_type="$1"

    cd "$PROJECT_DIR"

    source venv/bin/activate

    ansible-playbook compliance-check.yml \
        -i inventory/production/hosts.yml \
        -e "schedule_type=$schedule_type"
}

case "$ACTION" in
    setup)
        setup_cron "$SCHEDULE_TYPE"
        ;;
    run)
        run_check "$SCHEDULE_TYPE"
        ;;
    *)
        echo "Usage: $0 {daily|weekly|monthly} {setup|run}"
        exit 1
        ;;
esac
```

Make executable:
```bash
chmod +x scripts/schedule_compliance_check.sh
```

### Step 5.2: Create Utility Scripts

**Create: scripts/cleanup_old_reports.py**

```python
#!/usr/bin/env python3
import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta
import argparse

def cleanup_reports(reports_dir, schedule_type, retention_days):
    schedule_dir = Path(reports_dir) / "scheduled" / schedule_type

    if not schedule_dir.exists():
        print(f"Directory not found: {schedule_dir}")
        return

    cutoff_date = datetime.now() - timedelta(days=retention_days)
    removed = 0

    for item in schedule_dir.iterdir():
        if item.is_dir() and item.name != "latest":
            try:
                dir_date = datetime.strptime(item.name, "%Y-%m-%d")
                if dir_date < cutoff_date:
                    print(f"Removing: {item}")
                    shutil.rmtree(item)
                    removed += 1
            except (ValueError, OSError) as e:
                print(f"Error processing {item}: {e}")

    print(f"Removed {removed} old reports")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reports-dir", required=True)
    parser.add_argument("--schedule-type", required=True)
    parser.add_argument("--retention-days", type=int, required=True)
    args = parser.parse_args()

    cleanup_reports(args.reports_dir, args.schedule_type, args.retention_days)
```

Make executable:
```bash
chmod +x scripts/cleanup_old_reports.py
```

---

## Phase 6: Testing & Validation (Week 6)

### Step 6.1: Create Test Fixtures

**Create: tests/fixtures/sample_configs/ios_switch_config.txt**

```
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
service password-encryption
!
hostname TestSwitch01
!
boot-start-marker
boot-end-marker
!
!
aaa new-model
!
aaa authentication login default group tacacs+ local
aaa authorization exec default group tacacs+ local
!
no ip domain-lookup
!
banner login ^C
*** AUTHORIZED USE ONLY ***
All activity is monitored and logged.
Unauthorized access is prohibited.
^C
!
line con 0
 exec-timeout 10 0
 logging synchronous
line vty 0 4
 exec-timeout 10 0
 transport input ssh
!
end
```

### Step 6.2: Create Test Playbook

**Create: tests/integration/test_compliance_check.yml**

```yaml
---
- name: Test Compliance Check Workflow
  hosts: localhost
  gather_facts: no
  tasks:
    - name: Run compliance check in dry-run mode
      command: ansible-playbook compliance-check.yml -i tests/fixtures/test_inventory.yml --check
      register: dry_run_result

    - name: Verify dry-run succeeded
      assert:
        that:
          - dry_run_result.rc == 0
        msg: "Dry-run compliance check failed"

    - name: Verify report directory structure
      stat:
        path: "{{ item }}"
      loop:
        - reports
        - backups
        - logs
      register: dir_check

    - name: Verify all directories exist
      assert:
        that:
          - item.stat.exists
        msg: "Required directory missing"
      loop: "{{ dir_check.results }}"
```

### Step 6.3: Run Tests

```bash
# Run unit tests
pytest tests/unit/

# Run integration tests (requires test environment)
ansible-playbook tests/integration/test_compliance_check.yml

# Validate inventory
python scripts/validate_inventory.py --inventory inventory/production/hosts.yml

# Test CKL parser
python -m pytest tests/unit/test_ckl_parser.py -v
```

---

## Post-Implementation Checklist

### Configuration Validation

- [ ] Ansible configuration tested and working
- [ ] Python dependencies installed
- [ ] Ansible collections installed
- [ ] Inventory file populated with devices
- [ ] Vault file created with credentials
- [ ] STIG checklists placed in correct directory

### Functional Testing

- [ ] CKL parser successfully parses STIG files
- [ ] Device collector can connect to test device
- [ ] Compliance checks execute successfully
- [ ] Reports generate correctly (HTML + JSON)
- [ ] Backup functionality works
- [ ] Notifications send (if configured)

### Operational Readiness

- [ ] Scheduled jobs configured
- [ ] Cleanup scripts tested
- [ ] Documentation reviewed
- [ ] Team trained on usage
- [ ] Runbooks created
- [ ] Support process defined

---

## Common Implementation Issues

### Issue 1: Connection Timeouts

**Symptom**: Ansible fails to connect to devices

**Solution**:
```yaml
# Increase timeouts in ansible.cfg
[persistent_connection]
connect_timeout = 120
command_timeout = 120
```

### Issue 2: CKL Parsing Errors

**Symptom**: XML parsing fails

**Solution**:
1. Validate XML structure: `xmllint --noout stig_checklists/current/*.ckl`
2. Check file encoding (should be UTF-8)
3. Verify no special characters in XML

### Issue 3: Report Generation Fails

**Symptom**: HTML reports not generated

**Solution**:
```bash
# Install missing Python dependencies
pip install jinja2 lxml

# Verify template syntax
ansible-playbook --syntax-check compliance-check.yml
```

### Issue 4: Permission Denied

**Symptom**: Cannot write to reports directory

**Solution**:
```bash
# Fix permissions
chmod -R 755 reports/
chmod -R 755 logs/
chmod -R 755 backups/
```

---

## Next Steps After Implementation

1. **Baseline Compliance**: Run initial compliance check across all devices
2. **Review Findings**: Analyze results and prioritize remediation
3. **Test Remediation**: Test remediation on lab devices first
4. **Production Remediation**: Apply fixes to production (with approval)
5. **Monitor**: Set up regular scheduled checks
6. **Maintain**: Keep STIG checklists updated

---

## Support Resources

- **Documentation**: See `docs/` directory
- **Examples**: See `docs/examples/`
- **Logs**: Check `logs/ansible.log`
- **STIG Resources**: https://public.cyber.mil/stigs/

---

**Document Version**: 1.0.0
**Last Updated**: 2026-01-09
