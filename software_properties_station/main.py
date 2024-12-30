#!/usr/bin/env python3
# File: software_properties_station/main.py

import sys
import os
import logging

# Set up application paths
APP_BASE_DIR = os.getenv("SOFTWARE_PROPERTIES_BASE", "/usr/share/software-properties-station")
CONFIG_DIR = os.path.join(APP_BASE_DIR, "config")
REPO_DIR = os.path.join(APP_BASE_DIR, "repo")
UI_DIR = os.path.join(APP_BASE_DIR, "ui")

# Add directories to the Python path
sys.path.extend([CONFIG_DIR, REPO_DIR, UI_DIR])

try:
    from config.config import load_repos  # Import from config module
    from repo.ghostbsd_repo_manager import update_config, list_repos  # Import repository management
    from ui.ui import start_gui  # Import the GUI start function
except ImportError as e:
    print(f"Error: Failed to import required modules: {e}")
    sys.exit(1)

LOG_FILE = '/var/log/software-properties-station/software-properties-station.log'

def setup_logging():
    """
    Set up logging to a file or console if permissions are insufficient.
    """
    log_dir = os.path.dirname(LOG_FILE)
    if not os.access(log_dir, os.W_OK):
        print(f"Warning: Cannot write to {log_dir}. Falling back to console logging.")
        logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main entry point for the application. Determines if CLI or GUI mode is used.
    """
    setup_logging()

    if len(sys.argv) > 1:
        # Check if the user passed --gui as an argument
        if sys.argv[1] == '--gui':
            print("Starting in GUI mode...")
            gui_mode()
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print_usage()
    else:
        print("Starting in CLI mode...")
        cli_mode()

def cli_mode():
    """
    Run the CLI interface to manage repositories.
    """
    try:
        repos = list_repos()
        if repos:
            print("Available repositories:")
            for repo in repos:
                print(f"- {repo}")

            selected_repo = input("Select a repository: ").strip()
            if os.geteuid() == 0:  # Ensure the user is root
                success, message = update_config(selected_repo)
                if success:
                    print(f"Repository '{selected_repo}' selected successfully.")
                else:
                    print(f"Error: {message}")
            else:
                print("Running in read-only mode. Repository selection not available.")
        else:
            print("No repositories found.")
    except Exception as e:
        logging.error(f"Error in CLI mode: {e}")
        print(f"Error: {e}")

def gui_mode():
    """
    Start the GUI interface.
    """
    try:
        start_gui()  # No longer passing 'read_only'
    except Exception as e:
        logging.error(f"Error in GUI mode: {e}")
        print(f"Error: Unable to start GUI. {e}")

def print_usage():
    """
    Print usage information for the software-properties-station.
    """
    print("Usage:")
    print("  sudo software-properties-station            # Start in CLI mode (default)")
    print("  sudo software-properties-station --gui      # Start in GUI mode")

if __name__ == "__main__":
    main()

