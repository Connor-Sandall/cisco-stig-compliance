#!/bin/bash
#
# STIG Compliance Check Wrapper Script
# Use this script to run compliance checks with common options
#
# Usage:
#   ./scripts/run_compliance_check.sh                    # Check all devices
#   ./scripts/run_compliance_check.sh --daily            # Daily scheduled check
#   ./scripts/run_compliance_check.sh --weekly           # Weekly scheduled check
#   ./scripts/run_compliance_check.sh --monthly          # Monthly scheduled check
#   ./scripts/run_compliance_check.sh --host switch01    # Check specific host
#   ./scripts/run_compliance_check.sh --remediate        # Run remediation
#   ./scripts/run_compliance_check.sh --dry-run          # Dry run remediation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Default values
SCHEDULE_TYPE="manual"
TARGET_HOST=""
REMEDIATE=false
DRY_RUN=false
EXTRA_VARS=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --daily)
            SCHEDULE_TYPE="daily"
            shift
            ;;
        --weekly)
            SCHEDULE_TYPE="weekly"
            shift
            ;;
        --monthly)
            SCHEDULE_TYPE="monthly"
            shift
            ;;
        --host)
            TARGET_HOST="$2"
            shift 2
            ;;
        --remediate)
            REMEDIATE=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            EXTRA_VARS="$EXTRA_VARS dry_run=true"
            shift
            ;;
        --stig-file)
            EXTRA_VARS="$EXTRA_VARS stig_checklist_file=$2"
            shift 2
            ;;
        --no-approval)
            EXTRA_VARS="$EXTRA_VARS remediation_require_approval=false"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Change to project directory
cd "$PROJECT_DIR" || exit 1

# Build command
if [ "$REMEDIATE" = true ]; then
    PLAYBOOK="playbooks/remediation.yml"
elif [ -n "$TARGET_HOST" ]; then
    PLAYBOOK="playbooks/single_device_check.yml"
    EXTRA_VARS="$EXTRA_VARS target_host=$TARGET_HOST"
elif [ "$SCHEDULE_TYPE" != "manual" ]; then
    PLAYBOOK="playbooks/scheduled_check.yml"
    EXTRA_VARS="$EXTRA_VARS schedule_type=$SCHEDULE_TYPE"
else
    PLAYBOOK="playbooks/compliance_check.yml"
fi

# Add schedule type to extra vars
EXTRA_VARS="$EXTRA_VARS schedule_type=$SCHEDULE_TYPE"

# Build ansible-playbook command
CMD="ansible-playbook $PLAYBOOK"

if [ -n "$EXTRA_VARS" ]; then
    CMD="$CMD -e \"$EXTRA_VARS\""
fi

# Log start
echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting compliance check"
echo "Playbook: $PLAYBOOK"
echo "Schedule: $SCHEDULE_TYPE"
echo "Extra vars: $EXTRA_VARS"
echo "========================================"

# Run ansible playbook
eval "$CMD"
EXIT_CODE=$?

# Log completion
echo "========================================"
echo "$(date '+%Y-%m-%d %H:%M:%S') - Compliance check completed with exit code: $EXIT_CODE"

exit $EXIT_CODE
