#!/usr/bin/env python3
"""
Custom Ansible filter plugins for STIG compliance automation.
These filters help process and analyze STIG compliance data.
"""

import re
from datetime import datetime


class FilterModule:
    """Custom filter plugins for STIG compliance"""

    def filters(self):
        return {
            'extract_config_lines': self.extract_config_lines,
            'check_config_present': self.check_config_present,
            'check_config_absent': self.check_config_absent,
            'normalize_config': self.normalize_config,
            'get_compliance_status': self.get_compliance_status,
            'filter_by_severity': self.filter_by_severity,
            'calculate_compliance_score': self.calculate_compliance_score,
            'extract_ios_commands': self.extract_ios_commands,
            'parse_show_output': self.parse_show_output,
            'config_diff': self.config_diff,
            'severity_to_number': self.severity_to_number,
            'number_to_severity': self.number_to_severity,
            'format_compliance_report': self.format_compliance_report,
            'group_by_severity': self.group_by_severity,
            'get_noncompliant_items': self.get_noncompliant_items,
            'merge_compliance_results': self.merge_compliance_results
        }

    def extract_config_lines(self, config_text, pattern=None, section=None):
        """
        Extract configuration lines from show running-config output.

        Args:
            config_text: Full configuration text
            pattern: Regex pattern to match lines (optional)
            section: Section name to extract (e.g., 'aaa', 'line vty')

        Returns:
            List of matching configuration lines
        """
        if not config_text:
            return []

        lines = config_text.split('\n')
        result = []

        if section:
            # Extract entire section
            in_section = False
            section_pattern = re.compile(rf'^{re.escape(section)}', re.IGNORECASE)

            for line in lines:
                if section_pattern.match(line):
                    in_section = True
                    result.append(line)
                elif in_section:
                    if line.startswith(' ') or line.startswith('\t'):
                        result.append(line)
                    elif line.strip() == '!':
                        result.append(line)
                        in_section = False
                    else:
                        in_section = False

        elif pattern:
            # Match by pattern
            regex = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
            for line in lines:
                if regex.search(line):
                    result.append(line.strip())

        else:
            # Return all non-empty, non-comment lines
            result = [l.strip() for l in lines if l.strip() and not l.strip().startswith('!')]

        return result

    def check_config_present(self, config_text, expected_configs):
        """
        Check if expected configuration lines are present.

        Args:
            config_text: Full configuration text
            expected_configs: List of config lines that should be present

        Returns:
            Dict with 'compliant', 'missing', and 'found' lists
        """
        if not config_text:
            return {
                'compliant': False,
                'missing': expected_configs,
                'found': []
            }

        config_lower = config_text.lower()
        missing = []
        found = []

        for expected in expected_configs:
            expected_normalized = self._normalize_config_line(expected)
            config_normalized = self._normalize_config_line(config_text)

            # Check if the config exists (case-insensitive, whitespace-normalized)
            if expected_normalized.lower() in config_normalized.lower():
                found.append(expected)
            else:
                # Try regex match for more flexible matching
                pattern = re.escape(expected.strip()).replace(r'\ +', r'\s+')
                if re.search(pattern, config_text, re.IGNORECASE | re.MULTILINE):
                    found.append(expected)
                else:
                    missing.append(expected)

        return {
            'compliant': len(missing) == 0,
            'missing': missing,
            'found': found
        }

    def check_config_absent(self, config_text, prohibited_configs):
        """
        Check if prohibited configuration lines are absent.

        Args:
            config_text: Full configuration text
            prohibited_configs: List of config lines that should NOT be present

        Returns:
            Dict with 'compliant', 'violations', and 'clean' lists
        """
        if not config_text:
            return {
                'compliant': True,
                'violations': [],
                'clean': prohibited_configs
            }

        violations = []
        clean = []

        for prohibited in prohibited_configs:
            # Handle "no X" patterns - check if X exists without "no"
            if prohibited.lower().startswith('no '):
                # Looking for absence of "no X", which means X should not exist
                base_config = prohibited[3:].strip()
                pattern = rf'^(?!no\s+){re.escape(base_config)}'
                if re.search(pattern, config_text, re.IGNORECASE | re.MULTILINE):
                    violations.append(f"Found '{base_config}' (should have 'no' prefix)")
                else:
                    clean.append(prohibited)
            else:
                # Looking for exact match to be absent
                pattern = re.escape(prohibited.strip()).replace(r'\ +', r'\s+')
                if re.search(pattern, config_text, re.IGNORECASE | re.MULTILINE):
                    violations.append(prohibited)
                else:
                    clean.append(prohibited)

        return {
            'compliant': len(violations) == 0,
            'violations': violations,
            'clean': clean
        }

    def normalize_config(self, config_text):
        """
        Normalize configuration text for comparison.
        - Remove extra whitespace
        - Remove comments
        - Standardize line endings
        """
        if not config_text:
            return ''

        lines = config_text.split('\n')
        normalized = []

        for line in lines:
            # Skip empty lines and comments
            line = line.rstrip()
            if not line or line.strip().startswith('!'):
                continue

            # Normalize whitespace (but preserve leading spaces for hierarchy)
            leading_spaces = len(line) - len(line.lstrip())
            content = ' '.join(line.split())
            normalized.append(' ' * leading_spaces + content)

        return '\n'.join(normalized)

    def _normalize_config_line(self, line):
        """Normalize a single config line for comparison"""
        return ' '.join(line.split())

    def get_compliance_status(self, check_results):
        """
        Determine overall compliance status from multiple check results.

        Args:
            check_results: List of check result dicts with 'compliant' key

        Returns:
            'compliant', 'non_compliant', or 'partial'
        """
        if not check_results:
            return 'unknown'

        compliant_count = sum(1 for r in check_results if r.get('compliant', False))
        total = len(check_results)

        if compliant_count == total:
            return 'compliant'
        elif compliant_count == 0:
            return 'non_compliant'
        else:
            return 'partial'

    def filter_by_severity(self, items, severities, key='severity'):
        """
        Filter items by severity level.

        Args:
            items: List of dicts containing severity info
            severities: List of severities to include (e.g., ['CAT_I', 'CAT_II'])
            key: Key name for severity field

        Returns:
            Filtered list of items
        """
        if not severities:
            return items

        # Normalize severity values
        normalized = []
        for s in severities:
            s_upper = s.upper().replace(' ', '_')
            if s_upper in ['CAT_I', 'HIGH', 'I', '1']:
                normalized.append('CAT_I')
            elif s_upper in ['CAT_II', 'MEDIUM', 'II', '2']:
                normalized.append('CAT_II')
            elif s_upper in ['CAT_III', 'LOW', 'III', '3']:
                normalized.append('CAT_III')

        return [item for item in items if item.get(key, '').upper() in normalized]

    def calculate_compliance_score(self, results, weighted=True):
        """
        Calculate compliance score from results.

        Args:
            results: List of compliance check results
            weighted: If True, weight by severity (CAT_I=3, CAT_II=2, CAT_III=1)

        Returns:
            Dict with score, percentage, and breakdown
        """
        if not results:
            return {
                'score': 0,
                'max_score': 0,
                'percentage': 0.0,
                'breakdown': {}
            }

        weights = {'CAT_I': 3, 'CAT_II': 2, 'CAT_III': 1}

        total_score = 0
        max_score = 0
        breakdown = {
            'CAT_I': {'compliant': 0, 'total': 0},
            'CAT_II': {'compliant': 0, 'total': 0},
            'CAT_III': {'compliant': 0, 'total': 0}
        }

        for result in results:
            severity = result.get('severity', 'CAT_III')
            compliant = result.get('compliant', False)
            weight = weights.get(severity, 1) if weighted else 1

            max_score += weight
            if severity in breakdown:
                breakdown[severity]['total'] += 1

            if compliant:
                total_score += weight
                if severity in breakdown:
                    breakdown[severity]['compliant'] += 1

        percentage = (total_score / max_score * 100) if max_score > 0 else 0

        return {
            'score': total_score,
            'max_score': max_score,
            'percentage': round(percentage, 2),
            'breakdown': breakdown
        }

    def extract_ios_commands(self, text):
        """
        Extract Cisco IOS commands from text (fix text, check content, etc.)

        Args:
            text: Text containing potential IOS commands

        Returns:
            List of extracted commands
        """
        if not text:
            return []

        commands = []
        command_starters = [
            'aaa', 'access-', 'banner', 'boot', 'cdp', 'class-map',
            'clock', 'crypto', 'enable', 'hostname', 'interface',
            'ip', 'ipv6', 'line', 'logging', 'login', 'mls', 'no',
            'ntp', 'policy-map', 'router', 'service', 'snmp', 'spanning-tree',
            'ssh', 'tacacs', 'transport', 'username', 'vlan', 'vty'
        ]

        for line in text.split('\n'):
            line = line.strip()

            # Skip empty lines and obvious non-commands
            if not line or len(line) < 3:
                continue

            # Check if line starts with a known command
            first_word = line.split()[0].lower() if line.split() else ''

            if first_word in command_starters or first_word.startswith('no '):
                # Clean up the command
                cmd = line.strip()
                # Remove leading bullets or numbers
                cmd = re.sub(r'^[\d\.\)\-\*]+\s*', '', cmd)
                if cmd and len(cmd) > 3:
                    commands.append(cmd)

        return list(dict.fromkeys(commands))  # Remove duplicates

    def parse_show_output(self, output, output_type='generic'):
        """
        Parse common 'show' command output into structured data.

        Args:
            output: Raw command output string
            output_type: Type of output ('interfaces', 'version', 'ntp', 'aaa', 'generic')

        Returns:
            Parsed structured data
        """
        if not output:
            return {}

        if output_type == 'interfaces':
            return self._parse_interfaces(output)
        elif output_type == 'version':
            return self._parse_version(output)
        elif output_type == 'ntp':
            return self._parse_ntp(output)
        else:
            return {'raw': output}

    def _parse_interfaces(self, output):
        """Parse show ip interface brief output"""
        interfaces = []
        for line in output.split('\n')[1:]:  # Skip header
            parts = line.split()
            if len(parts) >= 6:
                interfaces.append({
                    'name': parts[0],
                    'ip_address': parts[1],
                    'ok': parts[2],
                    'method': parts[3],
                    'status': parts[4],
                    'protocol': parts[5]
                })
        return {'interfaces': interfaces}

    def _parse_version(self, output):
        """Parse show version output"""
        result = {}

        version_match = re.search(r'Version (\S+)', output)
        if version_match:
            result['version'] = version_match.group(1)

        model_match = re.search(r'cisco (\S+)', output, re.IGNORECASE)
        if model_match:
            result['model'] = model_match.group(1)

        uptime_match = re.search(r'uptime is (.+)', output, re.IGNORECASE)
        if uptime_match:
            result['uptime'] = uptime_match.group(1).strip()

        return result

    def _parse_ntp(self, output):
        """Parse show ntp associations output"""
        associations = []
        for line in output.split('\n'):
            if line.strip() and not line.startswith('address'):
                parts = line.split()
                if len(parts) >= 4:
                    associations.append({
                        'address': parts[0].lstrip('*~#+-'),
                        'ref_clock': parts[1] if len(parts) > 1 else '',
                        'stratum': parts[2] if len(parts) > 2 else ''
                    })
        return {'associations': associations}

    def config_diff(self, current_config, desired_config):
        """
        Generate diff between current and desired configuration.

        Returns:
            Dict with 'add', 'remove', and 'modify' lists
        """
        current_lines = set(self.normalize_config(current_config).split('\n'))
        desired_lines = set(self.normalize_config(desired_config).split('\n'))

        return {
            'add': list(desired_lines - current_lines),
            'remove': list(current_lines - desired_lines),
            'unchanged': list(current_lines & desired_lines)
        }

    def severity_to_number(self, severity):
        """Convert severity category to number (for sorting)"""
        mapping = {'CAT_I': 1, 'CAT_II': 2, 'CAT_III': 3}
        return mapping.get(severity.upper().replace(' ', '_'), 99)

    def number_to_severity(self, number):
        """Convert number to severity category"""
        mapping = {1: 'CAT_I', 2: 'CAT_II', 3: 'CAT_III'}
        return mapping.get(number, 'UNKNOWN')

    def format_compliance_report(self, results, format_type='summary'):
        """
        Format compliance results for reporting.

        Args:
            results: Compliance check results
            format_type: 'summary', 'detailed', or 'csv'

        Returns:
            Formatted string
        """
        if not results:
            return "No results to report"

        if format_type == 'summary':
            score = self.calculate_compliance_score(results)
            lines = [
                f"Compliance Score: {score['percentage']}%",
                f"Total Checks: {len(results)}",
                f"CAT I: {score['breakdown']['CAT_I']['compliant']}/{score['breakdown']['CAT_I']['total']}",
                f"CAT II: {score['breakdown']['CAT_II']['compliant']}/{score['breakdown']['CAT_II']['total']}",
                f"CAT III: {score['breakdown']['CAT_III']['compliant']}/{score['breakdown']['CAT_III']['total']}"
            ]
            return '\n'.join(lines)

        elif format_type == 'csv':
            lines = ['severity,stig_id,title,compliant']
            for r in results:
                lines.append(f"{r.get('severity','')},{r.get('stig_id','')},{r.get('title','')},{r.get('compliant','')}")
            return '\n'.join(lines)

        else:
            return str(results)

    def group_by_severity(self, items, key='severity'):
        """Group items by severity level"""
        grouped = {'CAT_I': [], 'CAT_II': [], 'CAT_III': [], 'OTHER': []}

        for item in items:
            severity = item.get(key, 'OTHER').upper().replace(' ', '_')
            if severity in grouped:
                grouped[severity].append(item)
            else:
                grouped['OTHER'].append(item)

        return grouped

    def get_noncompliant_items(self, results):
        """Extract only non-compliant items from results"""
        return [r for r in results if not r.get('compliant', True)]

    def merge_compliance_results(self, *result_lists):
        """Merge multiple compliance result lists, avoiding duplicates by STIG ID"""
        seen = set()
        merged = []

        for result_list in result_lists:
            if not result_list:
                continue
            for item in result_list:
                stig_id = item.get('stig_id', item.get('vuln_id', ''))
                if stig_id and stig_id not in seen:
                    seen.add(stig_id)
                    merged.append(item)

        return merged
