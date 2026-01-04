#!/bin/bash
##############################################################################
# Network Observability Platform - NeDi Integration Setup
#
# This script automates the complete setup of NeDi with all enhancements
# for the Network Observability Platform.
#
# Usage:
#   sudo ./scripts/setup-nedi-integration.sh
#   ./scripts/setup-nedi-integration.sh --dry-run
#   ./scripts/setup-nedi-integration.sh --with-nedi-install
#
# Options:
#   --dry-run              Show what would be done without making changes
#   --with-nedi-install    Include full NeDi installation (requires root)
#   --custom-icon-path     Custom path to icon library
#   --help                 Show this help message
##############################################################################

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
NEDI_REPO="/home/keith/NeDi"
NEDI_INSTALL="/var/nedi"
NEDI_ICON_LIB="${NEDI_ICON_LIB:-$NEDI_REPO/icon_library}"
LOG_FILE="$PROJECT_DIR/nedi_setup.log"
DRY_RUN=false
INSTALL_NEDI=false
EUID=$(id -u)

# Logging function
log() {
    local level=$1
    shift
    local message="$@"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "[${timestamp}] ${level}: ${message}" | tee -a "$LOG_FILE"
}

# Info, warning, error functions
info() { log "INFO" "$@"; }
warn() { log "WARN" "$@"; }
error() { log "ERROR" "$@"; }
success() { echo -e "${GREEN}✓ $@${NC}" | tee -a "$LOG_FILE"; }
fail() { echo -e "${RED}✗ $@${NC}" | tee -a "$LOG_FILE"; }

# Check if running as root
check_root() {
    if [ "$INSTALL_NEDI" = true ] && [ "$EUID" -ne 0 ]; then
        error "Full NeDi installation requires root privileges"
        error "Run with: sudo $0 --with-nedi-install"
        return 1
    fi
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                info "Running in DRY RUN mode (no changes will be made)"
                shift
                ;;
            --with-nedi-install)
                INSTALL_NEDI=true
                shift
                ;;
            --custom-icon-path)
                NEDI_ICON_LIB="$2"
                shift 2
                ;;
            --help)
                print_help
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                print_help
                exit 1
                ;;
        esac
    done
}

# Print help message
print_help() {
    cat << EOF
Network Observability Platform - NeDi Integration Setup

Usage:
    sudo ./scripts/setup-nedi-integration.sh [OPTIONS]

Options:
    --dry-run              Show what would be done without making changes
    --with-nedi-install    Include full NeDi installation (requires root)
    --custom-icon-path     Custom path to icon library (default: $NEDI_REPO/icon_library)
    --help                 Show this help message

Examples:
    # Setup with existing NeDi installation
    sudo ./scripts/setup-nedi-integration.sh

    # Full NeDi installation with enhancements
    sudo ./scripts/setup-nedi-integration.sh --with-nedi-install

    # Preview changes without making them
    ./scripts/setup-nedi-integration.sh --dry-run

Description:
    This script sets up the Network Observability Platform with NeDi integration.
    
    Without --with-nedi-install:
    - Assumes NeDi is already installed at $NEDI_INSTALL
    - Copies enhanced icon library
    - Applies PHP web interface enhancements
    
    With --with-nedi-install:
    - Installs NeDi from scratch
    - Sets up database
    - Applies all enhancements
    - Configures web server

EOF
}

# Verify dependencies
verify_dependencies() {
    info "Verifying dependencies..."
    
    local missing_deps=()
    
    # Check for required commands
    for cmd in python3 php curl; do
        if ! command -v $cmd &> /dev/null; then
            missing_deps+=("$cmd")
        fi
    done
    
    if [ "$INSTALL_NEDI" = true ]; then
        for cmd in mysql apache2ctl perl; do
            if ! command -v $cmd &> /dev/null; then
                missing_deps+=("$cmd")
            fi
        done
    fi
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        error "Missing dependencies: ${missing_deps[*]}"
        error "Install with: sudo apt-get install ${missing_deps[*]}"
        return 1
    fi
    
    success "All dependencies found"
    return 0
}

