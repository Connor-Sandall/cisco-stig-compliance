# Cisco STIG Compliance Checker - Visual Diagrams

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CISCO STIG COMPLIANCE CHECKER                         │
│                              System Architecture                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌───────────────────┐
│   User Actions    │
├───────────────────┤
│ - Run Check       │
│ - Run Remediation │
│ - View Reports    │
│ - Update STIGs    │
└────────┬──────────┘
         │
         v
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ANSIBLE CONTROL NODE                               │
│                                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐               │
│  │   Playbooks    │  │   Inventory    │  │  Vault (Creds) │               │
│  │                │  │                │  │                │               │
│  │ compliance-    │  │ Production     │  │ Encrypted      │               │
│  │   check.yml    │  │ Staging        │  │ Credentials    │               │
│  │ remediation    │  │ Development    │  │                │               │
│  │   .yml         │  │                │  │                │               │
│  └────────┬───────┘  └────────┬───────┘  └────────┬───────┘               │
│           │                   │                   │                        │
│           v                   v                   v                        │
│  ┌───────────────────────────────────────────────────────────┐             │
│  │                     ANSIBLE ROLES                          │             │
│  ├───────────────────────────────────────────────────────────┤             │
│  │                                                            │             │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │             │
│  │  │ stig_parser  │  │device_       │  │compliance_   │   │             │
│  │  │              │  │collector     │  │checker       │   │             │
│  │  │ Parse CKL    │→ │              │→ │              │   │             │
│  │  │ files        │  │ Collect      │  │ Execute      │   │             │
│  │  │              │  │ configs      │  │ checks       │   │             │
│  │  └──────────────┘  └──────────────┘  └──────┬───────┘   │             │
│  │                                              │           │             │
│  │  ┌──────────────┐  ┌──────────────┐        │           │             │
│  │  │remediation_  │  │report_       │←───────┘           │             │
│  │  │engine        │  │generator     │                     │             │
│  │  │              │  │              │                     │             │
│  │  │ Apply fixes  │  │ Create       │                     │             │
│  │  │              │  │ reports      │                     │             │
│  │  └──────────────┘  └──────┬───────┘                     │             │
│  │                           │                             │             │
│  │  ┌──────────────┐         │                             │             │
│  │  │notification  │←────────┘                             │             │
│  │  │              │                                        │             │
│  │  │ Send alerts  │                                        │             │
│  │  └──────────────┘                                        │             │
│  └───────────────────────────────────────────────────────────┘             │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────┐             │
│  │                  CUSTOM MODULES                            │             │
│  ├───────────────────────────────────────────────────────────┤             │
│  │ ckl_parser.py  │ cisco_config_parser.py  │ stig_compliance│             │
│  │                │                         │ _checker.py    │             │
│  └───────────────────────────────────────────────────────────┘             │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
                v                               v
┌───────────────────────────┐   ┌───────────────────────────┐
│    DATA SOURCES           │   │    MANAGED DEVICES        │
├───────────────────────────┤   ├───────────────────────────┤
│                           │   │                           │
│ STIG Checklists           │   │ Cisco IOS Switches        │
│ ┌─────────────────────┐   │   │ ┌─────────────────────┐   │
│ │ current/            │   │   │ │ switch01            │   │
│ │  - IOS_L2S_V2R8.ckl│   │   │ │ switch02            │   │
│ │  - Router_V2R8.ckl │   │   │ │ switch03            │   │
│ │  - NXOS_V2R4.ckl   │   │   │ └─────────────────────┘   │
│ └─────────────────────┘   │   │                           │
│                           │   │ Cisco IOS Routers         │
│ archive/                  │   │ ┌─────────────────────┐   │
│ ┌─────────────────────┐   │   │ │ router01            │   │
│ │ 2025-12-15/         │   │   │ │ router02            │   │
│ │ 2025-11-01/         │   │   │ └─────────────────────┘   │
│ └─────────────────────┘   │   │                           │
└───────────────────────────┘   │ Cisco NX-OS Switches      │
                                │ ┌─────────────────────┐   │
                                │ │ dc-switch01         │   │
                                │ │ dc-switch02         │   │
                                │ └─────────────────────┘   │
                                └───────────────────────────┘
                                           │
                                           v
