#!/bin/bash
#
# Setup Scheduled Compliance Checks (Linux/macOS)
# Creates cron jobs for daily, weekly, and monthly checks
#
# Usage:
#   ./scripts/setup_schedule.sh              # Interactive setup
#   ./scripts/setup_schedule.sh --daily      # Setup daily only
#   ./scripts/setup_schedule.sh --all        # Setup all schedules
#   ./scripts/setup_schedule.sh --remove     # Remove all schedules

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Cron schedule defaults
DAILY_SCHEDULE="0 6 * * *"           # 6:00 AM daily
WEEKLY_SCHEDULE="0 6 * * 0"          # 6:00 AM Sundays
MONTHLY_SCHEDULE="0 6 1 * *"         # 6:00 AM first day of month

setup_daily() {
    echo "Setting up daily compliance check..."
    (crontab -l 2>/dev/null | grep -v "cisco-stig.*daily"; echo "$DAILY_SCHEDULE cd $PROJECT_DIR && ./scripts/run_compliance_check.sh --daily >> logs/cron_daily.log 2>&1") | crontab -
    echo "Daily check scheduled for 6:00 AM"
}

setup_weekly() {
    echo "Setting up weekly compliance check..."
    (crontab -l 2>/dev/null | grep -v "cisco-stig.*weekly"; echo "$WEEKLY_SCHEDULE cd $PROJECT_DIR && ./scripts/run_compliance_check.sh --weekly >> logs/cron_weekly.log 2>&1") | crontab -
    echo "Weekly check scheduled for Sundays at 6:00 AM"
}

setup_monthly() {
    echo "Setting up monthly compliance check..."
    (crontab -l 2>/dev/null | grep -v "cisco-stig.*monthly"; echo "$MONTHLY_SCHEDULE cd $PROJECT_DIR && ./scripts/run_compliance_check.sh --monthly >> logs/cron_monthly.log 2>&1") | crontab -
    echo "Monthly check scheduled for 1st of each month at 6:00 AM"
}

remove_all() {
    echo "Removing all scheduled compliance checks..."
    crontab -l 2>/dev/null | grep -v "cisco-stig" | crontab -
    echo "All schedules removed"
}

show_current() {
    echo "Current cron jobs:"
    crontab -l 2>/dev/null | grep "cisco-stig" || echo "No scheduled checks found"
}

# Main logic
case "${1:-}" in
    --daily)
        setup_daily
        ;;
    --weekly)
        setup_weekly
        ;;
    --monthly)
        setup_monthly
        ;;
    --all)
        setup_daily
        setup_weekly
        setup_monthly
        ;;
    --remove)
        remove_all
        ;;
    --show)
        show_current
        ;;
    *)
        echo "STIG Compliance Schedule Setup"
        echo "=============================="
        echo ""
        echo "Options:"
        echo "  --daily    Setup daily check (6:00 AM)"
        echo "  --weekly   Setup weekly check (Sundays 6:00 AM)"
        echo "  --monthly  Setup monthly check (1st of month 6:00 AM)"
        echo "  --all      Setup all schedules"
        echo "  --remove   Remove all schedules"
        echo "  --show     Show current schedules"
        echo ""
        show_current
        ;;
esac
