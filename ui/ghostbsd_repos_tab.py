from gi.repository import Gtk
import repo.ghostbsd_repo_manager as ghostbsd_repo_manager
import os

class GhostBSDReposTab(Gtk.Box):
    CONFIG_FILE = "/usr/local/etc/pkg/repos/GhostBSD.conf"

    def __init__(self, privilege_level):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.is_read_only = (privilege_level == "read-only")
        self.checkboxes = {}  # Dictionary to track checkboxes by repository name
        self.selected_repo = None  # Track the currently selected repository
        self.create_ghostbsd_repo_ui()

    def create_ghostbsd_repo_ui(self):
        # Header
        header_label = Gtk.Label(label="Manage Repositories")
        header_label.set_halign(Gtk.Align.CENTER)
        header_label.get_style_context().add_class("title-1")  # Add custom GTK CSS class if needed
        self.append(header_label)

        description_label = Gtk.Label(label="Enable one repository at a time for your system.")
        description_label.set_halign(Gtk.Align.CENTER)
        description_label.set_margin_bottom(10)
        self.append(description_label)

        # Repository List (using Gtk.ListBox)
        self.repo_listbox = Gtk.ListBox()
        self.update_repo_list()
        self.append(self.repo_listbox)

    def update_repo_list(self):
        # Clear existing rows
        row = self.repo_listbox.get_first_child()
        while row:
            next_row = row.get_next_sibling()
            self.repo_listbox.remove(row)
            row = next_row

        # Clear existing checkboxes
        self.checkboxes.clear()

        # Populate repository rows with checkboxes
        for repo_name, repo_url in ghostbsd_repo_manager.ghostbsd_repos.items():
            row = Gtk.ListBoxRow()

            # Create a horizontal box for each row
            row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

            # Add checkbox
            checkbox = Gtk.CheckButton()
            checkbox.set_active(False)  # Start with all checkboxes unchecked
            checkbox.set_sensitive(not self.is_read_only)  # Disable in read-only mode
            checkbox.connect("toggled", self.on_checkbox_toggled, repo_name)
            self.checkboxes[repo_name] = checkbox  # Track the checkbox by repo name
            row_box.append(checkbox)

            # Add repository name
            name_label = Gtk.Label(label=repo_name)
            name_label.set_halign(Gtk.Align.START)
            name_label.set_margin_end(10)
            row_box.append(name_label)

            # Add repository URL
            url_label = Gtk.Label(label=repo_url)
            url_label.set_halign(Gtk.Align.START)
            row_box.append(url_label)

            row.set_child(row_box)
            self.repo_listbox.append(row)

    def on_checkbox_toggled(self, checkbox, repo_name):
        """
        Callback for the checkbox to enable one repository and disable others.
        """
        if checkbox.get_active():
            print(f"Enabling repository: {repo_name}")
            self.selected_repo = repo_name  # Update the currently selected repository

            # Uncheck all other checkboxes
            for name, other_checkbox in self.checkboxes.items():
                if name != repo_name:
                    other_checkbox.handler_block_by_func(self.on_checkbox_toggled)  # Temporarily block signal
                    other_checkbox.set_active(False)
                    other_checkbox.handler_unblock_by_func(self.on_checkbox_toggled)  # Unblock signal

            # Update the configuration file
            self.update_config_file(repo_name)
        else:
            print(f"Disabling repository: {repo_name}")
            if self.selected_repo == repo_name:
                self.selected_repo = None  # Clear the selected repository

    def update_config_file(self, repo_name):
        """
        Write the selected repository configuration to the GhostBSD.conf file.
        """
        repo_url = ghostbsd_repo_manager.ghostbsd_repos.get(repo_name)
        if not repo_url:
            print(f"Error: Repository URL for {repo_name} not found.")
            return

        base_url = repo_url.replace("latest", "base")

        config_content = f"""
GhostBSD: {{
  url: "{repo_url}",
  signature_type: "pubkey",
  pubkey: "/usr/share/keys/ssl/certs/ghostbsd.cert",
  enabled: yes
}}
GhostBSD-base: {{
  url: "{base_url}",
  signature_type: "pubkey",
  pubkey: "/usr/share/keys/ssl/certs/ghostbsd.cert",
  enabled: yes
}}
"""

        try:
            with open(self.CONFIG_FILE, "w") as config_file:
                config_file.write(config_content)
            print(f"Configuration updated for {repo_name} in {self.CONFIG_FILE}.")
        except PermissionError:
            print(f"Error: Insufficient permissions to write to {self.CONFIG_FILE}.")
        except Exception as e:
            print(f"Error: Unable to update configuration file: {e}")