┌─────────────────────────────────────────────────────────────────────────────┐
│                              OUTPUT & STORAGE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐         │
│  │   Reports        │  │   Backups        │  │   Logs           │         │
│  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤         │
│  │ 2026-01-09/      │  │ 2026-01-09/      │  │ ansible.log      │         │
│  │ ├─ device_       │  │ ├─ pre_remed/    │  │ compliance_      │         │
│  │ │  reports/      │  │ └─ post_remed/   │  │   checks.log     │         │
│  │ ├─ inventory_    │  │                  │  │ remediation.log  │         │
│  │ │  report.html   │  │ 2026-01-08/      │  │ scheduled_       │         │
│  │ └─ executive_    │  │ 2026-01-07/      │  │   runs.log       │         │
│  │    summary.html  │  │                  │  │                  │         │
│  │                  │  │                  │  │                  │         │
│  │ latest/ (link)   │  │ latest/ (link)   │  │                  │         │
│  │                  │  │                  │  │                  │         │
│  │ scheduled/       │  │                  │  │                  │         │
│  │ ├─ daily/        │  │                  │  │                  │         │
│  │ ├─ weekly/       │  │                  │  │                  │         │
│  │ └─ monthly/      │  │                  │  │                  │         │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘         │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────┐          │
│  │                    Notifications                              │          │
│  ├──────────────────────────────────────────────────────────────┤          │
│  │  Email (SMTP)  │  Slack Webhook  │  MS Teams Webhook        │          │
│  └──────────────────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow: STIG CKL to Compliance Result

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        STIG TO COMPLIANCE DATA FLOW                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────┐
│   STIG CKL File (XML)               │
│   From cyber.mil                    │
├─────────────────────────────────────┤
│ <CHECKLIST>                         │
│   <STIGS>                           │
│     <VULN>                          │
│       Vuln_Num: V-220518            │
│       Severity: medium              │
│       Rule_Title: "AAA required"    │
│       Check_Content: "Verify..."    │
│       Fix_Text: "Configure..."      │
│     </VULN>                         │
│   </STIGS>                          │
│ </CHECKLIST>                        │
└─────────────┬───────────────────────┘
              │
              │  ckl_parser.py (library module)
              │  - Parse XML using ElementTree
              │  - Extract all VULN elements
              │  - Convert to Python dict
              │
              v
┌─────────────────────────────────────┐
│   Parsed STIG Data (Memory)        │
├─────────────────────────────────────┤
│ stig_vulnerabilities:               │
│   - vuln_id: V-220518               │
│     severity: CAT2                  │
│     rule_title: "AAA required"      │
│     check_content: "Verify..."      │
│     fix_text: "Configure..."        │
└─────────────┬───────────────────────┘
              │
              │  COMBINED WITH
              │
┌─────────────┴───────────────────────┐
│   STIG Mappings (YAML)              │
│   stig_mappings.yml                 │
├─────────────────────────────────────┤
│ V-220518:                           │
│   name: "AAA new-model required"    │
│   applicable_platforms:             │
│     - ios                           │
│     - ios-xe                        │
│   check_method: config_contains     │
│   config_section: aaa               │
│   required_config:                  │
│     - "aaa new-model"               │
│   severity: CAT2                    │
└─────────────┬───────────────────────┘
              │
              │  compliance_checker role
              │  - Iterate through requirements
              │  - Match V-ID to mapping
              │  - Execute check method
              │
              v
┌─────────────────────────────────────┐
│   Device Configuration              │
│   From device_collector role        │
├─────────────────────────────────────┤
│ hostname switch01                   │
│ !                                   │
│ aaa new-model                       │  ← FOUND!
│ aaa authentication login default... │
│ !                                   │
│ interface GigabitEthernet0/1        │
│ ...                                 │
└─────────────┬───────────────────────┘
              │
              │  Check Execution
              │  - Search config for "aaa new-model"
              │  - String found = Compliant
              │  - String not found = Non-Compliant
              │
              v
