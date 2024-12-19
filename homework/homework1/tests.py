import unittest
import time
import tempfile
import zipfile
from io import StringIO
from unittest.mock import patch
from datetime import datetime

def create_vfs_zip():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip:
        with zipfile.ZipFile(temp_zip, 'w') as zipf:
            # Структура директорй
            zipf.writestr('dir1/file1.txt', 'content1')
            zipf.writestr('dir1/file2.txt', 'content2')
            zipf.writestr('dir2/file3.txt', 'content3')
            zipf.writestr('dir2/file4.txt', 'content4')
            zipf.writestr('dir3/file5.txt', 'content5')
            zipf.writestr('dir3/file6.txt', 'content6')
        return temp_zip.name

class TestemulatorCommands(unittest.TestCase):
    
    # Фикстура для вфс
    @classmethod
    def setUpClass(cls):
        cls.vfs_path = create_vfs_zip()
        cls.log_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        cls.log_file.close()

    # Фикстура для очистки временных файлов
    @classmethod
    def tearDownClass(cls):
        import os
        os.remove(cls.vfs_path)
        os.remove(cls.log_file.name)
    
    def setUp(self):
        from emulator import load_vfs, handle_ls, handle_cd, handle_echo, handle_tree, handle_uptime
        self.vfs_data = load_vfs(self.vfs_path)
        self.handle_ls = handle_ls
        self.handle_cd = handle_cd
        self.handle_echo = handle_echo
        self.handle_tree = handle_tree
        self.handle_uptime = handle_uptime
    
    def test_ls(self):
        # Корневой путь
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.handle_ls(".", self.vfs_data, self.vfs_data)
            output = mock_stdout.getvalue().strip().split("\n")
            output = " ".join(output).split()
            self.assertIn("dir1", output)
            self.assertIn("dir2", output)
            self.assertIn("dir3", output)

        # dir1
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.handle_ls("dir1", self.vfs_data, self.vfs_data)
            output = mock_stdout.getvalue().strip().split("\n")
            output = " ".join(output).split()
            self.assertIn("file1.txt", output)
            self.assertIn("file2.txt", output)

        # nonexistent
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.handle_ls("nonexistent", self.vfs_data, self.vfs_data)
            output = mock_stdout.getvalue().strip()
            self.assertIn("Ошибка: Директория 'nonexistent' не найдена.", output)

    def test_cd(self):
        # dir1
        current_dir = self.vfs_data
        current_path = []
        new_current_dir, new_current_path = self.handle_cd("dir1", current_dir, self.vfs_data, current_path)
        self.assertEqual(new_current_dir, self.vfs_data["dir1"])
        self.assertEqual(new_current_path, ["dir1"])

        # ".."
        new_current_dir, new_current_path = self.handle_cd("..", new_current_dir, self.vfs_data, new_current_path)
        self.assertEqual(new_current_dir, self.vfs_data)
        self.assertEqual(new_current_path, [])

        # nonexistent
        new_current_dir, new_current_path = self.handle_cd("nonexistent", current_dir, self.vfs_data, current_path)
        self.assertEqual(new_current_dir, current_dir)  # Директория не должна измениться
        self.assertEqual(new_current_path, current_path)

    def test_echo(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.handle_echo("Hello, World!")
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "Hello, World!")

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.handle_echo("")
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "")

    def test_tree(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.handle_tree(self.vfs_data)
            output = mock_stdout.getvalue().strip().split("\n")
            
            self.assertIn("├── dir1", output)
            self.assertIn("├── dir2", output)
            self.assertIn("└── dir3", output)
            
            self.assertIn("│   ├── file1.txt", output)
            self.assertIn("│   └── file2.txt", output)
            self.assertIn("│   ├── file3.txt", output)
            self.assertIn("│   └── file4.txt", output)
            self.assertIn("    ├── file5.txt", output)
            self.assertIn("    └── file6.txt", output)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.handle_tree(self.vfs_data["dir1"])
            output = mock_stdout.getvalue().strip().split("\n")
            self.assertIn("├── file1.txt", output)
            self.assertIn("└── file2.txt", output)

    def test_uptime(self):
        start_time = time.time()

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.handle_uptime(start_time)
            output = mock_stdout.getvalue().strip()
            self.assertIn("Текущее системное время:", output)
            self.assertIn("Время работы эмулятора:", output)
            self.assertIn("секунд", output)

if __name__ == '__main__':
    unittest.main()
