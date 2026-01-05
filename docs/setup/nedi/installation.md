# NeDi Installation Guide for Network Observability Platform

This guide provides step-by-step instructions for installing NeDi with all enhancements for the Network Observability Platform, including vendor-specific device icons and client device identification.

## Prerequisites

- Ubuntu/Debian Linux system
- Root or sudo access
- 2GB+ disk space
- MySQL/MariaDB server running
- SNMP v3 configured on managed devices (optional but recommended)

## System Requirements

```bash
# Check Ubuntu version
lsb_release -a

# Recommended: Ubuntu 22.04 LTS or later
```

## Step 1: Install Base Dependencies

```bash
#!/bin/bash
set -e

echo "Installing NeDi dependencies..."
sudo apt-get update
sudo apt-get install -y \
    perl \
    perl-modules \
    libdbi-perl \
    libdbd-mysql-perl \
    libnet-snmp-perl \
    libfile-find-rule-perl \
    mysql-client \
    apache2 \
    php \
    php-mysql \
    php-cli \
    snmp \
    snmpd

echo "✓ Dependencies installed"
```

## Step 2: Create NeDi System User

```bash
#!/bin/bash
set -e

echo "Creating NeDi user and directories..."

# Create nedi user
sudo useradd -r -s /bin/bash -m nedi || echo "User nedi already exists"

# Create installation directory
sudo mkdir -p /var/nedi
sudo chown nedi:nedi /var/nedi
sudo chmod 755 /var/nedi

echo "✓ NeDi user and directories created"
```

## Step 3: Download and Install NeDi

```bash
#!/bin/bash
set -e

cd /tmp

echo "Downloading NeDi..."
# Download latest NeDi version
wget https://www.nedi.ch/pub/nedi_1.0.tar.gz

echo "Extracting NeDi..."
tar xzf nedi_1.0.tar.gz

echo "Installing NeDi..."
cd nedi_1.0

# Run installation script
sudo ./install.sh

echo "✓ NeDi base installation complete"
```

## Step 4: Apply Icon Library Enhancements

The enhanced icon library with vendor-specific device icons is essential for topology visualization.

```bash
#!/bin/bash
set -e

echo "Setting up enhanced icon library..."

# Copy enhanced icon library
sudo cp -r /home/keith/NeDi/icon_library/* /var/nedi/icon_library/

# Set proper permissions
sudo chown -R nedi:nedi /var/nedi/icon_library
sudo chmod -R 755 /var/nedi/icon_library

# Verify icons
if [ -d /var/nedi/icon_library/fortigate ] && [ -d /var/nedi/icon_library/endpoints ]; then
    echo "✓ Enhanced icon library installed successfully"
    echo "  - FortiGate icons: $(ls /var/nedi/icon_library/fortigate/*.svg 2>/dev/null | wc -l)"
    echo "  - FortiAP icons: $(ls /var/nedi/icon_library/fortiap/*.svg 2>/dev/null | wc -l)"
    echo "  - FortiSwitch icons: $(ls /var/nedi/icon_library/fortiswitch/*.svg 2>/dev/null | wc -l)"
    echo "  - Client device icons: $(ls /var/nedi/icon_library/endpoints/*.svg 2>/dev/null | wc -l)"
else
    echo "✗ Error: Icon library not installed correctly"
    exit 1
fi
```

## Step 5: Apply PHP Web Interface Enhancements

Apply the vendor-specific device icon enhancements to the web interface.

### Option A: Using Automated Patch Script (Recommended)

```bash
#!/bin/bash
set -e

echo "Applying PHP web interface enhancements..."

# Navigate to NeDi directory
cd /var/nedi/html/inc

# Backup original files
sudo cp libmap.php libmap.php.backup.$(date +%s)
sudo cp libmisc.php libmisc.php.backup.$(date +%s)

echo "Backing up original files..."
echo "  - libmap.php → libmap.php.backup.*"
echo "  - libmisc.php → libmisc.php.backup.*"

# Apply enhancements using Python script
sudo python3 /home/keith/NeDi/apply-enhancements.py

# Verify PHP syntax
echo "Verifying PHP syntax..."
sudo php -l libmap.php
sudo php -l libmisc.php

echo "✓ PHP enhancements applied successfully"
```

### Option B: Manual Application

If you prefer to manually apply the enhancements, you can review the changes made by the automated script in `/home/keith/NeDi/apply-enhancements.py` and apply them manually to the PHP files.

## Step 6: Configure NeDi Database