┌─────────────────────────────────────┐
│   Finding Result                    │
├─────────────────────────────────────┤
│ vuln_id: V-220518                   │
│ status: NotAFinding (Compliant)     │
│ severity: CAT2                      │
│ finding_details:                    │
│   "AAA new-model: Found"            │
│ evidence:                           │
│   "aaa new-model"                   │
│ check_date: 2026-01-09T10:30:00Z    │
└─────────────┬───────────────────────┘
              │
              │  Aggregate all findings
              │  for all V-IDs
              │
              v
┌─────────────────────────────────────┐
│   Device Compliance Summary         │
├─────────────────────────────────────┤
│ device: switch01.example.com        │
│ compliance_score: 85%               │
│ total_checks: 68                    │
│ compliant: 58                       │
│ non_compliant: 8                    │
│ not_applicable: 2                   │
│                                     │
│ cat1_open: 0                        │
│ cat2_open: 5                        │
│ cat3_open: 3                        │
└─────────────┬───────────────────────┘
              │
              │  report_generator role
              │  - Load Jinja2 templates
              │  - Render HTML report
              │
              v
┌─────────────────────────────────────┐
│   HTML Report                       │
│   switch01.example.com.html         │
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │ STIG Compliance Report          │ │
│ │ Device: switch01.example.com    │ │
│ │ Score: 85%                      │ │
│ │                                 │ │
│ │ Findings:                       │ │
│ │ ✓ V-220518: Compliant (AAA)     │ │
│ │ ✗ V-220519: Non-Compliant       │ │
│ │ ...                             │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

---

## Compliance Check Process Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         COMPLIANCE CHECK PROCESS                             │
└─────────────────────────────────────────────────────────────────────────────┘

START
  │
  v
┌───────────────────────────┐
│ ansible-playbook          │
│ compliance-check.yml      │
└─────────────┬─────────────┘
              │
              v
┌───────────────────────────┐
│ Pre-Tasks                 │
├───────────────────────────┤
│ - Create report directory │
│ - Initialize variables    │
│ - Set timestamp           │
└─────────────┬─────────────┘
              │
              v
┌───────────────────────────┐
│ Role: stig_parser         │
├───────────────────────────┤
│ Tasks:                    │
│ 1. Locate CKL file        │
│ 2. Parse XML structure    │
│ 3. Extract vulnerabilities│
│ 4. Cache parsed data      │
│                           │
│ Output:                   │
│ - stig_requirements list  │
└─────────────┬─────────────┘
              │
              v
┌───────────────────────────┐
│ Role: device_collector    │
│ (Runs on each device)     │
├───────────────────────────┤
│ Tasks:                    │
│ 1. Connect via SSH        │
│ 2. Gather facts           │
│ 3. Get running-config     │
│ 4. Execute show commands: │
│    - show version         │
│    - show users           │
│    - show logging         │
│    - show snmp            │
│ 5. Store config locally   │
│                           │
│ Output:                   │
│ - device_config (text)    │
│ - device_facts (dict)     │
│ - show_output (list)      │
└─────────────┬─────────────┘
              │
              v
┌───────────────────────────┐
│ Role: compliance_checker  │
│ (Runs on each device)     │
├───────────────────────────┤
│ Process:                  │
│                           │
│ FOR EACH stig_requirement:│
│   ├─ Get check_mapping    │
│   ├─ Check if applicable  │
│   │   (platform match)    │
│   ├─ Execute check_method:│
│   │   ├─ config_contains  │
│   │   ├─ config_regex     │
│   │   ├─ banner_check     │
│   │   ├─ show_command     │
│   │   └─ etc.             │
│   ├─ Evaluate result      │
│   │   (Pass/Fail)         │
│   └─ Record finding       │
│                           │
│ Calculate scores:         │
│ - Overall compliance %    │
│ - Findings by severity    │
│ - Open vs closed          │
│                           │
│ Save to JSON file         │
└─────────────┬─────────────┘
              │
              v