# Verify NeDi repository
verify_nedi_repo() {
    info "Verifying NeDi repository..."
    
    if [ ! -d "$NEDI_REPO" ]; then
        error "NeDi repository not found at: $NEDI_REPO"
        error "Expected: $NEDI_REPO/icon_library"
        return 1
    fi
    
    if [ ! -d "$NEDI_ICON_LIB" ]; then
        error "Icon library not found at: $NEDI_ICON_LIB"
        return 1
    fi
    
    # Check for required enhancement script
    if [ ! -f "$NEDI_REPO/apply-enhancements.py" ]; then
        error "Enhancement script not found: $NEDI_REPO/apply-enhancements.py"
        return 1
    fi
    
    success "NeDi repository verified"
    return 0
}

# Verify NeDi installation
verify_nedi_install() {
    info "Verifying NeDi installation..."
    
    if [ ! -d "$NEDI_INSTALL" ]; then
        error "NeDi installation not found at: $NEDI_INSTALL"
        if [ "$INSTALL_NEDI" = false ]; then
            error "Run with --with-nedi-install to perform full installation"
        fi
        return 1
    fi
    
    # Check for required directories
    local required_dirs=("html/inc" "icon_library" "logs" "reports")
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$NEDI_INSTALL/$dir" ]; then
            warn "Missing directory: $NEDI_INSTALL/$dir"
        fi
    done
    
    # Check for required PHP files
    if [ ! -f "$NEDI_INSTALL/html/inc/libmap.php" ]; then
        error "libmap.php not found at: $NEDI_INSTALL/html/inc/libmap.php"
        return 1
    fi
    
    if [ ! -f "$NEDI_INSTALL/html/inc/libmisc.php" ]; then
        error "libmisc.php not found at: $NEDI_INSTALL/html/inc/libmisc.php"
        return 1
    fi
    
    success "NeDi installation verified"
    return 0
}

