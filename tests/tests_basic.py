import unittest
import os
import tempfile
from unittest.mock import patch

class TestSoftwarePropertiesStation(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.mock_config_file = os.path.join(self.temp_dir.name, "GhostBSD.conf")

        # Mock the CONFIG_FILE path
        patcher = patch("ui.ghostbsd_repos_tab.GhostBSDReposTab.CONFIG_FILE", self.mock_config_file)
        self.addCleanup(patcher.stop)
        self.mock_config_file_patch = patcher.start()

    def tearDown(self):
        # Cleanup the temporary directory
        self.temp_dir.cleanup()

    def test_config_file_creation(self):
        """Test if the configuration file is created when a repository is selected."""
        from ui.ghostbsd_repos_tab import GhostBSDReposTab

        tab = GhostBSDReposTab(privilege_level="root")
        tab.update_config_file("GhostBSD")

        self.assertTrue(os.path.exists(self.mock_config_file), "Configuration file was not created.")

    def test_config_file_content(self):
        """Test if the configuration file contains valid data."""
        from ui.ghostbsd_repos_tab import GhostBSDReposTab

        tab = GhostBSDReposTab(privilege_level="root")
        tab.update_config_file("GhostBSD")

        with open(self.mock_config_file, "r") as f:
            content = f.read()

        self.assertIn("GhostBSD", content, "Configuration file does not contain repository name.")
        self.assertIn("enabled: yes", content, "Configuration file does not enable the repository.")


if __name__ == "__main__":
    unittest.main()