┌───────────────────────────┐
│ Post-Tasks                │
├───────────────────────────┤
│ - Aggregate all findings  │
│ - Create metadata.json    │
│ - Create latest symlink   │
└─────────────┬─────────────┘
              │
              v
┌───────────────────────────┐
│ Play 2: localhost         │
│ Report Generation         │
├───────────────────────────┤
│ Role: report_generator    │
│                           │
│ Tasks:                    │
│ 1. Load all device JSON   │
│ 2. Generate device reports│
│    - HTML per device      │
│    - JSON per device      │
│ 3. Generate inventory     │
│    report (all devices)   │
│ 4. Generate executive     │
│    summary                │
│ 5. Generate dashboard     │
└─────────────┬─────────────┘
              │
              v
┌───────────────────────────┐
│ Role: notification        │
│ (If enabled)              │
├───────────────────────────┤
│ Tasks:                    │
│ 1. Prepare notification   │
│    message                │
│ 2. Send email (SMTP)      │
│ 3. POST to Slack webhook  │
│ 4. POST to Teams webhook  │
└─────────────┬─────────────┘
              │
              v
┌───────────────────────────┐
│ END                       │
│                           │
│ Reports available at:     │
│ reports/{timestamp}/      │
└───────────────────────────┘
```

---

## Remediation Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          REMEDIATION WORKFLOW                                │
└─────────────────────────────────────────────────────────────────────────────┘

START
  │
  v
┌──────────────────────────┐
│ ansible-playbook         │
│ remediation.yml          │
└────────────┬─────────────┘
             │
             v
┌──────────────────────────┐
│ PHASE 1:                 │
│ Pre-Remediation Check    │
├──────────────────────────┤
│ Run full compliance      │
│ check (same as above)    │
│                          │
│ Output:                  │
│ - All findings           │
│ - Identify non-compliant │
└────────────┬─────────────┘
             │
             v
┌──────────────────────────┐
│ PHASE 2:                 │
│ Backup Configuration     │
├──────────────────────────┤
│ For each device:         │
│ - Connect via SSH        │
│ - Get running-config     │
│ - Save to file:          │
│   backups/{date}/        │
│   pre_remediation/       │
│   {hostname}.cfg         │
└────────────┬─────────────┘
             │
             v
┌──────────────────────────┐
│ PHASE 3:                 │
│ Generate Remediation Plan│
├──────────────────────────┤
│ For each non-compliant   │
│ finding:                 │
│                          │
│ 1. Load remediation      │
│    mapping               │
│ 2. Select config template│
│ 3. Render Jinja2 template│
│ 4. Generate commands     │
│                          │
│ Example:                 │
│ V-220518 → aaa_template  │
│         → "aaa new-model"│
│                          │
│ Display plan to user:    │
│ ┌────────────────────┐   │
│ │ Remediation Plan   │   │
│ │                    │   │
│ │ switch01:          │   │
│ │ - aaa new-model    │   │
│ │ - aaa auth...      │   │
│ │                    │   │
│ │ router01:          │   │
│ │ - banner login...  │   │
│ └────────────────────┘   │
└────────────┬─────────────┘
             │
             v
        ┌────┴────┐
        │ IF      │
        │ require_│
        │ approval│
        └────┬────┘
             │ YES
             v
┌──────────────────────────┐
│ PHASE 4:                 │
│ Approval Gate            │
├──────────────────────────┤
│ [PAUSE]                  │
│                          │
│ Prompt user:             │
│ "Proceed with            │
│  remediation? (yes/no)"  │
│                          │
│ Wait for input...        │
└────────┬─────────────────┘
         │ "yes"
         v
┌──────────────────────────┐
│ PHASE 5:                 │
│ Apply Remediation        │
├──────────────────────────┤
│ For each device:         │
│                          │
│ 1. Connect via SSH       │
│ 2. Apply commands using  │
│    cisco.ios.ios_config: │
│    - lines: [commands]   │
│    - save_when: modified │
│ 3. After each command:   │
│    - Verify applied      │
│    - Check for errors    │
│ 4. Log all actions       │
│                          │
│ If any command fails:    │
│ → Jump to ROLLBACK       │
└────────────┬─────────────┘
             │ SUCCESS
             v
┌──────────────────────────┐
│ PHASE 6:                 │
│ Post-Remediation Verify  │
├──────────────────────────┤
│ 1. Run compliance check  │
│    again                 │
│ 2. Compare results:      │
│    Before: 68% compliant │
│    After:  94% compliant │
│ 3. Verify improvements   │
│ 4. Backup post-config    │
└────────────┬─────────────┘
             │
             v
┌──────────────────────────┐
│ PHASE 7:                 │
│ Generate Report          │
├──────────────────────────┤
│ Remediation Report:      │
│                          │
│ ┌────────────────────┐   │
│ │ Changes Made:      │   │
│ │                    │   │
│ │ switch01:          │   │
│ │ ✓ Fixed V-220518   │   │
│ │ ✓ Fixed V-220519   │   │
│ │                    │   │
│ │ Score: 68% → 94%   │   │
│ │                    │   │
│ │ Remaining Issues:  │   │
│ │ - V-220650 (CAT3)  │   │
│ └────────────────────┘   │
└────────────┬─────────────┘
             │
             v
           END


         FAILURE PATH
             │
             v
┌──────────────────────────┐
│ ROLLBACK                 │
├──────────────────────────┤
│ 1. Load backup config    │
│    from:                 │
│    backups/{date}/       │
│    pre_remediation/      │
│                          │
│ 2. Apply backup using    │
│    cisco.ios.ios_config: │
│    - src: backup.cfg     │
│                          │
│ 3. Verify restoration    │
│                          │
│ 4. Generate failure      │
│    report                │
│                          │
│ 5. Send alert            │
│    notification          │
└────────────┬─────────────┘
             │
             v
           END
        (ABORTED)
```