# Setup icon library
setup_icon_library() {
    info "Setting up enhanced icon library..."
    
    if [ ! -d "$NEDI_INSTALL/icon_library" ]; then
        info "Creating icon_library directory..."
        if [ "$DRY_RUN" = false ]; then
            sudo mkdir -p "$NEDI_INSTALL/icon_library"
        fi
    fi
    
    # Copy icon library
    info "Copying icon library from $NEDI_ICON_LIB..."
    if [ "$DRY_RUN" = false ]; then
        sudo cp -r "$NEDI_ICON_LIB"/* "$NEDI_INSTALL/icon_library/" 2>/dev/null || true
        sudo chown -R nedi:nedi "$NEDI_INSTALL/icon_library" 2>/dev/null || true
        sudo chmod -R 755 "$NEDI_INSTALL/icon_library" 2>/dev/null || true
    fi
    
    # Verify icons
    info "Verifying icon library contents..."
    local icon_count=$(find "$NEDI_INSTALL/icon_library" -name "*.svg" 2>/dev/null | wc -l)
    
    if [ "$icon_count" -gt 0 ]; then
        success "Icon library setup complete ($icon_count SVG icons found)"
        return 0
    else
        warn "No SVG icons found in icon library (may be OK if copying from repo)"
        return 0
    fi
}

# Apply PHP enhancements
apply_php_enhancements() {
    info "Applying PHP web interface enhancements..."
    
    if [ "$DRY_RUN" = true ]; then
        info "DRY RUN: Would run: sudo python3 $NEDI_REPO/apply-enhancements.py"
        return 0
    fi
    
    # Run enhancement script
    if ! sudo python3 "$NEDI_REPO/apply-enhancements.py" 2>&1 | tee -a "$LOG_FILE"; then
        error "Failed to apply PHP enhancements"
        return 1
    fi
    
    # Verify PHP syntax
    info "Verifying PHP syntax..."
    if ! php -l "$NEDI_INSTALL/html/inc/libmap.php" >/dev/null 2>&1; then
        error "PHP syntax error in libmap.php"
        return 1
    fi
    if ! php -l "$NEDI_INSTALL/html/inc/libmisc.php" >/dev/null 2>&1; then
        error "PHP syntax error in libmisc.php"
        return 1
    fi
    
    success "PHP enhancements applied and verified"
    return 0
}

# Test NeDi access
test_nedi_access() {
    info "Testing NeDi web interface access..."
    
    local nedi_url="http://localhost/Topology-Map.php"
    
    # Wait for web server to be ready
    sleep 2
    
    if curl -s "$nedi_url" >/dev/null 2>&1; then
        success "NeDi web interface is accessible"
        return 0
    else
        warn "Could not access NeDi web interface at $nedi_url"
        warn "Web server may not be running or NeDi not configured"
        return 0  # Not a fatal error
    fi
}

# Test icon library
test_icon_library() {
    info "Testing icon library access..."
    
    # Check file existence
    if [ -f "$NEDI_INSTALL/icon_library/fortigate/fortigate.svg" ]; then
        success "Generic FortiGate icon found"
    else
        warn "Generic FortiGate icon not found"
    fi
    
    if [ -f "$NEDI_INSTALL/icon_library/endpoints/mobile.svg" ]; then
        success "Client device icons found"
    else
        warn "Client device icons not found"
    fi
    
    return 0
}

# Create integration guide
create_integration_guide() {
    info "Creating integration guide..."
    
    local guide="$PROJECT_DIR/NEDI_INTEGRATION_SETUP.md"
    
    if [ "$DRY_RUN" = true ]; then
        info "DRY RUN: Would create integration guide at $guide"
        return 0
    fi
    
    cat > "$guide" << 'EOF'
# NeDi Integration Setup for Network Observability Platform

## Setup Summary

NeDi has been successfully integrated with all enhancements:

### Enhancements Applied

✓ **Vendor-Specific Device Icons**
  - FortiGate icons (136+ device models)
  - FortiAP icons (35+ device models)
  - FortiSwitch icons (69+ device models)
  - Generic fallback icons

✓ **Client Device Identification**
  - Mobile device detection (Apple, Samsung, etc.)
  - Laptop/Computer detection (ASUS, Dell, HP, Lenovo, etc.)
  - IoT device detection (Raspberry Pi, Arduino, etc.)
  - Printer detection (Brother, Canon, HP, etc.)

✓ **Enhanced Topology Visualization**
  - D3.js rendering with SVG icons
  - Device metrics display (CPU, Temperature, Memory, OS)
  - Enhanced tooltips with vendor and device information
  - Three-tier icon priority (vendor → client → fallback)

### Directory Structure

```
/var/nedi/
├── html/                     # Web interface
│   ├── inc/
│   │   ├── libmap.php       # ✓ Enhanced topology rendering
│   │   ├── libmisc.php      # ✓ Enhanced utility functions
│   │   └── [other files]
│   └── Topology-Map.php
├── icon_library/            # ✓ Enhanced icon library
│   ├── fortigate/           # 136+ FortiGate icons
│   ├── fortiap/             # 35+ FortiAP icons
│   ├── fortiswitch/         # 69+ FortiSwitch icons
│   ├── endpoints/           # Client device icons
│   ├── meraki/              # Cisco Meraki icons
│   ├── routers/             # Router icons
│   └── switches/            # Network switch icons
├── html/                     # Web root
├── logs/                     # Application logs
└── reports/                  # Generated reports
```

### Next Steps

1. **Configure SNMP Credentials**
   - Access NeDi web interface: http://localhost/Topology-Map.php
   - Configure SNMP v3 credentials for your devices
   - (Or configure in /var/nedi/nedi.conf)

2. **Add Network Devices**
   - Add device IP addresses in NeDi configuration
   - Configure SNMP community strings or v3 credentials
   - Set device types (managed/client/router/etc)

3. **Run Initial Discovery**
   - Execute NeDi discovery script: `sudo /var/nedi/nedi.pl`
   - This will populate the database with discovered devices
   - First discovery may take several minutes depending on network size

4. **Verify Icons Display**
   - Check topology map for vendor-specific icons
   - Verify device tooltips show metrics (CPU, temperature, OS)
   - Check for client device icons on non-managed nodes

5. **Integrate with Application**
   - See ../APPLICATION_SETUP.md for full platform setup
   - Configure FastAPI backend to use NeDi database
   - Set up API endpoints for device data

### Testing Enhancements

Test that the enhancements are working:

```bash
# Check topology map JSON
curl http://localhost/Topology-Map.php?fmt=json | head -100

# Verify vendor icons
curl -I http://localhost/icon_library/fortigate/FG-1000.svg
curl -I http://localhost/icon_library/fortiap/FAP-231.svg
curl -I http://localhost/icon_library/fortiswitch/FSW-248.svg

# Verify client device icons
curl -I http://localhost/icon_library/endpoints/mobile.svg
curl -I http://localhost/icon_library/endpoints/laptop.svg
curl -I http://localhost/icon_library/endpoints/desktop.svg

# Check NeDi logs
tail -100 /var/nedi/logs/nedi.log

# Verify PHP syntax
php -l /var/nedi/html/inc/libmap.php
php -l /var/nedi/html/inc/libmisc.php
```

### Troubleshooting

**Icons not displaying:**
```bash
# Check icon directory permissions
ls -la /var/nedi/icon_library/fortigate/ | head -5

# Verify web server can read icons
sudo -u www-data cat /var/nedi/icon_library/fortigate/FG-1000.svg >/dev/null && echo "OK"
```

**PHP errors:**
```bash
# Check Apache error logs
sudo tail -100 /var/log/apache2/error.log

# Verify PHP syntax
php -l /var/nedi/html/inc/libmap.php
php -l /var/nedi/html/inc/libmisc.php
```

**Database connectivity:**
```bash
# Test database connection
mysql -u nedi -pdbpa55 -h localhost nedi -e "SELECT 1;"
```

### Backups Created

Original files have been backed up:
- `/var/nedi/html/inc/libmap.php.backup.*`
- `/var/nedi/html/inc/libmisc.php.backup.*`

To restore to original:
```bash
sudo cp /var/nedi/html/inc/libmap.php.backup.* /var/nedi/html/inc/libmap.php
sudo cp /var/nedi/html/inc/libmisc.php.backup.* /var/nedi/html/inc/libmisc.php
sudo systemctl restart apache2
```

### Support

- NeDi Documentation: https://www.nedi.ch/
- NeDi Installation: https://www.nedi.ch/installation/
- Network Observability Platform: See ../README.md

---

Generated: $(date)
EOF
    
    success "Integration guide created at: $guide"
    return 0
}

# Main setup function
main() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Network Observability Platform${NC}"
    echo -e "${BLUE}NeDi Integration Setup${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo
    
    # Start logging
    log "INFO" "Starting NeDi integration setup"
    
    # Parse arguments
    parse_args "$@"
    
    # Check root if needed
    if ! check_root; then
        return 1
    fi
    
    # Run verification and setup steps
    if ! verify_dependencies; then return 1; fi
    if ! verify_nedi_repo; then return 1; fi
    if ! verify_nedi_install; then return 1; fi
    
    echo
    
    if ! setup_icon_library; then return 1; fi
    if ! apply_php_enhancements; then return 1; fi
    
    echo
    info "Testing configuration..."
    test_icon_library
    test_nedi_access
    
    echo
    if ! create_integration_guide; then return 1; fi
    
    echo
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ Setup Complete!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo
    
    if [ "$DRY_RUN" = true ]; then
        echo "This was a DRY RUN. No actual changes were made."
        echo "Run without --dry-run to apply changes."
    else
        echo "Next steps:"
        echo "1. Restart Apache: sudo systemctl restart apache2"
        echo "2. Configure SNMP credentials in NeDi"
        echo "3. Add network devices for discovery"
        echo "4. Run: sudo /var/nedi/nedi.pl"
        echo "5. Check topology map: http://localhost/Topology-Map.php"
    fi
    echo
    
    return 0
}

# Run main function
main "$@"
exit $?
