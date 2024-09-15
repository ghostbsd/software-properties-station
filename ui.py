#!/usr/bin/env python3.11

import os
import gi

# Set the GTK version before importing Gtk
gi.require_version('Gtk', '4.0')

from gi.repository import Gtk, Pango, GLib, Gdk, Gio
import logging
import repo_manager

# Constants
TITLE = "Software Properties Station"
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 400
CONFIG_FILE = '/etc/pkg/GhostBSD.conf'
LOG_FILE = os.path.expanduser('~/software-properties-station.log')

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class RepoSelector(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title=TITLE)

        # CSS Provider to add margins or padding
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data("""
            window { padding: 10px; }
        """, -1)

        style_context = self.get_style_context()
        style_context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        self.set_default_size(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Header Bar (replaces toolbar)
        header_bar = Gtk.HeaderBar()
        header_bar.set_show_title_buttons(True)

        # Create a label for the title and add it to the HeaderBar
        title_label = Gtk.Label(label=TITLE)
        header_bar.set_title_widget(title_label)

        self.set_titlebar(header_bar)

        # Main layout
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(main_vbox)

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

        main_vbox.append(notebook)

        # Quit button
        quit_button = Gtk.Button(label="Quit")
        quit_button.connect("clicked", self.on_quit)

        # Create a box to hold the quit button
        button_box = Gtk.Box(spacing=6)
        button_box.set_halign(Gtk.Align.END)
        button_box.append(quit_button)

        main_vbox.append(button_box)

    def create_repo_tab(self, vbox):
        instruction_label = Gtk.Label(label="Select a package repository")
        instruction_label.set_halign(Gtk.Align.START)
        instruction_label.set_hexpand(True)
        vbox.append(instruction_label)

        # Create a Gio.ListStore model from the repository names
        liststore = Gio.ListStore.new(Gtk.StringObject)
        for repo in repo_manager.REPOS.keys():
            liststore.append(Gtk.StringObject.new(repo))

        # Create a DropDown using the ListStore
        repo_combo = Gtk.DropDown.new(liststore, None)
        repo_combo.connect("notify::selected", self.on_repo_selected)

        vbox.append(repo_combo)

    def create_status_tab(self, vbox):
        self.status_label = Gtk.Label(label="Status messages will appear here.")
        self.status_label.set_wrap(True)
        self.status_label.set_hexpand(True)
        vbox.append(self.status_label)

    def on_repo_selected(self, combo, *args):
        selected_item = combo.get_selected_item()
        if selected_item:
            repo_name = selected_item.get_string()

            # Create a confirmation dialog using Gtk.MessageDialog
            dialog = Gtk.MessageDialog(
                transient_for=self,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text="Confirm Repository Change"
            )

            # Add secondary text as an extra label inside the content area
            secondary_label = Gtk.Label(label=f"Do you want to change the repository to {repo_name}?")
            dialog.get_content_area().append(secondary_label)

            # Connect the response to a callback function (remove the extra dialog argument)
            dialog.connect("response", self.on_response_dialog, repo_name)

            dialog.show()

    def on_response_dialog(self, dialog, response_id, repo_name):
        if response_id == Gtk.ResponseType.YES:
            dialog.destroy()

            # Attempt to select and apply the repository
            success, message = repo_manager.select_repo(repo_name)

            # Show a message based on whether the operation succeeded or failed
            if success:
                self.show_message(f"Repository '{repo_name}' selected and configuration updated.", Gtk.MessageType.INFO)
            else:
                self.show_message(f"Failed to update repository: {message}", Gtk.MessageType.ERROR)
        else:
            dialog.destroy()

    def show_message(self, message, message_type):
        self.status_label.set_text(message)
        if message_type == Gtk.MessageType.ERROR:
            css_provider = Gtk.CssProvider()
            css_provider.load_from_data("* { color: red; }", -1)
            self.status_label.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def on_quit(self, widget):
        self.close()

class SoftwarePropertiesApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.gtk.example")

    def do_activate(self):
        # Create the main window
        win = RepoSelector(self)
        win.present()

def start_gui():
    app = SoftwarePropertiesApp()
    app.run(None)

if __name__ == "__main__":
    repo_manager.main()