---

## Scheduled Execution Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SCHEDULED EXECUTION                                  │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────┐
│         SYSTEM SCHEDULER                │
│                                         │
│  Linux: cron                            │
│  Windows: Task Scheduler                │
└──────────────┬──────────────────────────┘
               │
               │ Triggers at scheduled time
               │
               v
┌────────────────────────────────────────┐
│  Cron Job Entry                        │
├────────────────────────────────────────┤
│  Daily:   0 2 * * *                    │
│  Weekly:  0 2 * * 0                    │
│  Monthly: 0 2 1 * *                    │
│                                        │
│  Command:                              │
│  cd /path/to/project &&                │
│  ./scripts/schedule_compliance_        │
│  check.sh run daily                    │
└──────────────┬─────────────────────────┘
               │
               v
┌────────────────────────────────────────┐
│  schedule_compliance_check.sh          │
├────────────────────────────────────────┤
│  1. Set environment variables          │
│  2. Activate Python venv               │
│  3. Set report directory:              │
│     reports/scheduled/daily/           │
│     {YYYY-MM-DD}/                      │
│  4. Execute Ansible playbook:          │
│     ansible-playbook                   │
│       compliance-check.yml             │
│       -e schedule_type=daily           │
│  5. Log output to:                     │
│     logs/scheduled_runs.log            │
└──────────────┬─────────────────────────┘
               │
               v
┌────────────────────────────────────────┐
│  Ansible Playbook Execution            │
│  (Full compliance check)               │
├────────────────────────────────────────┤
│  - Parse STIG                          │
│  - Collect from devices                │
│  - Check compliance                    │
│  - Generate reports                    │
│  - Send notifications                  │
└──────────────┬─────────────────────────┘
               │
               v
┌────────────────────────────────────────┐
│  Post-Execution Tasks                  │
├────────────────────────────────────────┤
│  1. Create symlink:                    │
│     scheduled/daily/latest →           │
│     2026-01-09                         │
│                                        │
│  2. Cleanup old reports:               │
│     Keep last 30 daily                 │
│     Keep last 12 weekly                │
│     Keep last 12 monthly               │
│                                        │
│  3. Send notifications:                │
│     - Email with summary               │
│     - Webhook to Slack/Teams           │
│     - Only if:                         │
│       * Failures occurred              │
│       * Critical findings              │
│       * Weekly summary                 │
└──────────────┬─────────────────────────┘
               │
               v
