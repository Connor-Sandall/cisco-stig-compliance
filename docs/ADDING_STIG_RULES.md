# Adding Custom STIG Rules

This guide explains how to add custom STIG compliance rules to the automation tool.

## Option 1: YAML Configuration File

The easiest way to add custom rules is using the YAML format in `stig_checklists/current/config_rules.yml`.

### Rule Structure

```yaml
rules:
  - id: "CUSTOM-001"              # Unique identifier
    stig_id: "CUSTOM-001"         # STIG reference ID
    severity: "CAT_II"            # CAT_I, CAT_II, or CAT_III
    title: "Short description"    # Display title
    description: "Detailed description of the requirement"
    check_type: present           # "present" or "absent"
    config_lines:                 # Configuration to check for
      - "ip ssh version 2"
    check_regex: "pattern"        # Optional: regex for complex matching
    fix_commands:                 # Commands to remediate
      - "ip ssh version 2"
```

### Check Types

#### `present` - Configuration Should Exist

```yaml
- id: "RULE-001"
  severity: "CAT_II"
  title: "SSH version 2 required"
  check_type: present
  config_lines:
    - "ip ssh version 2"
  fix_commands:
    - "ip ssh version 2"
```

#### `absent` - Configuration Should NOT Exist

```yaml
- id: "RULE-002"
  severity: "CAT_II"
  title: "HTTP server must be disabled"
  check_type: absent
  config_lines:
    - "ip http server"
  fix_commands:
    - "no ip http server"
```

### Using Regex Patterns

For complex checks, use `check_regex`:

```yaml
- id: "RULE-003"
  severity: "CAT_I"
  title: "Enable secret must use strong encryption"
  check_type: present
  config_lines:
    - "enable secret"
  check_regex: "enable secret [5-9]"  # Types 5-9 are strong
  fix_commands:
    - "enable algorithm-type scrypt secret <PASSWORD>"
```

### Multiple Configuration Lines

```yaml
- id: "RULE-004"
  severity: "CAT_II"
  title: "TCP keepalives must be enabled"
  check_type: present
  config_lines:
    - "service tcp-keepalives-in"
    - "service tcp-keepalives-out"
  fix_commands:
    - "service tcp-keepalives-in"
    - "service tcp-keepalives-out"
```

## Option 2: Simple Text File

For quick rule creation, use a simple text file format:

```text
# CAT I - Critical
aaa new-model
ip ssh version 2
enable secret

# CAT II - Medium
service password-encryption
no ip http server
no ip source-route

# CAT III - Low
banner login
logging buffered
```

Lines starting with `#` define severity. Each subsequent line is a configuration rule.

## Option 3: STIG ID Mapping

For official STIG IDs, add mappings to `roles/stig_parser/vars/stig_config_mapping.yml`:

```yaml
mappings:
  CISC-ND-001234:
    category: ssh
    check_type: present
    check_command: "show running-config | include ip ssh"
    expected_config:
      - "ip ssh version 2"
    fix_commands:
      - "ip ssh version 2"
```

### Mapping Structure

| Field | Description |
|-------|-------------|
| `category` | Grouping for reports (aaa, ssh, ntp, etc.) |
| `check_type` | `present` or `absent` |
| `check_command` | Show command to run |
| `expected_config` | Config lines that should exist |
| `prohibited_config` | Config lines that should NOT exist |
| `fix_commands` | Commands to remediate |
| `check_regex` | Optional regex pattern |

## Examples by Category

### AAA Configuration

```yaml
- id: "AAA-001"
  severity: "CAT_I"
  title: "AAA must be enabled"
  check_type: present
  config_lines:
    - "aaa new-model"
  fix_commands:
    - "aaa new-model"

- id: "AAA-002"
  severity: "CAT_I"
  title: "Login authentication must be configured"
  check_type: present
  check_regex: "aaa authentication login .+ (group tacacs|group radius|local)"
  config_lines:
    - "aaa authentication login"
  fix_commands:
    - "aaa authentication login default group tacacs+ local"
```

### SSH Configuration

```yaml
- id: "SSH-001"
  severity: "CAT_I"
  title: "SSH version 2 only"
  check_type: present
  config_lines:
    - "ip ssh version 2"
  fix_commands:
    - "ip ssh version 2"

- id: "SSH-002"
  severity: "CAT_II"
  title: "SSH timeout must be configured"
  check_type: present
  check_regex: "ip ssh time-out [1-9][0-9]?"
  config_lines:
    - "ip ssh time-out"
  fix_commands:
    - "ip ssh time-out 60"
```

### Service Hardening

```yaml
- id: "SVC-001"
  severity: "CAT_II"
  title: "HTTP server must be disabled"
  check_type: absent
  config_lines:
    - "ip http server"
  fix_commands:
    - "no ip http server"
    - "no ip http secure-server"

- id: "SVC-002"
  severity: "CAT_II"
  title: "Source routing must be disabled"
  check_type: absent
  check_regex: "^ip source-route$"
  config_lines:
    - "ip source-route"
  fix_commands:
    - "no ip source-route"
```

### SNMP Security

```yaml
- id: "SNMP-001"
  severity: "CAT_I"
  title: "SNMPv1/v2 communities must be removed"
  check_type: absent
  config_lines:
    - "snmp-server community"
  fix_commands:
    - "no snmp-server community public"
    - "no snmp-server community private"

- id: "SNMP-002"
  severity: "CAT_II"
  title: "SNMPv3 must be configured"
  check_type: present
  check_regex: "snmp-server group .+ v3 (priv|auth)"
  config_lines:
    - "snmp-server group"
  fix_commands:
    - "snmp-server group SNMPV3_GROUP v3 priv"
```

## Testing New Rules

1. Add your rules to the config file
2. Run a compliance check in dry-run mode:

```bash
ansible-playbook playbooks/compliance_check.yml \
  -e "stig_checklist_file=stig_checklists/current/config_rules.yml" \
  --limit test_device
```

3. Review the generated report
4. Test remediation in dry-run mode:

```bash
ansible-playbook playbooks/remediation.yml \
  -e "dry_run=true" \
  --limit test_device
```

## Best Practices

1. **Use Unique IDs**: Each rule needs a unique identifier
2. **Set Appropriate Severity**: CAT_I for critical, CAT_II for medium, CAT_III for low
3. **Test Regex Patterns**: Verify regex matches expected configurations
4. **Include Fix Commands**: Always provide remediation commands
5. **Document Rules**: Use clear titles and descriptions
6. **Group by Category**: Organize related rules together
7. **Version Control**: Track changes to rule files in git
