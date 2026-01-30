<?php
/**
 * NeDi Topology Mapper with Vendor-Specific Icons
 *
 * Integrates with NeDi discovered topology data and applies vendor-specific icons
 * to network devices. Can be included in NeDi topology visualization pages.
 *
 * Usage:
 *   require_once('/home/keith/network-observability-platform/nedi_topology_mapper.php');
 *   $mapper = new NeDiTopologyMapper();
 *   $devices = $mapper->get_devices_with_icons('SELECT * FROM nodes');
 */

class NeDiTopologyMapper {
    private $db_connection;
    private $icon_base_path = '/var/nedi/icon_library';
    private $icon_mapping = array();

    // Device type configurations with patterns and styles
    private $device_configs = array(
        'fortigate' => array(
            'vendor' => 'Fortinet',
            'type' => 'infrastructure',
            'category' => 'firewall',
            'icon_dir' => 'fortigate',
            'color' => '#E5A100',
            'priority' => 100,
            'patterns' => array(
                '/FG-\d+/',
                '/FWF-\d+/',
                '/FortiGate/',
                '/Forti.*Gate/'
            ),
            'default_icon' => 'fortigate.svg'
        ),
        'fortiswitch' => array(
            'vendor' => 'Fortinet',
            'type' => 'infrastructure',
            'category' => 'switch',
            'icon_dir' => 'fortiswitch',
            'color' => '#E5A100',
            'priority' => 90,
            'patterns' => array(
                '/FSW-\d+/',
                '/FS-\d+/',
                '/FortiSwitch/',
                '/Forti.*Switch/'
            ),
            'default_icon' => 'fortiswitch.svg'
        ),
        'fortiap' => array(
            'vendor' => 'Fortinet',
            'type' => 'infrastructure',
            'category' => 'access_point',
            'icon_dir' => 'fortiap',
            'color' => '#E5A100',
            'priority' => 85,
            'patterns' => array(
                '/FAP-\d+/',
                '/FortiAP/',
                '/Forti.*AP/'
            ),
            'default_icon' => 'fortiap.svg'
        ),
        'meraki-firewall' => array(
            'vendor' => 'Meraki',
            'type' => 'infrastructure',
            'category' => 'firewall',
            'icon_dir' => 'meraki',
            'color' => '#00BCD4',
            'priority' => 100,
            'patterns' => array(
                '/MX\d+/',
                '/Meraki.*MX/',
                '/Meraki.*Firewall/'
            ),
            'default_icon' => 'meraki-firewall.svg'
        ),
        'meraki-switch' => array(
            'vendor' => 'Meraki',
            'type' => 'infrastructure',
            'category' => 'switch',
            'icon_dir' => 'meraki',
            'color' => '#00BCD4',
            'priority' => 90,
            'patterns' => array(
                '/MS\d+/',
                '/Meraki.*MS/',
                '/Meraki.*Switch/'
            ),
            'default_icon' => 'meraki-switch.svg'
        ),
        'desktop' => array(
            'vendor' => 'Generic',
            'type' => 'endpoint',
            'category' => 'desktop',
            'icon_dir' => 'endpoints',
            'color' => '#34495E',
            'priority' => 10,
            'patterns' => array(
                '/desktop/i',
                '/Desktop/i',
                '/PC/i',
                '/computer/i'
            ),
            'default_icon' => 'desktop.svg'
        ),
        'laptop' => array(
            'vendor' => 'Generic',
            'type' => 'endpoint',
            'category' => 'laptop',
            'icon_dir' => 'endpoints',
            'color' => '#2C3E50',
            'priority' => 10,
            'patterns' => array(
                '/laptop/i',
                '/notebook/i',
                '/MacBook/i'
            ),
            'default_icon' => 'laptop.svg'
        ),
        'mobile' => array(
            'vendor' => 'Generic',
            'type' => 'endpoint',
            'category' => 'mobile',
            'icon_dir' => 'endpoints',
            'color' => '#16A085',
            'priority' => 10,
            'patterns' => array(
                '/mobile/i',
                '/phone/i',
                '/iPhone/i',
                '/iPad/i'
            ),
            'default_icon' => 'mobile.svg'
        )
    );

    /**
     * Initialize the topology mapper
     *
     * @param string $icon_base_path Optional path to icon library
     */
    public function __construct($icon_base_path = '/var/nedi/icon_library') {
        $this->icon_base_path = $icon_base_path;
    }

    /**
     * Get device icon information
     *
     * @param string $sysname Device system name
     * @param string $model Device model
     * @return array Icon information array
     */
    public function get_device_icon($sysname = '', $model = '') {
        // Try to identify device type
        $device_type = $this->identify_device_type($sysname, $model);
        $config = $this->device_configs[$device_type];

        return array(
            'device_type' => $device_type,
            'vendor' => $config['vendor'],
            'category' => $config['category'],
            'icon_path' => $config['icon_dir'] . '/' . $config['default_icon'],
            'icon_file' => $config['default_icon'],
            'color' => $config['color'],
            'type' => $config['type']
        );
    }