┌────────────────────────────────────────┐
│  Report Storage Structure              │
├────────────────────────────────────────┤
│  reports/scheduled/                    │
│  ├─ daily/                             │
│  │  ├─ latest → 2026-01-09            │
│  │  ├─ 2026-01-09/                    │
│  │  │  ├─ device_reports/             │
│  │  │  ├─ inventory_report.html       │
│  │  │  └─ metadata.json               │
│  │  ├─ 2026-01-08/                    │
│  │  └─ 2026-01-07/                    │
│  │                                     │
│  ├─ weekly/                            │
│  │  ├─ latest → 2026-W02              │
│  │  ├─ 2026-W02/                      │
│  │  └─ 2026-W01/                      │
│  │                                     │
│  └─ monthly/                           │
│     ├─ latest → 2026-01                │
│     ├─ 2026-01/                        │
│     └─ 2025-12/                        │
└────────────────────────────────────────┘


Notification Flow:
                │
                v
┌────────────────────────────────────────┐
│  Email Notification                    │
├────────────────────────────────────────┤
│  To: network-team@example.com          │
│  Subject: Daily STIG Compliance Report │
│                                        │
│  Overall Compliance: 87%               │
│  Devices Checked: 45                   │
│  CAT1 Open: 2                          │
│  CAT2 Open: 18                         │
│                                        │
│  View Full Report:                     │
│  file:///reports/scheduled/daily/      │
│       latest/inventory_report.html     │
└────────────────────────────────────────┘
                │
                v
┌────────────────────────────────────────┐
│  Slack/Teams Notification              │
├────────────────────────────────────────┤
│  Daily STIG Compliance Update          │
│                                        │
│  Status: ⚠️ Action Required            │
│  Compliance: 87% (↓ 3% from yesterday)│
│                                        │
│  Critical Issues:                      │
│  • 2 CAT1 findings                     │
│  • 3 devices below 80%                 │
│                                        │
│  [View Report]                         │
└────────────────────────────────────────┘
```

---

## Role Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ROLE INTERACTIONS                                   │
└─────────────────────────────────────────────────────────────────────────────┘

                        ┌─────────────────┐
                        │   User/Cron     │
                        └────────┬────────┘
                                 │
                                 v
                        ┌─────────────────┐
                        │   Main Playbook │
                        │ compliance-check│
                        │   .yml          │
                        └────────┬────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              v                  v                  v
    ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
    │ stig_parser     │ │device_collector │ │compliance_      │
    │                 │ │                 │ │checker          │
    │ Input:          │ │ Input:          │ │                 │
    │ - CKL file      │ │ - Inventory     │ │ Input:          │
    │                 │ │ - Credentials   │ │ - STIG reqs     │
    │ Does:           │ │                 │ │ - Device config │
    │ - Parse XML     │ │ Does:           │ │ - Mappings      │
    │ - Extract V-IDs │ │ - Connect SSH   │ │                 │
    │                 │ │ - Get config    │ │ Does:           │
    │ Output:         │ │ - Run shows     │ │ - Execute checks│
    │ - Requirements  │ │                 │ │ - Evaluate      │
    │   list          │ │ Output:         │ │ - Record        │
    │                 │ │ - device_config │ │                 │
    └────────┬────────┘ └────────┬────────┘ │ Output:         │
             │                   │          │ - Findings list │
             │     Provides      │          │                 │
             └──────┬────────────┘          └────────┬────────┘
                    │                                │
                    │         Uses                   │
                    v                                │
         ┌──────────────────┐                        │
         │ STIG Requirements│                        │
         │ Data Structure   │                        │
         └──────────────────┘                        │
                    │                                │
                    │          Combines              │
                    v                                │
         ┌──────────────────┐                        │
         │ Device Config    │←───────────────────────┘
         │ Data Structure   │
         └────────┬─────────┘
                  │
                  │    Both feed into
                  v
         ┌──────────────────┐
         │ Findings         │
         │ Data Structure   │
         └────────┬─────────┘
                  │
                  │    Consumed by
                  │
      ┌───────────┼───────────┬───────────────┐
      │           │           │               │
      v           v           v               v
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│report_   │ │remedia-  │ │notifica- │ │ Logs     │
│generator │ │tion_     │ │tion      │ │          │
│          │ │engine    │ │          │ │          │
│Input:    │ │          │ │Input:    │ │Input:    │
│-Findings │ │Input:    │ │-Report   │ │-All      │
│          │ │-Findings │ │ summary  │ │ actions  │
│Does:     │ │ (Open)   │ │          │ │          │
│-Aggregate│ │-Templates│ │Does:     │ │Does:     │
│-Render   │ │          │ │-Format   │ │-Write to │
│ HTML     │ │Does:     │ │ message  │ │ log files│
│          │ │-Generate │ │-Send     │ │          │
│Output:   │ │ commands │ │ email    │ │Output:   │
│-HTML     │ │-Apply    │ │-POST     │ │-ansible  │
│ reports  │ │ fixes    │ │ webhook  │ │ .log     │
│-JSON     │ │-Verify   │ │          │ │-compliance│
│ reports  │ │          │ │Output:   │ │ _checks  │
│          │ │Output:   │ │-Sent     │ │ .log     │
└──────────┘ │-Remedia- │ │ status   │ │          │
             │ tion     │ │          │ │          │
             │ report   │ └──────────┘ └──────────┘
             └──────────┘
```

