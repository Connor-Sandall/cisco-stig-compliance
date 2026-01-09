#!/usr/bin/env python3
"""
Ansible Module: ckl_parser
Parse STIG Checklist (.ckl) files and extract compliance rules.

CKL files are XML-based STIG Viewer checklists containing:
- STIG metadata (title, version, release)
- Individual vulnerability checks (VULN elements)
- Status information (Open, NotAFinding, Not_Applicable)

Usage in playbook:
  - name: Parse STIG checklist
    ckl_parser:
      src: /path/to/checklist.ckl
      output_format: yaml
    register: stig_rules
"""

from ansible.module_utils.basic import AnsibleModule
import xml.etree.ElementTree as ET
import json
import yaml
import re
import os

DOCUMENTATION = r'''
---
module: ckl_parser
short_description: Parse STIG Checklist (.ckl) files
description:
    - Parses DISA STIG Viewer checklist files (.ckl)
    - Extracts vulnerability IDs, check content, and fix text
    - Supports filtering by severity category
    - Outputs structured data for compliance automation
version_added: "1.0.0"
author:
    - "Cisco STIG Compliance Automation"
options:
    src:
        description:
            - Path to the .ckl file to parse
        type: path
        required: true
    output_format:
        description:
            - Output format for parsed rules
        type: str
        choices: ['dict', 'yaml', 'json']
        default: 'dict'
    severity_filter:
        description:
            - Filter results by severity (CAT_I, CAT_II, CAT_III)
            - If not specified, returns all severities
        type: list
        elements: str
        default: []
    extract_fix_commands:
        description:
            - Attempt to extract CLI commands from fix text
        type: bool
        default: true
'''

EXAMPLES = r'''
- name: Parse STIG checklist
  ckl_parser:
    src: /path/to/Cisco_IOS_STIG.ckl
  register: stig_data

- name: Parse only CAT I findings
  ckl_parser:
    src: /path/to/checklist.ckl
    severity_filter:
      - CAT_I
  register: critical_stigs

- name: Parse and extract fix commands
  ckl_parser:
    src: /path/to/checklist.ckl
    extract_fix_commands: true
  register: stig_with_commands
'''

RETURN = r'''
stig_info:
    description: STIG metadata
    type: dict
    returned: always
    sample:
        title: "Cisco IOS XE Router RTR STIG"
        version: "2"
        release: "3"
vulns:
    description: List of vulnerability checks
    type: list
    returned: always
    sample:
        - vuln_id: "V-220518"
          rule_id: "SV-220518r879887_rule"
          stig_id: "CISC-RT-000010"
          severity: "CAT_I"
          title: "AAA must be enabled"
          check_content: "Verify AAA is configured..."
          fix_text: "Configure AAA authentication..."
          fix_commands: ["aaa new-model"]
summary:
    description: Summary statistics
    type: dict
    returned: always
    sample:
        total_vulns: 150
        cat_i_count: 25
        cat_ii_count: 100
        cat_iii_count: 25
'''


