#!/usr/bin/env python3
# File: ui.py

import os
import sys
import logging
import gi

# Set the GTK version before importing Gtk
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

# Import centralized privilege management
try:
    from config.privileges import get_privilege_level
    from ui.ghostbsd_repos_tab import GhostBSDReposTab
    from ui.custom_repos_tab import CustomReposTab
except ImportError as e:
    logging.error(f"Error importing modules: {e}")
    sys.exit(1)

TITLE = "Software Properties Station"
WINDOW_WIDTH, WINDOW_HEIGHT = 1024, 480
LOG_FILE = '/var/log/software-properties-station/software-properties-station.log'

def setup_logging():
    log_dir = os.path.dirname(LOG_FILE)
    if not os.access(log_dir, os.W_OK):
        print(f"Warning: Cannot write to {log_dir}. Falling back to console logging.")
        logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

class RepoSelector(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title=TITLE)
        self.set_default_size(WINDOW_WIDTH, WINDOW_HEIGHT)

        privilege_level = get_privilege_level()

        # Header Bar
        header_bar = Gtk.HeaderBar()
        header_bar.set_show_title_buttons(True)
        title_label = Gtk.Label(label=TITLE)
        header_bar.set_title_widget(title_label)
        self.set_titlebar(header_bar)

        # Main layout
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(main_vbox)

        # Privilege level label
        privilege_label = Gtk.Label(label=f"Privilege level: {privilege_level}")
        privilege_label.set_halign(Gtk.Align.START)
        main_vbox.prepend(privilege_label)  # Corrected line to prepend

        # Stack and StackSwitcher for tabs
        stack = Gtk.Stack()
        stack_switcher = Gtk.StackSwitcher(stack=stack)
        stack_switcher.set_halign(Gtk.Align.START)
        main_vbox.append(stack_switcher)

        ghostbsd_repos_tab = GhostBSDReposTab(privilege_level=privilege_level)
        stack.add_titled(ghostbsd_repos_tab, "ghostbsd_repos", "GhostBSD Repositories")

        custom_repos_tab = CustomReposTab(privilege_level=privilege_level)
        stack.add_titled(custom_repos_tab, "custom_repos", "Custom Repositories")

        main_vbox.append(stack)

        # Quit button
        quit_button = Gtk.Button(label="Quit")
        quit_button.connect("clicked", self.on_quit)
        button_box = Gtk.Box(spacing=6)
        button_box.set_halign(Gtk.Align.END)
        button_box.append(quit_button)
        main_vbox.append(button_box)

    def on_quit(self, widget):
        self.get_application().quit()

class SoftwarePropertiesApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.ghostbsd.software-properties")

    def do_activate(self):
        win = RepoSelector(self)
        win.present()

def start_gui():
    setup_logging()
    app = SoftwarePropertiesApp()
    app.run(None)

if __name__ == "__main__":
    start_gui()

