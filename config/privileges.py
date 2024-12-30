import os

def is_root_user():
    """
    Checks if the current user has root privileges.
    """
    return os.geteuid() == 0

def get_privilege_level():
    """
    Returns the privilege level as 'read-only' or 'full'.
    """
    return 'full' if is_root_user() else 'read-only'

