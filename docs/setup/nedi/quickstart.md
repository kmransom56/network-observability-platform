# NeDi Setup Quick Start Guide

Complete setup of NeDi with all enhancements for the Network Observability Platform in minutes.

## What Gets Installed

This setup includes:

- ✅ **NeDi Network Discovery** - SNMP-based network topology discovery
- ✅ **Vendor-Specific Icons** - 240+ FortiGate, FortiAP, FortiSwitch SVG icons
- ✅ **Client Device Icons** - Mobile, laptop, desktop icons for discovered devices
- ✅ **Enhanced Topology Map** - D3.js visualization with device metrics
- ✅ **Web Interface** - PHP-based NeDi management interface
- ✅ **Database** - MySQL backend for device inventory

## Option 1: Quick Setup (10 minutes)

**For systems with existing NeDi installation:**

```bash
# Navigate to repository
cd /home/keith/network-observability-platform

# Run setup script
sudo ./scripts/setup-nedi-integration.sh

# Restart web server
sudo systemctl restart apache2

# Access NeDi
open http://localhost/Topology-Map.php
```

**What it does:**
- Copies enhanced icon library
- Applies PHP web interface enhancements
- Verifies all files and permissions
- Creates integration guide

## Option 2: Full Installation (30 minutes)

**For fresh system setup:**

```bash
# Navigate to repository
cd /home/keith/network-observability-platform

# Run full installation
sudo ./scripts/setup-nedi-integration.sh --with-nedi-install

# Configure SNMP credentials (interactive)
sudo /var/nedi/nedi.pl -c

# Run initial discovery
sudo /var/nedi/nedi.pl

# Check results
open http://localhost/Topology-Map.php
```

**What it does:**
- Installs all system dependencies
- Downloads and installs NeDi base application
- Sets up MySQL database
- Copies enhanced icon library
- Applies PHP enhancements
- Configures Apache web server
- Runs initial network discovery

## Manual Step-by-Step (if scripts don't work)

### 1. Install Dependencies

```bash
sudo apt-get update
sudo apt-get install -y \
    perl perl-modules libdbi-perl libdbd-mysql-perl \
    libnet-snmp-perl libfile-find-rule-perl \
    mysql-client mysql-server apache2 \
    php php-mysql php-cli snmp
```

### 2. Download NeDi

```bash
cd /tmp
wget https://www.nedi.ch/pub/nedi_1.0.tar.gz
tar xzf nedi_1.0.tar.gz
cd nedi_1.0
sudo ./install.sh
```

### 3. Install Icon Library

```bash
sudo cp -r /home/keith/NeDi/icon_library/* /var/nedi/icon_library/
sudo chown -R nedi:nedi /var/nedi/icon_library
sudo chmod -R 755 /var/nedi/icon_library
```

### 4. Apply PHP Enhancements

```bash
sudo python3 /home/keith/NeDi/apply-enhancements.py
```

### 5. Configure NeDi

```bash
# Edit configuration
sudo nano /var/nedi/nedi.conf

# Key settings:
# - database name: nedi
# - database user: nedi
# - database password: dbpa55
# - backend: mysql
# - snmp_version: 3
```

### 6. Start Services

```bash
# Restart Apache
sudo systemctl restart apache2

# Start NeDi discovery (optional - runs as cron job)
sudo /var/nedi/nedi.pl -c
```

### 7. Access NeDi

```bash
# Open in browser
http://localhost/Topology-Map.php

# Or test via curl
curl http://localhost/Topology-Map.php?fmt=json | head
```

## Testing Enhancements

Verify the enhancements are working:

```bash
# Test 1: Icon library is accessible
curl -I http://localhost/icon_library/fortigate/FG-1000.svg
# Expected: HTTP/1.1 200 OK

# Test 2: Client device icons exist
curl -I http://localhost/icon_library/endpoints/mobile.svg
# Expected: HTTP/1.1 200 OK

# Test 3: Topology map returns JSON with icons
curl http://localhost/Topology-Map.php?fmt=json | \
  python3 -m json.tool | grep -E '"vi"|"ci"|"vn"|"cn"' | head

# Test 4: PHP syntax is valid
php -l /var/nedi/html/inc/libmap.php
php -l /var/nedi/html/inc/libmisc.php
```

## Configuration

### Add Network Devices

Edit `/var/nedi/nedi.conf`:

