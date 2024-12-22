# software-properties-station

The `software-properties-station` app is a simple graphical and command-line application to manage and select package repositories for GhostBSD. It provides a user-friendly interface for switching between different repository mirrors, making it easy to update and configure the system's package sources.

## Features

- **Graphical Interface**: Easy-to-use GTK-based GUI for selecting package repositories.
- **Command-line Interface**: Allows repository management directly from the CLI.
- **Custom Repositories**: Easily add and remove custom repositories through the interface.
- **Validation**: Ensures the configuration file is valid after updating the repository.
- **Logging**: Logs actions and errors for troubleshooting.

## Requirements

- Python 3.11+
- GTK 4.0+
- GhostBSD
- `PyGObject` (GTK bindings for Python)
- `pip`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ghostbsd/software-properties-station.git
   cd software-properties-station
   ```

2. Install the required dependencies:
   ```bash
   sudo pkg install gtk4 pygobject3-common
   ```

3. Install the application using `pip`:
   ```bash
   sudo pip install . 
   ```

4. Create a directory for the `.log` file:
   ```bash
   sudo mkdir /var/log/software-properties-station
   ```

## Usage

### Graphical Interface

1. To launch the graphical interface, run:
   ```bash
   sudo software-properties-station --gui
   ```

2. Select the desired repository from the list of GhostBSD repositories or add a custom repository.
3. Confirm the selection when prompted.
4. The application will update the repository URLs and validate the new configuration.

### Command-line Interface

1. List available repositories:
   ```bash
   sudo software-properties-station --list
   ```

2. Show the current repository:
   ```bash
   sudo software-properties-station --current
   ```

3. Select a repository:
   ```bash
   sudo software-properties-station <repo_name>
   ```
   Replace `<repo_name>` with the name of the repository you want to select, such as `GhostBSD_France`.

### Custom Repositories

1. Add a custom repository by selecting the **Custom Repositories** tab in the GUI.
2. Fill in the repository name, URL, base URL, and optionally the public key.
3. Save the repository, and it will appear in the list of available repositories.

## Configuration

The main configuration file is located at `/etc/pkg/GhostBSD.conf`. Custom repositories are stored in the `/etc/pkg/` directory, each with its own `.conf` file.

### Example Configuration:

```ini
GhostBSD: {
  url: "https://pkg.ghostbsd.org/unstable/${ABI}/latest",
  signature_type: "pubkey",
  pubkey: "/usr/share/keys/ssl/certs/ghostbsd.cert",
  enabled: yes
}
GhostBSD-base: {
  url: "https://pkg.ghostbsd.org/unstable/${ABI}/base",
  signature_type: "pubkey",
  pubkey: "/usr/share/keys/ssl/certs/ghostbsd.cert",
  enabled: yes
}
```

## Logging

Logs are written to `/var/log/software-properties-station/software-properties-station.log`. Check this file for any errors or information about the application's operations.

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