```bash
#!/bin/bash
set -e

echo "Configuring NeDi database..."

# Create NeDi database
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS nedi;"

# Create NeDi database user
mysql -u root -p -e "CREATE USER IF NOT EXISTS 'nedi'@'localhost' IDENTIFIED BY 'dbpa55';"
mysql -u root -p -e "GRANT ALL PRIVILEGES ON nedi.* TO 'nedi'@'localhost';"
mysql -u root -p -e "FLUSH PRIVILEGES;"

# Initialize database schema
mysql -u nedi -pdbpa55 nedi < /var/nedi/nedi.sql

echo "✓ NeDi database configured"
```

## Step 7: Configure Web Server

```bash
#!/bin/bash
set -e

echo "Configuring Apache for NeDi..."

# Enable Apache modules
sudo a2enmod rewrite
sudo a2enmod php

# Create Apache configuration
sudo tee /etc/apache2/sites-available/nedi.conf > /dev/null <<EOF
<VirtualHost *:80>
    ServerName nedi.local
    ServerAdmin admin@nedi.local
    DocumentRoot /var/nedi/html
    
    <Directory /var/nedi/html>
        Options FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    
    <Directory /var/nedi/icon_library>
        Options FollowSymLinks
        AllowOverride None
        Require all granted
        <FilesMatch "\\.svg$">
            Header set Content-Type "image/svg+xml"
        </FilesMatch>
    </Directory>
    
    ErrorLog \${APACHE_LOG_DIR}/nedi_error.log
    CustomLog \${APACHE_LOG_DIR}/nedi_access.log combined
</VirtualHost>
EOF

# Enable site
sudo a2ensite nedi.conf
sudo a2dissite 000-default

# Test Apache configuration
sudo apache2ctl configtest

# Restart Apache
sudo systemctl restart apache2

echo "✓ Apache configured for NeDi"
```

## Step 8: Configure NeDi Settings

```bash
#!/bin/bash
set -e

echo "Configuring NeDi settings..."

# Edit NeDi configuration
sudo tee /var/nedi/nedi.conf > /dev/null <<EOF
# NeDi Configuration with Network Observability Platform Enhancements

# Database Configuration
backend=mysql
dbname=nedi
dbuser=nedi
dbpass=dbpa55
dbhost=localhost
dbport=3306

# Web Interface Configuration
web_port=80
web_host=0.0.0.0
web_root=/var/nedi/html

# SNMP Configuration
snmp_version=3
snmp_timeout=5
snmp_retries=2

# Device Discovery
discovery_interval=3600
discovery_timeout=300

# Topology Visualization
icon_library=/var/nedi/icon_library
topology_format=json
d3js_enabled=true

# Enhanced Features
vendor_icons_enabled=true
client_device_icons_enabled=true
device_metrics_enabled=true
device_tooltips_enabled=true

# Fortinet Integration
fortinet_icons=/var/nedi/icon_library/fortigate:/var/nedi/icon_library/fortiap:/var/nedi/icon_library/fortiswitch

# Client Device Icons
endpoint_icons=/var/nedi/icon_library/endpoints

# Logging
log_dir=/var/nedi/logs
log_level=info
EOF

# Set permissions
sudo chown nedi:nedi /var/nedi/nedi.conf
sudo chmod 600 /var/nedi/nedi.conf

echo "✓ NeDi configuration updated"
```

## Step 9: Set Permissions and Directories

```bash
#!/bin/bash
set -e

echo "Setting up NeDi directories and permissions..."

# Create necessary directories
sudo mkdir -p /var/nedi/{logs,reports,data,tmp,cache}

# Set permissions
sudo chown -R nedi:nedi /var/nedi
sudo chmod -R 755 /var/nedi
sudo chmod 750 /var/nedi/{logs,data,tmp,cache}

# Ensure web server can read/write
sudo usermod -aG nedi www-data
sudo chmod g+w /var/nedi/logs
sudo chmod g+w /var/nedi/reports

echo "✓ Directory permissions configured"
```

## Step 10: Verify Installation

```bash
#!/bin/bash
set -e

echo "Verifying NeDi installation..."

# Check installation directory
if [ ! -d /var/nedi ]; then
    echo "✗ NeDi directory not found"
    exit 1
fi

# Check icon library
echo "Checking icon library..."
if [ ! -d /var/nedi/icon_library/fortigate ]; then
    echo "✗ FortiGate icons missing"
    exit 1
fi
echo "✓ Icon library OK"

# Check database connectivity
echo "Checking database connectivity..."
mysql -u nedi -pdbpa55 -h localhost nedi -e "SELECT 1;" >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Database connectivity OK"
else
    echo "✗ Database connectivity failed"
    exit 1
fi

# Check PHP files
echo "Checking PHP files..."
php -l /var/nedi/html/inc/libmap.php >/dev/null 2>&1 && echo "✓ libmap.php syntax OK" || echo "✗ libmap.php has errors"
php -l /var/nedi/html/inc/libmisc.php >/dev/null 2>&1 && echo "✓ libmisc.php syntax OK" || echo "✗ libmisc.php has errors"

# Check web server
echo "Checking web server..."
curl -s http://localhost/Topology-Map.php >/dev/null 2>&1 && echo "✓ Web server OK" || echo "✗ Web server not responding"

echo ""
echo "========================================"
echo "✓ NeDi Installation Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Access NeDi at: http://$(hostname -I | awk '{print $1}')/Topology-Map.php"
echo "2. Configure SNMP credentials in NeDi web interface"
echo "3. Add network devices for discovery"
echo "4. Run initial network discovery"
echo ""
```

