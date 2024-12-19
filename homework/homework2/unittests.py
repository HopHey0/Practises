import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import yaml
import sys

from hw2 import parse_config, parse_dependencies, generate_plantuml

class TestDependencyParser(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='{"package_name": "test-package", "output_file": "output.puml", "max_depth": 2}')
    def test_parse_config(self, mock_file):
        config = parse_config("dummy_path")
        self.assertEqual(config["package_name"], "test-package")
        self.assertEqual(config["output_file"], "output.puml")
        self.assertEqual(config["max_depth"], 2)

    @patch("builtins.open", new_callable=mock_open, read_data='{"dependencies": {"dep1": "^1.0.0", "dep2": "^2.0.0"}}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_parse_dependencies(self, mock_exists, mock_file):
        dependencies = parse_dependencies("test-package", "./node_modules", max_depth=2)
        expected_dependencies = {'test-package': {'dep1', 'dep2'}, 'dep1': {'dep1', 'dep2'}, 'dep2': {'dep1', 'dep2'}}
        self.assertEqual(dependencies, expected_dependencies)

    @patch("builtins.open", new_callable=mock_open, read_data='{"dependencies": {"dep1": "^1.0.0"}}')
    @patch("pathlib.Path.exists", side_effect=lambda: True) 
    def test_parse_dependencies_recursive(self, mock_exists, mock_file):
        with patch("builtins.open", new_callable=mock_open, read_data='{"dependencies": {"dep2": "^1.0.0"}}'):
            dependencies = parse_dependencies("test-package", "./node_modules", max_depth=2)
            expected_dependencies = {
                'test-package': {'dep2'}, 'dep2': {'dep2'}
            }
            self.assertEqual(dependencies, expected_dependencies)

    def test_generate_plantuml(self):
        dependencies = {
            "packageA": {"packageB", "packageC"},
            "packageB": {"packageD"},
            "packageC": {}
        }
        plantuml_code = generate_plantuml(dependencies)

        expected_output = ("""
"packageA" --> "packageB"
""")
        
        for line in expected_output.splitlines():
            self.assertIn(line.strip(), plantuml_code.strip())


if __name__ == "__main__":
    unittest.main()
