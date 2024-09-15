#!/usr/bin/env python3.11

def load_repos():
    repos = {
        "GhostBSD": ("https://pkg.ghostbsd.org/unstable/${ABI}/latest", "https://pkg.ghostbsd.org/unstable/${ABI}/base"),
        "GhostBSD_Canada": ("https://pkg.ca.ghostbsd.org/unstable/${ABI}/latest", "https://pkg.ca.ghostbsd.org/unstable/${ABI}/base"),
        "GhostBSD_France": ("https://pkg.fr.ghostbsd.org/unstable/${ABI}/latest", "https://pkg.fr.ghostbsd.org/unstable/${ABI}/base"),
    }
    return repos
