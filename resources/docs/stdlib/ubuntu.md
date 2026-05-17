# Ubuntu System Administration Reference

## Package Management (APT)

```bash
sudo apt update              # Update package list
sudo apt upgrade -y          # Upgrade all packages
sudo apt install pkg -y      # Install package
sudo apt remove pkg          # Remove package
sudo apt purge pkg           # Remove with config
sudo apt autoremove          # Remove unused deps
apt search "keyword"         # Search packages
apt show pkg                 # Package info
```

## Service Management (systemd)

```bash
sudo systemctl start service
sudo systemctl stop service
sudo systemctl restart service
sudo systemctl enable service    # Start at boot
sudo systemctl disable service   # Don't start at boot
systemctl status service
journalctl -u service -f         # Follow logs
```

## User Management

```bash
sudo useradd -m -s /bin/bash user
sudo passwd user
sudo usermod -aG group user
sudo userdel -r user
id user
groups user
```

## File Permissions

```bash
chmod 755 file    # rwxr-xr-x
chmod u+x file    # Add execute for owner
chown user:group file
chown -R user:group dir/
```

## Networking

```bash
ip addr show          # Show IP addresses
ss -tuln              # Show listening ports
sudo ufw enable       # Enable firewall
sudo ufw allow 22/tcp # Allow SSH
ping host             # Test connectivity
```

## Disk Management

```bash
df -h                 # Disk space usage
du -sh dir/           # Directory size
lsblk                 # List block devices
mount /dev/sdb1 /mnt  # Mount device
```

## Process Management

```bash
ps aux                # All processes
top                   # Real-time monitor
kill PID              # Terminate process
kill -9 PID           # Force kill
nice -n 10 command    # Run with lower priority
```

## Cron Jobs

Format: `minute hour day month weekday command`

```bash
crontab -e            # Edit crontab
crontab -l            # List cron jobs
# 0 2 * * * /path/to/backup.sh   # Daily at 2 AM
# */5 * * * * /path/to/check.sh  # Every 5 minutes
```