class CKLParser:
    """Parser for DISA STIG Viewer .ckl files"""

    # Mapping of severity values to categories
    SEVERITY_MAP = {
        'high': 'CAT_I',
        'medium': 'CAT_II',
        'low': 'CAT_III',
        'cat_i': 'CAT_I',
        'cat_ii': 'CAT_II',
        'cat_iii': 'CAT_III',
        'i': 'CAT_I',
        'ii': 'CAT_II',
        'iii': 'CAT_III',
        '1': 'CAT_I',
        '2': 'CAT_II',
        '3': 'CAT_III'
    }

    # Common Cisco IOS command patterns for extraction
    COMMAND_PATTERNS = [
        r'^\s*(no\s+)?[a-z][\w\-]+(\s+[\w\-./]+)*\s*$',  # Basic commands
        r'^\s*(interface|line|router|aaa|ip|snmp|logging|ntp|banner|service)\s+.*$',
        r'^\s*(enable\s+secret|username|crypto|access-list)\s+.*$'
    ]

    def __init__(self, ckl_path):
        self.ckl_path = ckl_path
        self.tree = None
        self.root = None
        self.stig_info = {}
        self.vulns = []

    def parse(self):
        """Parse the CKL file and extract all vulnerability data"""
        try:
            self.tree = ET.parse(self.ckl_path)
            self.root = self.tree.getroot()
        except ET.ParseError as e:
            raise ValueError(f"Failed to parse CKL file: {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"CKL file not found: {self.ckl_path}")

        self._extract_stig_info()
        self._extract_vulns()

        return {
            'stig_info': self.stig_info,
            'vulns': self.vulns,
            'summary': self._generate_summary()
        }

    def _extract_stig_info(self):
        """Extract STIG metadata from the checklist"""
        # Try to find STIG_INFO element
        stig_info_elem = self.root.find('.//STIG_INFO')

        if stig_info_elem is not None:
            for si_data in stig_info_elem.findall('SI_DATA'):
                sid_name = si_data.find('SID_NAME')
                sid_data = si_data.find('SID_DATA')

                if sid_name is not None and sid_name.text:
                    name = sid_name.text.lower().replace(' ', '_')
                    value = sid_data.text if sid_data is not None else ''
                    self.stig_info[name] = value

        # Also try alternate locations
        if not self.stig_info:
            # Try to extract from iSTIG
            istig = self.root.find('.//iSTIG')
            if istig is not None:
                stig_info = istig.find('STIG_INFO')
                if stig_info is not None:
                    for si_data in stig_info.findall('SI_DATA'):
                        sid_name = si_data.find('SID_NAME')
                        sid_data = si_data.find('SID_DATA')
                        if sid_name is not None and sid_name.text:
                            name = sid_name.text.lower().replace(' ', '_')
                            value = sid_data.text if sid_data is not None else ''
                            self.stig_info[name] = value

    def _extract_vulns(self):
        """Extract all vulnerability entries from the checklist"""
        # Find all VULN elements
        for vuln in self.root.findall('.//VULN'):
            vuln_data = self._parse_vuln(vuln)
            if vuln_data:
                self.vulns.append(vuln_data)

    def _parse_vuln(self, vuln_elem):
        """Parse a single VULN element"""
        vuln_data = {
            'vuln_id': '',
            'rule_id': '',
            'stig_id': '',
            'severity': '',
            'title': '',
            'description': '',
            'check_content': '',
            'fix_text': '',
            'fix_commands': [],
            'status': '',
            'comments': '',
            'finding_details': ''
        }

        # Extract STIG_DATA elements
        for stig_data in vuln_elem.findall('STIG_DATA'):
            vuln_attribute = stig_data.find('VULN_ATTRIBUTE')
            attribute_data = stig_data.find('ATTRIBUTE_DATA')

            if vuln_attribute is None or vuln_attribute.text is None:
                continue

            attr_name = vuln_attribute.text.lower()
            attr_value = attribute_data.text if attribute_data is not None else ''

            # Map the attribute to our data structure
            if attr_name == 'vuln_num':
                vuln_data['vuln_id'] = attr_value
            elif attr_name == 'rule_id':
                vuln_data['rule_id'] = attr_value
            elif attr_name == 'rule_ver' or attr_name == 'stig_id':
                vuln_data['stig_id'] = attr_value
            elif attr_name == 'severity':
                vuln_data['severity'] = self._normalize_severity(attr_value)
            elif attr_name == 'rule_title':
                vuln_data['title'] = attr_value
            elif attr_name == 'vuln_discuss' or attr_name == 'discussion':
                vuln_data['description'] = attr_value
            elif attr_name == 'check_content':
                vuln_data['check_content'] = attr_value
            elif attr_name == 'fix_text':
                vuln_data['fix_text'] = attr_value

        # Extract STATUS
        status_elem = vuln_elem.find('STATUS')
        if status_elem is not None and status_elem.text:
            vuln_data['status'] = status_elem.text

        # Extract COMMENTS
        comments_elem = vuln_elem.find('COMMENTS')
        if comments_elem is not None and comments_elem.text:
            vuln_data['comments'] = comments_elem.text

        # Extract FINDING_DETAILS
        finding_elem = vuln_elem.find('FINDING_DETAILS')
        if finding_elem is not None and finding_elem.text:
            vuln_data['finding_details'] = finding_elem.text

        return vuln_data

    def _normalize_severity(self, severity):
        """Normalize severity value to CAT_I/II/III format"""
        if not severity:
            return 'CAT_III'

        severity_lower = severity.lower().strip()
        return self.SEVERITY_MAP.get(severity_lower, 'CAT_III')

    def extract_fix_commands(self, fix_text):
        """Extract potential CLI commands from fix text"""
        if not fix_text:
            return []

        commands = []
        lines = fix_text.split('\n')

        for line in lines:
            line = line.strip()

            # Skip empty lines and common non-command text
            if not line:
                continue
            if line.startswith('#') or line.startswith('!'):
                continue
            if any(line.lower().startswith(x) for x in ['note:', 'example:', 'verify', 'check', 'ensure']):
                continue

            # Check against command patterns
            for pattern in self.COMMAND_PATTERNS:
                if re.match(pattern, line, re.IGNORECASE):
                    # Clean up the command
                    cmd = line.strip()
                    if cmd and len(cmd) > 3:
                        commands.append(cmd)
                    break

        return list(dict.fromkeys(commands))  # Remove duplicates while preserving order

    def _generate_summary(self):
        """Generate summary statistics"""
        summary = {
            'total_vulns': len(self.vulns),
            'cat_i_count': 0,
            'cat_ii_count': 0,
            'cat_iii_count': 0,
            'by_status': {},
            'stig_title': self.stig_info.get('title', 'Unknown'),
            'stig_version': self.stig_info.get('version', 'Unknown'),
            'stig_release': self.stig_info.get('releaseinfo', 'Unknown')
        }

        for vuln in self.vulns:
            severity = vuln.get('severity', '')
            status = vuln.get('status', 'Not_Reviewed')

            if severity == 'CAT_I':
                summary['cat_i_count'] += 1
            elif severity == 'CAT_II':
                summary['cat_ii_count'] += 1
            elif severity == 'CAT_III':
                summary['cat_iii_count'] += 1

            summary['by_status'][status] = summary['by_status'].get(status, 0) + 1

        return summary


def parse_text_config_rules(file_path):
    """
    Parse a text/YAML file containing configuration rules.

    Expected format (YAML):
    ---
    rules:
      - id: "CUSTOM-001"
        severity: "CAT_II"
        title: "Enable SSH version 2"
        check_type: "present"  # present or absent
        config_lines:
          - "ip ssh version 2"
        fix_commands:
          - "ip ssh version 2"

    Or simple text format (one config per line):
    # Comment - severity: CAT_I
    ip ssh version 2
    aaa new-model
    no ip http server
    """

    rules = []

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config rules file not found: {file_path}")

    with open(file_path, 'r') as f:
        content = f.read()

    # Try YAML format first
    try:
        data = yaml.safe_load(content)
        if data and 'rules' in data:
            return data['rules']
    except yaml.YAMLError:
        pass

    # Fall back to simple text format
    current_severity = 'CAT_II'
    rule_id = 1

    for line in content.split('\n'):
        line = line.strip()

        if not line:
            continue

        # Check for severity marker
        if line.startswith('#'):
            if 'CAT_I' in line.upper() or 'CAT I' in line.upper():
                current_severity = 'CAT_I'
            elif 'CAT_II' in line.upper() or 'CAT II' in line.upper():
                current_severity = 'CAT_II'
            elif 'CAT_III' in line.upper() or 'CAT III' in line.upper():
                current_severity = 'CAT_III'
            continue

        # Determine if this is a "no" command (config should be absent)
        check_type = 'absent' if line.lower().startswith('no ') else 'present'

        rules.append({
            'id': f'CUSTOM-{rule_id:04d}',
            'severity': current_severity,
            'title': f'Config: {line[:50]}',
            'check_type': check_type,
            'config_lines': [line],
            'fix_commands': [line]
        })
        rule_id += 1

    return rules


def main():
    module_args = dict(
        src=dict(type='path', required=True),
        output_format=dict(type='str', choices=['dict', 'yaml', 'json'], default='dict'),
        severity_filter=dict(type='list', elements='str', default=[]),
        extract_fix_commands=dict(type='bool', default=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    src = module.params['src']
    output_format = module.params['output_format']
    severity_filter = module.params['severity_filter']
    extract_commands = module.params['extract_fix_commands']

    result = dict(
        changed=False,
        stig_info={},
        vulns=[],
        summary={},
        rules_from_text=[]
    )

    try:
        # Determine file type and parse accordingly
        if src.lower().endswith('.ckl'):
            parser = CKLParser(src)
            parsed_data = parser.parse()

            result['stig_info'] = parsed_data['stig_info']
            result['vulns'] = parsed_data['vulns']
            result['summary'] = parsed_data['summary']

            # Extract fix commands if requested
            if extract_commands:
                for vuln in result['vulns']:
                    vuln['fix_commands'] = parser.extract_fix_commands(vuln.get('fix_text', ''))

            # Apply severity filter
            if severity_filter:
                normalized_filter = [CKLParser.SEVERITY_MAP.get(s.lower(), s.upper()) for s in severity_filter]
                result['vulns'] = [v for v in result['vulns'] if v.get('severity') in normalized_filter]

                # Update summary counts
                result['summary']['filtered_count'] = len(result['vulns'])

        elif src.lower().endswith(('.yml', '.yaml', '.txt')):
            rules = parse_text_config_rules(src)

            # Apply severity filter
            if severity_filter:
                normalized_filter = [CKLParser.SEVERITY_MAP.get(s.lower(), s.upper()) for s in severity_filter]
                rules = [r for r in rules if r.get('severity') in normalized_filter]

            result['rules_from_text'] = rules
            result['summary'] = {
                'total_rules': len(rules),
                'source_type': 'text_config'
            }

        else:
            module.fail_json(msg=f"Unsupported file format. Expected .ckl, .yml, .yaml, or .txt: {src}")

        # Format output
        if output_format == 'json':
            result['formatted_output'] = json.dumps(result, indent=2)
        elif output_format == 'yaml':
            result['formatted_output'] = yaml.dump(result, default_flow_style=False)

    except Exception as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
