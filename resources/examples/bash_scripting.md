# Bash Scripting Examples

## Hello World Script

```bash
#!/bin/bash
echo "Hello, World!"
echo "Script name: $0"
echo "Arguments: $@"
echo "Number of args: $#"
```

## Backup Script

```bash
#!/bin/bash
# Simple backup script with date-stamped archives
set -euo pipefail

SOURCE_DIR="${1:-/home}"
BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d_%H%M%S)
ARCHIVE="$BACKUP_DIR/backup_$DATE.tar.gz"

mkdir -p "$BACKUP_DIR"
tar -czf "$ARCHIVE" "$SOURCE_DIR"
echo "Backup created: $ARCHIVE"

# Remove backups older than 7 days
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -delete
echo "Old backups cleaned up."
```

## Log Monitor Script

```bash
#!/bin/bash
# Monitor a log file for errors and send alerts
LOG_FILE="/var/log/syslog"
PATTERN="error|critical|fatal"

tail -f "$LOG_FILE" | while read -r line; do
    if echo "$line" | grep -iE "$PATTERN" > /dev/null; then
        echo "[ALERT] $(date): $line" >> /var/log/alerts.log
    fi
done
```

## System Health Check

```bash
#!/bin/bash
# System health check script
echo "=== System Health Report ==="
echo "Date: $(date)"
echo ""

echo "--- CPU Usage ---"
top -bn1 | grep "Cpu(s)" | awk '{print "Usage: " $2 "%"}'

echo ""
echo "--- Memory Usage ---"
free -h | awk '/^Mem:/ {print "Used: " $3 "/" $2}'

echo ""
echo "--- Disk Usage ---"
df -h / | awk 'NR==2 {print "Root: " $5 " used (" $3 "/" $2 ")"}'

echo ""
echo "--- Top 5 Processes (by CPU) ---"
ps aux --sort=-%cpu | head -6
```
