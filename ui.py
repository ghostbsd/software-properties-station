#!/usr/bin/env python3.11

import os
import gi
import logging
gi.require_version('Gtk', '3.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Pango, GLib, Gdk
import repo_manager

# Constants
TITLE = "Software Properties Station"
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 400
CONFIG_FILE = '/etc/pkg/GhostBSD.conf'
LOG_FILE = os.path.expanduser('~/software-properties-station.log')

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class RepoSelector(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title=TITLE)
        self.set_border_width(10)
        self.set_default_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Main layout
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(main_vbox)

        # Toolbar
        toolbar = self.create_toolbar()
        main_vbox.pack_start(toolbar, False, False, 0)

        # Notebook for tabs
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.TOP)
        
        # Repository Selection Tab
        repo_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.create_repo_tab(repo_vbox)
        notebook.append_page(repo_vbox, Gtk.Label(label="Repositories"))

        # Status Tab
        status_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.create_status_tab(status_vbox)
        notebook.append_page(status_vbox, Gtk.Label(label="Status"))

        main_vbox.pack_start(notebook, True, True, 0)

        # Quit button
        quit_button = Gtk.Button(label="Quit")
        quit_button.connect("clicked", self.on_quit)
        
        # Create a box to hold the quit button
        button_box = Gtk.Box(spacing=6)
        button_box.set_halign(Gtk.Align.END)  # Align to the right
        button_box.pack_start(quit_button, False, False, 0)
        
        main_vbox.pack_end(button_box, False, False, 0)

        self.show_all()

    def create_toolbar(self):
        toolbar = Gtk.Toolbar()
#        refresh_button = Gtk.ToolButton(icon_name="view-refresh-symbolic")
#        refresh_button.set_tooltip_text("Refresh Repository List")
#        refresh_button.connect("clicked", self.refresh_repos)
#        toolbar.insert(refresh_button, -1)
        return toolbar

    def create_repo_tab(self, vbox):
        instruction_label = Gtk.Label(label="Select a package repository")
        instruction_label.set_alignment(0.0, 0.5)
        instruction_label.set_hexpand(True)
        instruction_label.set_vexpand(False)
        vbox.pack_start(instruction_label, False, False, 0)

        repo_combo = Gtk.ComboBoxText()
        repo_combo.set_hexpand(True)
        
        for name in repo_manager.REPOS.keys():
            repo_combo.append_text(name)
        
        repo_combo.connect("changed", self.on_repo_selected)
        vbox.pack_start(repo_combo, False, False, 0)

    def create_status_tab(self, vbox):
        self.status_label = Gtk.Label("Status messages will appear here.")
        self.status_label.set_line_wrap(True)
        self.status_label.set_hexpand(True)
        vbox.pack_start(self.status_label, True, True, 0)

    def on_repo_selected(self, combo):
        repo_name = combo.get_active_text()
        if repo_name:
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text="Confirm Repository Change",
            )
            dialog.format_secondary_text(f"Do you want to change the repository to {repo_name}?")
            response = dialog.run()
            dialog.destroy()

            if response == Gtk.ResponseType.YES:
                self.show_message("Updating repository configuration...", Gtk.MessageType.INFO)
                success, message = repo_manager.select_repo(repo_name)
                self.show_message(message, Gtk.MessageType.INFO if success else Gtk.MessageType.ERROR)

    def show_message(self, message, message_type):
        self.status_label.set_text(message)
        color = Gdk.RGBA(1, 0, 0, 1) if message_type == Gtk.MessageType.ERROR else None
        self.status_label.override_color(Gtk.StateFlags.NORMAL, color)

    def refresh_repos(self, widget):
        self.show_message("Repository list refreshed.", Gtk.MessageType.INFO)

    def on_quit(self, widget):
        Gtk.main_quit()

def start_gui():
    win = RepoSelector()
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    repo_manager.main()