    /**
     * Get HTML SVG img tag for device icon
     *
     * @param string $sysname Device system name
     * @param string $model Device model
     * @param int $size Icon size in pixels
     * @return string HTML img tag
     */
    public function get_device_icon_html($sysname = '', $model = '', $size = 32) {
        $icon_info = $this->get_device_icon($sysname, $model);
        $icon_url = '/nedi/icon_library/' . $icon_info['icon_path'];

        $html = '<img src="' . htmlspecialchars($icon_url) . '" ';
        $html .= 'width="' . intval($size) . '" height="' . intval($size) . '" ';
        $html .= 'alt="' . htmlspecialchars($icon_info['vendor'] . ' ' . $icon_info['category']) . '" ';
        $html .= 'style="filter: drop-shadow(0 0 2px ' . $icon_info['color'] . ')" ';
        $html .= 'title="' . htmlspecialchars($icon_info['device_type']) . '" />';

        return $html;
    }

    /**
     * Get device icon URL
     *
     * @param string $sysname Device system name
     * @param string $model Device model
     * @return string Full URL to icon
     */
    public function get_device_icon_url($sysname = '', $model = '') {
        $icon_info = $this->get_device_icon($sysname, $model);
        return '/nedi/icon_library/' . $icon_info['icon_path'];
    }

    /**
     * Identify device type from identifiers
     *
     * @param string $sysname System name
     * @param string $model Model identifier
     * @return string Device type
     */
    public function identify_device_type($sysname = '', $model = '') {
        $identifiers = array_filter(array($sysname, $model));

        foreach ($this->device_configs as $type => $config) {
            foreach ($identifiers as $identifier) {
                foreach ($config['patterns'] as $pattern) {
                    if (preg_match($pattern, $identifier)) {
                        return $type;
                    }
                }
            }
        }

        return 'generic-device';
    }

    /**
     * Get all device types
     *
     * @return array Device type configurations
     */
    public function get_all_device_types() {
        $types = array();
        foreach ($this->device_configs as $type => $config) {
            $types[$type] = array(
                'vendor' => $config['vendor'],
                'category' => $config['category'],
                'color' => $config['color'],
                'type' => $config['type']
            );
        }
        return $types;
    }

    /**
     * Get devices by vendor
     *
     * @param string $vendor Vendor name
     * @return array Array of device configurations
     */
    public function get_devices_by_vendor($vendor) {
        $devices = array();
        foreach ($this->device_configs as $type => $config) {
            if ($config['vendor'] === $vendor) {
                $devices[$type] = $config;
            }
        }
        return $devices;
    }

    /**
     * Get device color by type
     *
     * @param string $sysname Device system name
     * @param string $model Device model
     * @return string Hex color code
     */
    public function get_device_color($sysname = '', $model = '') {
        $device_type = $this->identify_device_type($sysname, $model);
        return $this->device_configs[$device_type]['color'];
    }

    /**
     * Export device types as JSON
     *
     * @return string JSON representation
     */
    public function export_device_types_json() {
        return json_encode($this->get_all_device_types(), JSON_PRETTY_PRINT);
    }

    /**
     * Generate SVG device icon with styling
     *
     * @param string $sysname Device system name
     * @param string $model Device model
     * @param int $size Icon size
     * @return string SVG string or img tag
     */
    public function generate_styled_icon($sysname = '', $model = '', $size = 40) {
        $icon_info = $this->get_device_icon($sysname, $model);

        $svg = '<g transform="translate(0, 0)">';
        $svg .= '  <circle cx="' . ($size/2) . '" cy="' . ($size/2) . '" r="' . ($size/2 - 2) . '" ';
        $svg .= '    fill="' . $icon_info['color'] . '" opacity="0.1" />';
        $svg .= '  <circle cx="' . ($size/2) . '" cy="' . ($size/2) . '" r="' . ($size/2 - 2) . '" ';
        $svg .= '    fill="none" stroke="' . $icon_info['color'] . '" stroke-width="1" />';
        $svg .= '  <image x="' . (($size - 24) / 2) . '" y="' . (($size - 24) / 2) . '" ';
        $svg .= '    width="24" height="24" ';
        $svg .= '    xlink:href="' . $this->get_device_icon_url($sysname, $model) . '" />';
        $svg .= '</g>';

        return $svg;
    }
}

// Helper functions for template use
function nedi_get_device_icon($sysname = '', $model = '', $size = 32) {
    static $mapper = null;
    if (!$mapper) {
        $mapper = new NeDiTopologyMapper();
    }
    return $mapper->get_device_icon_html($sysname, $model, $size);
}

function nedi_get_device_color($sysname = '', $model = '') {
    static $mapper = null;
    if (!$mapper) {
        $mapper = new NeDiTopologyMapper();
    }
    return $mapper->get_device_color($sysname, $model);
}

function nedi_get_device_type($sysname = '', $model = '') {
    static $mapper = null;
    if (!$mapper) {
        $mapper = new NeDiTopologyMapper();
    }
    return $mapper->identify_device_type($sysname, $model);
}

?>