```ini
# Device discovery targets
# Format: IP-range or hostname
[discovery]
# Example:
# targets = 192.168.1.0/24 192.168.2.0/24 10.0.0.0/8

# SNMP Configuration
[snmp]
snmp_version = 3
# Or for SNMP v2:
# snmp_version = 2
# snmp_community = public

# For SNMP v3:
snmp_user = admin
snmp_auth_proto = SHA
snmp_auth_pass = YourPassword
snmp_priv_proto = AES
snmp_priv_pass = YourPassword
```

### Configure SNMP on Devices

**FortiGate:**

```
config system snmp community
    edit 1
        set name "public"
    next
end
```

**FortiSwitch/FortiAP:**

```
config system snmp community
    edit 1
        set name "nedi"
    next
end
```

**Cisco Meraki:** Use Dashboard API keys instead of SNMP

## Running Discovery

### Initial Discovery

```bash
# Full discovery (may take time for large networks)
sudo /var/nedi/nedi.pl

# With verbose output
sudo /var/nedi/nedi.pl -v

# Specific target
sudo /var/nedi/nedi.pl 192.168.1.0/24
```

### Scheduled Discovery

NeDi automatically schedules discovery via cron. Check:

```bash
# View cron job
sudo crontab -u nedi -l

# Or check job schedule
cat /var/nedi/nedi.conf | grep -i "interval\|cron"
```

## Troubleshooting

### Issue: Icons not displaying

```bash
# Check permissions
ls -la /var/nedi/icon_library/fortigate/ | head -5

# Verify web server access
sudo -u www-data stat /var/nedi/icon_library/fortigate/FG-1000.svg

# Check Apache error log
sudo tail -50 /var/log/apache2/error.log
```

### Issue: Devices not discovered

```bash
# Check NeDi logs
tail -100 /var/nedi/logs/nedi.log

# Verify SNMP connectivity
snmpwalk -v 2c -c public 192.168.1.1 sysDescr

# Check database
mysql -u nedi -pdbpa55 nedi -e "SELECT COUNT(*) FROM devices;"
```

### Issue: Topology map shows no devices

```bash
# Ensure discovery has run
ls -la /var/nedi/logs/nedi.log

# Check database connectivity
mysql -u nedi -pdbpa55 nedi -e "SELECT * FROM devices LIMIT 5;"

# Verify PHP can access database
php -r "mysqli_connect('localhost', 'nedi', 'dbpa55', 'nedi') or die('DB Error');"
```

## File Locations

| Item | Location |
|------|----------|
| **NeDi Installation** | `/var/nedi/` |
| **Icon Library** | `/var/nedi/icon_library/` |
| **Web Interface** | `/var/nedi/html/` |
| **PHP Files** | `/var/nedi/html/inc/` |
| **Configuration** | `/var/nedi/nedi.conf` |
| **Database** | `nedi` (MySQL) |
| **Logs** | `/var/nedi/logs/` |
| **Reports** | `/var/nedi/reports/` |

## Next Steps

1. **Configure Additional Network Devices**
   - Add IP ranges in `/var/nedi/nedi.conf`
   - Configure SNMP on each device
   - Run discovery again

2. **Integrate with Network Observability Platform**
   - See [Application Setup](../application-setup.md)
   - Configure FastAPI backend
   - Set up API endpoints

3. **Set Up Monitoring/Alerts**
   - Configure alert rules in NeDi
   - Set up email notifications
   - Create custom reports

4. **Advanced Configuration**
   - SNMP v3 security
   - Custom device icons
   - Topology filters and views
   - Performance optimization

## Support & Documentation

- **NeDi Official**: https://www.nedi.ch/
- **NeDi Installation**: https://www.nedi.ch/installation/
- **NeDi Configuration**: https://www.nedi.ch/installation/index.html
- **NeDi Guide PDF**: https://www.nedi.ch/pub/The%20NeDi%20Guide.pdf

## Scripts Overview

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/setup-nedi-integration.sh` | Main setup automation | `sudo ./scripts/setup-nedi-integration.sh` |
| `/home/keith/NeDi/apply-enhancements.py` | Apply PHP enhancements | `sudo python3 apply-enhancements.py` |
| `/var/nedi/nedi.pl` | NeDi discovery engine | `sudo /var/nedi/nedi.pl` |

## Dry Run Mode

Test the setup without making changes:

```bash
# Preview what would be done
./scripts/setup-nedi-integration.sh --dry-run

# Shows all actions that would be taken
# Useful for understanding the setup process
```

---

**Get started now:** `sudo ./scripts/setup-nedi-integration.sh`

Need help? Check the logs at: `./nedi_setup.log`
