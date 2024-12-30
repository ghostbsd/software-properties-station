#!/usr/bin/env python
# Filename: config.py

def load_repos():
    repos = {
        "GhostBSD": ("https://pkg.ghostbsd.org/stable/${ABI}/latest", "https://pkg.ghostbsd.org/stable/${ABI}/base"),
        "GhostBSD_Canada": ("https://pkg.ca.ghostbsd.org/stable/${ABI}/latest", "https://pkg.ca.ghostbsd.org/stable/${ABI}/base"),
        "GhostBSD_France": ("https://pkg.fr.ghostbsd.org/stable/${ABI}/latest", "https://pkg.fr.ghostbsd.org/stable/${ABI}/base"),
    }
    return repos