---

## File System Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          FILE SYSTEM LAYOUT                                  │
└─────────────────────────────────────────────────────────────────────────────┘

E:\01- Chrome Downloads\cisco-stig-compliance\
│
├── [CODE] Source Files (Version Controlled)
│   ├── ansible.cfg                    Config file
│   ├── requirements.txt               Python deps
│   ├── requirements.yml               Ansible deps
│   ├── *.yml playbooks               Main playbooks
│   │
│   ├── inventory/                     Device lists
│   │   └── production/
│   │       ├── hosts.yml             ~100 lines
│   │       └── group_vars/
│   │           ├── all.yml           ~50 lines
│   │           └── vault.yml         Encrypted
│   │
│   ├── roles/                        ~80-100 files
│   │   ├── stig_parser/              ~12 files
│   │   ├── device_collector/         ~15 files
│   │   ├── compliance_checker/       ~25 files
│   │   ├── remediation_engine/       ~18 files
│   │   ├── report_generator/         ~15 files
│   │   └── notification/             ~10 files
│   │
│   ├── library/                      ~8-10 files
│   │   ├── ckl_parser.py            ~300 lines
│   │   └── cisco_config_parser.py   ~200 lines
│   │
│   ├── filter_plugins/               ~5 files
│   ├── config_templates/             ~20-30 files
│   ├── scripts/                      ~10 files
│   ├── tests/                        ~15-20 files
│   └── docs/                         ~10 files
│
├── [DATA] User-Managed Files
│   └── stig_checklists/
│       ├── current/                   Active CKLs
│       │   ├── IOS_L2S_V2R8.ckl     ~5MB XML
│       │   └── Router_V2R8.ckl      ~5MB XML
│       └── archive/                  Old versions
│           └── 2025-12-15/
│
└── [OUTPUT] Generated Files (Not in Git)
    ├── reports/                      Grows daily
    │   ├── 2026-01-09_10-30-00/     ~50-100 files
    │   │   ├── device_reports/       1 HTML + 1 JSON per device
    │   │   ├── inventory_report.html ~500KB
    │   │   └── metadata.json         ~10KB
    │   │
    │   ├── latest/                   Symlink
    │   │
    │   └── scheduled/
    │       ├── daily/                ~30 directories
    │       ├── weekly/               ~12 directories
    │       └── monthly/              ~12 directories
    │
    ├── backups/                      Grows with remediations
    │   ├── 2026-01-09/
    │   │   ├── pre_remediation/      1 file per device
    │   │   └── post_remediation/     1 file per device
    │   └── latest/                   Symlink
    │
    ├── logs/                         Grows continuously
    │   ├── ansible.log               ~10MB (rotated)
    │   ├── compliance_checks.log     ~5MB
    │   ├── remediation.log           ~2MB
    │   └── scheduled_runs.log        ~5MB
    │
    └── cache/                        Temporary
        ├── facts/                    Ansible fact cache
        └── parsed_stigs/             Parsed CKL cache


