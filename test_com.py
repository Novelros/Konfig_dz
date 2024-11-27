import unittest
from unittest.mock import patch

from tar1 import VirtualFileSystem
from start import ShellEmulator

class TestShellEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создаем виртуальную файловую систему для тестов
        cls.fs_archive = "virtual_fs_archive.tar"
        cls.log = "log.file.xml"
        cls.start_script = "test_script.txt"

        # Создаем виртуальный файловый архив для тестов
        cls.fs = VirtualFileSystem(cls.fs_archive)

    def setUp(self):
        # Инициализируем эмулятор для каждого теста
        self.shell = ShellEmulator(self.log, self.fs, self.fs_archive)

    # Тесты для команды ls
    def test_ls_root(self):
        result = self.shell.ls()
        self.assertIn("virtual_fs_archive", result)

    def test_ls_testing(self):
        self.shell.cd("virtual_fs_archive")
        result = self.shell.ls()
        self.assertIn("ne_tochka", result)

    def test_ls_testdir(self):
        self.shell.cd("virtual_fs_archive/ne_tochka/konfig_dz")
        result = self.shell.ls()
        self.assertIn("start.py", result)
        self.assertIn("tar1.py", result)
        self.assertIn("commands.txt", result)

    # Тесты для команды cd
    def test_cd_to_existing_dir(self):
        result = self.shell.cd("virtual_fs_archive/ne_tochka/konfig_dz")
        self.assertEqual(self.shell.current_dir, "virtual_fs_archive/ne_tochka/konfig_dz")
        self.assertEqual(result, "")

    def test_cd_invalid_dir(self):
        result = self.shell.cd("ne_tochka/vevn")
        self.assertIn("Directory not found", result)

    def test_cd_back_to_parent(self):
        self.shell.cd("virtual_fs_archive/ne_tochka/konfig_dz")
        self.shell.cd("..")
        self.assertEqual(self.shell.current_dir, "virtual_fs_archive/ne_tochka")

    # Тесты для команды touch
    def test_touch_create_new_file(self):
        self.shell.cd("virtual_fs_archive/ne_tochka/konfig_dz")
        result = self.shell.touch("newfile.txt")
        self.assertEqual("Файл 'newfile.txt' создан", result)
        index = str(self.shell.virtual_files).find(":")
        self.assertEqual("virtual_fs_archive/ne_tochka/konfig_dz/newfile.txt", str(self.shell.virtual_files)[2:index-1])

    def test_touch_update_existing_file(self):
        self.shell.cd("virtual_fs_archive/ne_tochka/konfig_dz")
        result = self.shell.touch("commands.txt")
        self.assertIn("Метка времени для 'commands.txt' обновлена.", result)

    def test_touch_nonexistent_path(self):
        self.shell.cd("ne_tochka/vevn")
        result = self.shell.touch("newfile.txt")
        self.assertIn("Файл 'newfile.txt' создан", result)

    # Тесты для команды tac
    def test_cat_existing_file(self):
        self.shell.cd("virtual_fs_archive/ne_tochka/konfig_dz")
        result = self.shell.cat("commands.txt")
        self.assertEqual(result, "")

    def test_cat_empty_file(self):
        self.shell.cd("virtual_fs_archive/ne_tochka/konfig_dz")
        result = self.shell.cat("session_log.xml")
        self.assertEqual(result, "<session_log><action>ls</action><result>file1 file2 file3</result></session_log>")

    def test_cat_nonexistent_file(self):
        self.shell.cd("virtual_fs_archive/ne_tochka/konfig_dz")
        result = self.shell.cat("nonexistent.txt")
        self.assertEqual("Файл virtual_fs_archive/ne_tochka/konfig_dz/nonexistent.txt не найден в архиве", result)

    # Тесты для команды exit
    def test_exit(self):
        with self.assertRaises(SystemExit):
            self.shell.exit()

        # Тесты для команды uname

    @patch('platform.system', return_value='Windows')
    @patch('platform.node', return_value='DESKTOP-0DPJS96')
    @patch('platform.release', return_value='11')
    @patch('platform.version', return_value='10.0.22631')
    @patch('platform.machine', return_value='AMD64')
    @patch('platform.processor', return_value='Intel64 Family 6 Model 154 Stepping 3, GenuineIntel')
    def test_uname(self, mock_processor, mock_machine, mock_version, mock_release, mock_node, mock_system):
        result = self.shell.uname()

        # Ожидаемый вывод
        expected_output = (
            "Система: Windows\n"
            "Имя узла: DESKTOP-0DPJS96\n"
            "Версия: 11\n"
            "Полная версия: 10.0.22631\n"
            "Архитектура: AMD64\n"
            "Процессор: Intel64 Family 6 Model 154 Stepping 3, GenuineIntel"
        )

        # Сравнение результата с ожидаемым выводом
        self.assertEqual(result, expected_output)

if __name__ == "__main__":
    unittest.main()

