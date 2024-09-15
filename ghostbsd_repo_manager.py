import os

# Assuming this is the path to GhostBSD.conf
CONFIG_FILE = '/etc/pkg/GhostBSD.conf'

# Example repositories and their associated content
REPOS = {
    "GhostBSD": {
        "url_latest": "https://pkg.ghostbsd.org/unstable/${ABI}/latest",
        "url_base": "https://pkg.ghostbsd.org/unstable/${ABI}/base"
    },
    "GhostBSD_Canada": {
        "url_latest": "https://pkg.ca.ghostbsd.org/unstable/${ABI}/latest",
        "url_base": "https://pkg.ca.ghostbsd.org/unstable/${ABI}/base"
    },
    "GhostBSD_France": {
        "url_latest": "https://pkg.fr.ghostbsd.org/unstable/${ABI}/latest",
        "url_base": "https://pkg.fr.ghostbsd.org/unstable/${ABI}/base"
    }
}

def select_repo(repo_name):
    """
    Updates the content of the GhostBSD.conf file based on the selected repository.
    """
    if repo_name not in REPOS:
        return False, f"Repository '{repo_name}' not found."

    try:
        # Fetch repository configuration
        repo_config = REPOS[repo_name]

        # Prepare the content for GhostBSD.conf in the desired format
        content = f"""
GhostBSD: {{
  url: "{repo_config['url_latest']}",
  signature_type: "pubkey",
  pubkey: "/usr/share/keys/ssl/certs/ghostbsd.cert",
  enabled: yes
}}
GhostBSD-base: {{
  url: "{repo_config['url_base']}",
  signature_type: "pubkey",
  pubkey: "/usr/share/keys/ssl/certs/ghostbsd.cert",
  enabled: yes
}}
        """

        # Write the new configuration to GhostBSD.conf (do not change the file name)
        with open(CONFIG_FILE, 'w') as config_file:
            config_file.write(content.strip())

        return True, f"Repository '{repo_name}' successfully selected."
    except Exception as e:
        return False, str(e)

def update_config(repo_name):
    """
    Updates the GhostBSD.conf file with new repository settings.
    """
    success, message = select_repo(repo_name)
    return success, message

def validate_config():
    """
    Validates the current GhostBSD.conf file to ensure it's correctly formatted.
    """
    if not os.path.exists(CONFIG_FILE):
        return False, "Configuration file does not exist."
    
    # Example check: Ensuring the file contains the expected blocks
    with open(CONFIG_FILE, 'r') as config_file:
        content = config_file.read()
        if "GhostBSD:" in content and "GhostBSD-base:" in content:
            return True, "Configuration is valid."
        else:
            return False, "Configuration is invalid."

def list_repos():
    """
    Returns a list of available repositories.
    """
    return list(REPOS.keys())

def show_current_repo():
    """
    Shows the current repository configuration.
    """
    if not os.path.exists(CONFIG_FILE):
        return "No configuration file found."

    with open(CONFIG_FILE, 'r') as config_file:
        content = config_file.read()
        return content

# Command-line interaction if this script is directly run
if __name__ == "__main__":
    repos = list_repos()
    print("Available repositories:")
    for repo in repos:
        print(f"- {repo}")

    selected_repo = input("Select a repository: ")
    success, message = update_config(selected_repo)
    if success:
        print(f"Repository '{selected_repo}' selected successfully.")
    else:
        print(f"Error: {message}")

