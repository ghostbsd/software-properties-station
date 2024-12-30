# Software Properties Station

## Overview
Software Properties Station is a GUI and CLI tool for managing package repositories on GhostBSD. It allows users to enable or disable repositories, add custom repositories, and update configurations dynamically.

---

## Features

1. **Graphical User Interface (GUI)**:
    - Enable or disable repositories using checkboxes.
    - Dynamically update the `/usr/local/etc/pkg/repos/GhostBSD.conf` file.
    - Read-only mode for non-root users.

2. **Command-Line Interface (CLI)**:
    - View available repositories.
    - Enable or disable repositories.
    - Add or remove custom repositories.

3. **Custom Repository Management**:
    - Add custom repositories with URLs and optional public keys.
    - Remove existing custom repositories.

4. **Dynamic Configuration Updates**:
    - Automatically updates the configuration file when repository selections change.

---

## Requirements

- **Python**: version 3.6 or later.
- **GTK 4**: For the GUI.
- **Root Privileges**: Required for modifying system configuration files.

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ghostbsd/software-properties-station.git
    cd software-properties-station
    ```

2. Build and install using the Makefile:
    ```bash
    sudo make install
    ```

3. (Optional) Run tests to verify the installation:
    ```bash
    make test
    ```

---

## Usage

### GUI Mode
To start the application in GUI mode:
```bash
sudo software-properties-station --gui
```

### CLI Mode
To start the application in CLI mode:
```bash
sudo software-properties-station
```

---

## Configuration File
The main configuration file is located at:
```
/usr/local/etc/pkg/repos/GhostBSD.conf
```

### Example Configuration
The configuration uses the following variables:
- `${ABI}`: System architecture and version (e.g., "FreeBSD:13:amd64" for 64-bit FreeBSD 13)

```plaintext
GhostBSD: {
  url: "https://pkg.ghostbsd.org/stable/${ABI}/latest",
  signature_type: "pubkey",
  pubkey: "/usr/share/keys/ssl/certs/ghostbsd.cert",
  enabled: yes
}
GhostBSD-base: {
  url: "https://pkg.ghostbsd.org/stable/${ABI}/base",
  signature_type: "pubkey",
  pubkey: "/usr/share/keys/ssl/certs/ghostbsd.cert",
  enabled: yes
}
```

---

## Development

### Run Tests
To run the unit tests:
```bash
make test
```

### Contribution Guidelines
1. Fork the repository.
2. Create a feature branch.
3. Make your changes and add tests.
4. Submit a pull request.

---

## Known Issues
- Non-root users cannot modify the configuration file and are limited to read-only mode.
- Ensure that GTK 4 is properly installed for the GUI to work.

---

## License
This project is licensed under the BSD 3-Clause License. See the [LICENSE](LICENSE) file for details.

---

## Support
For issues or feature requests, please open an issue on the [GitHub repository](https://github.com/ghostbsd/software-properties-station/issues).

---

## Tests

### Basic Test Script: `tests/tests_basic.py`