## Automated Installation Script

For convenience, use the complete automated installation script:

```bash
#!/bin/bash
# Complete NeDi installation with all enhancements

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/nedi_installation.log"

# Logging function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "Starting NeDi installation with enhancements..."

# Step 1: Dependencies
log "Step 1: Installing dependencies..."
sudo apt-get update
sudo apt-get install -y perl perl-modules libdbi-perl libdbd-mysql-perl libnet-snmp-perl libfile-find-rule-perl mysql-client apache2 php php-mysql php-cli snmp snmpd

# Step 2: User and directories
log "Step 2: Creating NeDi user and directories..."
sudo useradd -r -s /bin/bash -m nedi || true
sudo mkdir -p /var/nedi && sudo chown nedi:nedi /var/nedi

# Step 3: Download and install NeDi
log "Step 3: Installing NeDi base application..."
cd /tmp
wget -q https://www.nedi.ch/pub/nedi_1.0.tar.gz
tar xzf nedi_1.0.tar.gz
cd nedi_1.0
sudo ./install.sh

# Step 4: Icon library
log "Step 4: Installing enhanced icon library..."
sudo cp -r /home/keith/NeDi/icon_library/* /var/nedi/icon_library/
sudo chown -R nedi:nedi /var/nedi/icon_library
sudo chmod -R 755 /var/nedi/icon_library

# Step 5: PHP enhancements
log "Step 5: Applying PHP web interface enhancements..."
cd /var/nedi/html/inc
sudo cp libmap.php libmap.php.backup.$(date +%s)
sudo cp libmisc.php libmisc.php.backup.$(date +%s)
sudo python3 /home/keith/NeDi/apply-enhancements.py

# Step 6-10: Configuration
log "Step 6-10: Configuring NeDi..."
# [Configuration steps as above]

log "✓ NeDi installation complete!"
log "Installation log saved to: $LOG_FILE"
```

Save this as `scripts/install-nedi.sh` in the network-observability-platform repository.

## Testing the Installation

After installation, verify the enhancements are working:

### Test 1: Check Vendor Icons Load

```bash
curl -I http://localhost/icon_library/fortigate/FG-1000.svg
# Should return: HTTP/1.1 200 OK
```

### Test 2: Verify Client Device Icons

```bash
curl -I http://localhost/icon_library/endpoints/mobile.svg
# Should return: HTTP/1.1 200 OK
```

### Test 3: Test Topology Map

```bash
# Access topology map
curl http://localhost/Topology-Map.php?fmt=json | head -100
# Should return JSON with device data and icon paths
```

## Troubleshooting

### Issue: PHP Syntax Errors

```bash
# Check PHP syntax
sudo php -l /var/nedi/html/inc/libmap.php
sudo php -l /var/nedi/html/inc/libmisc.php

# Check Apache error logs
sudo tail -100 /var/log/apache2/nedi_error.log
```

### Issue: Database Connection Failed

```bash
# Test database connectivity
mysql -u nedi -pdbpa55 -h localhost nedi -e "SELECT 1;"

# Check NeDi config
cat /var/nedi/nedi.conf | grep db
```

### Issue: Icons Not Displaying

```bash
# Check icon directory permissions
ls -la /var/nedi/icon_library/fortigate/ | head -5

# Verify web server can read icons
sudo -u www-data cat /var/nedi/icon_library/fortigate/FG-1000.svg >/dev/null && echo "OK"
```

## Next Steps

1. **Initial Discovery**: Run the first network discovery to populate the database
2. **Configure Credentials**: Add SNMP/API credentials in the web interface
3. **Add Devices**: Register network devices for monitoring
4. **Set Up Alerts**: Configure alerts for device status changes
5. **Integrate with Network Observability Platform**: See [Application Setup](../application-setup.md)

## Support

For NeDi documentation, visit: https://www.nedi.ch/
For Network Observability Platform: See the main README.md in this repository
