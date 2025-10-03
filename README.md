# NIC Control Panel

A user-friendly tool for managing multiple Network Interface Card (NIC) configuration changes efficiently.

## Overview

The NIC Control Panel simplifies the process of managing network interface configurations across multiple NICs. Whether you need to change IP addresses, subnet masks, DNS servers, or other network settings, this tool provides an easier way to handle these tasks.

## Features

- Manage multiple network interface cards simultaneously
- Configure IP addresses, subnet masks, and gateways
- Update DNS server settings
- Enable/disable network interfaces
- Save and restore network configurations
- Cross-platform support (planned)

## Requirements

- Python 3.7 or higher (if applicable)
- Administrator/root privileges for network configuration changes
- Supported operating systems:
  - Windows 10/11
  - Linux (Ubuntu, Debian, RHEL, CentOS)
  - macOS (planned)

## Installation

```bash
# Clone the repository
git clone https://github.com/jaredewoods/nic_control_panel.git

# Navigate to the project directory
cd nic_control_panel

# Install dependencies (if any)
pip install -r requirements.txt
```

## Usage

```bash
# Run the control panel
python nic_control_panel.py

# Or with specific options
python nic_control_panel.py --list-interfaces
python nic_control_panel.py --configure <interface_name>
```

### Basic Examples

```bash
# List all available network interfaces
python nic_control_panel.py --list

# Configure a specific interface
python nic_control_panel.py --interface eth0 --ip 192.168.1.100 --netmask 255.255.255.0

# Save current configuration
python nic_control_panel.py --save-config config.json

# Restore configuration from file
python nic_control_panel.py --restore-config config.json
```

## Configuration

Configuration files are stored in JSON format and can be easily edited:

```json
{
  "interface": "eth0",
  "ip_address": "192.168.1.100",
  "netmask": "255.255.255.0",
  "gateway": "192.168.1.1",
  "dns": ["8.8.8.8", "8.8.4.4"]
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions, please file an issue on the GitHub repository.

## Roadmap

- [ ] GUI interface
- [ ] Batch configuration support
- [ ] Configuration templates
- [ ] Network diagnostics integration
- [ ] macOS support
- [ ] Docker container support

## Acknowledgments

- Thanks to all contributors who have helped with the project
- Inspired by the need for simpler network management tools
