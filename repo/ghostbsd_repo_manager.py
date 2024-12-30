ghostbsd_repos = {
    "GhostBSD": "https://pkg.ghostbsd.org/stable/${ABI}/latest",
    "GhostBSD_Canada": "https://pkg.ca.ghostbsd.org/stable/${ABI}/latest",
    "GhostBSD_France": "https://pkg.fr.ghostbsd.org/stable/${ABI}/latest"
}

def list_repos():
    """
    Returns a list of GhostBSD repositories.
    """
    return list(ghostbsd_repos.keys())

def update_config(repo_name):
    """
    Updates the GhostBSD configuration file with the selected repository.
    """
    if repo_name in ghostbsd_repos:
        config_content = f"""
GhostBSD: {{
  url: "{ghostbsd_repos[repo_name]}",
  signature_type: "pubkey",
  pubkey: "/usr/share/keys/ssl/certs/ghostbsd.cert",
  enabled: yes
}}
GhostBSD-base: {{
  url: "{ghostbsd_repos[repo_name].replace('latest', 'base')}",
  signature_type: "pubkey",
  pubkey: "/usr/share/keys/ssl/certs/ghostbsd.cert",
  enabled: yes
}}
"""
        # Simulating writing to config file (actual path may vary)
        with open('/usr/local/etc/pkg/repos/GhostBSD.conf', 'w') as config_file:
            config_file.write(config_content)

        return True, f"Repository '{repo_name}' updated successfully."
    return False, f"Repository '{repo_name}' not found."

