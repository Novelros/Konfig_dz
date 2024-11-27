import os
import sys
import platform
import time
import xml.etree.ElementTree as ET
import tarfile





class ShellEmulator:
    def __init__(self, log, fs, fs_arch):
        self.fs_path = fs_arch
        self.log = log
        self.fs = fs
        self.current_dir = '/'  # Начальная директория в виртуальной файловой системе
        self.virtual_files = {}  # Словарь для хранения "виртуальных" файлов и их содержимого
        self.file_timestamps = {}  # Словарь для хранения "временных меток" виртуальных файлов
        self.log_file = log  # Изменено имя файла на log.file.xml
        self.init_log()

    def init_log(self):
        """Инициализация XML лог-файла."""
        root = ET.Element("log_file")
        tree = ET.ElementTree(root)
        tree.write(self.log_file)

    def prompt(self):
        return f"{self.log}@emulator:{self.current_dir}$ "

    def log_command(self, command, status):
        """Логирование команды в XML файл."""
        tree = ET.parse(self.log_file)
        root = tree.getroot()

        command_entry = ET.SubElement(root, "command")
        command_entry.set("name", command)
        command_entry.set("status", status)

        tree.write(self.log_file)


    def execute_command(self, command):
        response = ""
        if command == "ls":
            response = self.ls()
            status = "Успешно" if response else "Неуспешно"
        elif command.startswith("cd "):
            directory = command.split(" ")[1]
            response = self.cd(directory)
            status = "Успешно" if not response else "Неуспешно"
        elif command.startswith("touch "):
            filename = command.split(" ")[1]
            response = self.touch(filename)
            status = "Успешно" if "создан." in response or "обновлена." in response else "Неуспешно"
        elif command.startswith("cat "):
            filename = command.split(" ")[1]
            response = self.cat(filename)
            status = "Успешно" if response else "Неуспешно"
        elif command.startswith("uname"):
            response = self.uname()
            status = "Успешно" if response else "Неуспешно"
        elif command == "exit":
            self.exit()
            return  # После выхода из программы можно не продолжать выполнение.
        else:
            response = f"Unknown command: {command}"
            status = "Неуспешно"

        self.log_command(command, status)  # Логируем команду вне зависимости от ее результата.
        return response

    def ls(self):
        """Список файлов в текущей директории виртуальной файловой системы, включая виртуальные файлы."""
        files = self.fs.list_files()
        current_path = self.current_dir.lstrip('/') + '/' if self.current_dir != '/' else ''
        filtered_files = [f[len(current_path):] for f in files if f.startswith(current_path)]

        # Добавляем виртуальные файлы, созданные командой touch
        virtual_files_in_dir = [
            f[len(current_path):] for f in self.virtual_files.keys() if f.startswith(current_path)
        ]

        list_ls_current = set()  # Используем множество для автоматического фильтрации дубликатов

        # Объединяем отфильтрованные файлы и виртуальные файлы в одном цикле
        for file in filtered_files + virtual_files_in_dir:
            # Проверяем наличие символа '/'
            if '/' in file:
                prefix = file.split('/')[0]  # Получаем префикс до первого '/'
                list_ls_current.add(prefix)  # Добавляем префикс
            else:
                list_ls_current.add(file)  # Добавляем сам файл, если '/' нет

        # Преобразуем обратно в список, если необходимо
        list_ls_current = list(list_ls_current)


        return '\n'.join(list_ls_current)

    def cd(self, directory):
        """Переход в другую директорию (эмуляция)."""
        if directory == '/':
            self.current_dir = '/'
        elif directory == '..':
            # Переход в родительскую директорию
            if self.current_dir != '/':
                self.current_dir = '/'.join(self.current_dir.rstrip('/').split('/')[:-1]) or '/'
        else:
            # Обработка полного пути
            if directory.startswith('/'):
                possible_path = directory
            else:
                if self.current_dir.endswith('/'):
                    possible_path = self.current_dir + directory
                else:
                    possible_path = self.current_dir + '/' + directory

            # Убираем лишние слеши
            possible_path = '/'.join(filter(None, possible_path.split('/')))

            # Проверка, существует ли директория
            if any(f.startswith(possible_path + '/') or f == possible_path for f in self.fs.list_files()):
                self.current_dir = possible_path
            else:
                return f"Directory not found: {directory}, path - {possible_path}"

        return ""

    def touch(self, filename):
        # Создание пустого файла или обновление времени для существующего.
        current_path = self.current_dir.rstrip('/') + '/' if self.current_dir != '/' else '/'
        file_path = current_path + filename

        # Если файл уже существует в архиве
        if file_path in self.fs.list_files():
            # Извлекаем содержимое архива
            extract_path = "./temp_fs"
            with tarfile.open(self.fs_path, "r") as tar:
                tar.extractall(path=extract_path)

            # Путь к извлеченному файлу
            extracted_file_path = os.path.join(extract_path, file_path.lstrip('/'))
            if os.path.exists(extracted_file_path):
                # Обновляем временную метку
                os.utime(extracted_file_path, None)
                message = f"Метка времени для '{filename}' обновлена."
            else:
                message = f"Ошибка: файл '{filename}' не найден в архиве."

            # Пересоздаем архив с обновленными файлами
            with tarfile.open(self.fs_path, "w") as tar:
                for root, dirs, files in os.walk(extract_path):
                    for file in files:
                        file_full_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_full_path,extract_path)  # Относительный путь для правильной структуры
                        tar.add(file_full_path, arcname=arcname)

            # Удаляем временные извлеченные файлы
            for root, dirs, files in os.walk(extract_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))


            return message
        # Если файл не существует, создаем пустой файл и устанавливаем начальную метку времени
        self.virtual_files[file_path] = ""  # Пустое содержимое файла
        self.file_timestamps[file_path] = time.ctime()  # Устанавливаем текущее время как метку времени
        return f"Файл '{filename}' создан"


    def cat(self, filename):
        """Вывод содержимого файла."""
        current_path = self.current_dir.lstrip('/') + '/' if self.current_dir != '/' else ''
        full_filename = current_path + filename

        # Проверка на виртуальные файлы
        if full_filename in self.virtual_files:
            content = self.virtual_files[full_filename]
            if not content:
                return f"Виртуальный файл '{filename}' пуст."
            return content  # Возвращаем содержимое файла в оригинальном порядке

        # Если файл не виртуальный, пробуем его прочитать из файловой системы
        content = self.fs.open_file(full_filename)
        return content  # Возвращаем содержимое файла в оригинальном порядке

    def uname(self):
        """Выводит информацию о системе."""
        system_info = {
            "system": platform.system(),  # Имя операционной системы
            "node": platform.node(),  # Имя узла
            "release": platform.release(),  # Версия операционной системы
            "version": platform.version(),  # Полная версия ОС
            "machine": platform.machine(),  # Архитектура машинного объекта
            "processor": platform.processor(),  # Имя процессора
        }

        # Форматируем вывод
        info_output = f"Система: {system_info['system']}\n" \
                      f"Имя узла: {system_info['node']}\n" \
                      f"Версия: {system_info['release']}\n" \
                      f"Полная версия: {system_info['version']}\n" \
                      f"Архитектура: {system_info['machine']}\n" \
                      f"Процессор: {system_info['processor']}\n"

        return info_output.strip()  # Удаляем лишние пробелы в конце строки

    def exit(self):
        sys.exit(0)

    # def execute_commands_from_file(self, file_path):
    #     """Читает команды из указанного текстового файла и выполняет их."""
    #     try:
    #         with open(file_path, 'r') as file:
    #             for line in file:
    #                 command = line.strip()
    #                 if command:  # Игнорируем пустые строки
    #                     #print(f"Выполнение команды: {command}")
    #                     self.execute_command(command)
    #                     #print(a)
    #     except FileNotFoundError as e:
    #         print(f"Файл '{file_path}' не найден: {e}")
    #     except Exception as e:
    #         print(f"Произошла ошибка при выполнении команд: {e}")

    def execute_commands_from_file(self, file_path):
        # Выполнение скрипта и сбор вывода
        output = ""
        if file_path:
            try:
                with open(file_path, "r") as script_file:
                    for line in script_file:
                        command = line.strip()
                        if command:  # Пропускаем пустые строки
                            result = self.execute_command(command)
                            output += f"{self.prompt()}{command}\n"
                            if result:
                                output += f"{result}\n"
            except FileNotFoundError:
                output += f"Ошибка: стартовый скрипт '{file_path}' не найден.\n"
        return output