Storage Growth Estimates:
┌──────────────┬────────────┬────────────┬────────────┐
│ Time Period  │ Reports    │ Backups    │ Total      │
├──────────────┼────────────┼────────────┼────────────┤
│ Initial      │ ~50 MB     │ 0          │ ~50 MB     │
│ 1 Week       │ ~350 MB    │ ~50 MB     │ ~400 MB    │
│ 1 Month      │ ~1.5 GB    │ ~200 MB    │ ~1.7 GB    │
│ 3 Months     │ ~3 GB      │ ~500 MB    │ ~3.5 GB    │
│ 1 Year       │ ~5 GB      │ ~1 GB      │ ~6 GB      │
│ (with cleanup)                                      │
└──────────────┴────────────┴────────────┴────────────┘
```

---

## Deployment Topology

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DEPLOYMENT TOPOLOGY                                  │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌───────────────────────────┐
                    │   Management Workstation  │
                    │   (Windows/Linux)         │
                    ├───────────────────────────┤
                    │ - Ansible installed       │
                    │ - Python 3.9+             │
                    │ - Project files           │
                    │ - SSH client              │
                    └────────────┬──────────────┘
                                 │
                                 │ SSH over
                                 │ Management Network
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        │                        │                        │
┌───────┴────────┐   ┌───────────┴──────────┐   ┌────────┴───────┐
│ Production     │   │ Staging              │   │ Development    │
│ Environment    │   │ Environment          │   │ Environment    │
├────────────────┤   ├──────────────────────┤   ├────────────────┤
│                │   │                      │   │                │
│ Switches:      │   │ Switches:            │   │ Lab Devices:   │
│ - 25 IOS L2S   │   │ - 5 IOS L2S          │   │ - 3 IOS        │
│ - 15 IOS RTR   │   │ - 3 IOS RTR          │   │ - 2 NX-OS      │
│ - 10 NX-OS     │   │ - 2 NX-OS            │   │                │
│                │   │                      │   │                │
│ Check: Daily   │   │ Check: Weekly        │   │ Check: Ad-hoc  │
│ Remediation:   │   │ Remediation:         │   │ Remediation:   │
│ Manual approve │   │ Auto (non-prod)      │   │ Testing only   │
│                │   │                      │   │                │
└────────────────┘   └──────────────────────┘   └────────────────┘


Network Topology:

┌──────────────────────────────────────────────────────────────┐
│                    Network Layout                            │
└──────────────────────────────────────────────────────────────┘

    Management VLAN 10 (10.1.10.0/24)
            │
            ├─ Management Workstation (10.1.10.5)
            │
            ├─ Ansible Control Node (can be same as workstation)
            │
    ┌───────┴────────────────────────────────────┐
    │                                            │
Production VLAN 100                  Datacenter VLAN 200
(10.1.100.0/24)                     (10.2.200.0/24)
    │                                            │
    ├─ IOS Switch01 (.10)                       ├─ NX-OS Switch01 (.10)
    ├─ IOS Switch02 (.11)                       ├─ NX-OS Switch02 (.11)
    ├─ IOS Switch03 (.12)                       └─ NX-OS Switch03 (.12)
    └─ IOS Router01 (.20)


Firewall Rules Required:
┌──────────────────────────────────────────────────────────────┐
│ Source: Management Workstation (10.1.10.5)                   │
│ Destination: All managed devices                             │
│ Ports: TCP/22 (SSH)                                          │
│ Protocol: SSH                                                │
└──────────────────────────────────────────────────────────────┘
```

---

**Document Version**: 1.0.0
**Last Updated**: 2026-01-09
**Total Diagrams**: 8
