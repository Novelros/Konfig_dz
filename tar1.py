import tarfile
import os


class VirtualFileSystem:
    def __init__(self, tar_path):
        self.tar_path = tar_path

    def list_files(self):
        """Возвращает список файлов внутри архива tar."""
        with tarfile.open(self.tar_path, 'r') as tar:
            return tar.getnames()

    def open_file(self, filename):
        """Открывает файл из архива tar и возвращает его содержимое."""
        with tarfile.open(self.tar_path, 'r') as tar:
            try:
                file = tar.extractfile(filename)
                return file.read().decode('utf-8')
            except KeyError:
                return f"Файл {filename} не найден в архиве"

    def archive_single_directory(self, directory_path, output_path='virtual_fs_archive.tar'):
        """Создает архив tar из указанной одной директории."""
        if not os.path.isdir(directory_path):
            return f"Путь '{directory_path}' не является директорией."

        with tarfile.open(output_path, 'w') as tar:
            # Добавляем саму директорию в архив
            tar.add(directory_path, arcname=os.path.basename(directory_path))

        return f"Архив '{output_path}' успешно создан из директории '{directory_path}'."

# Пример использования
vfs = VirtualFileSystem('path/to/your/archive.tar')
output_archive = vfs.archive_single_directory(r'virtual_fs_archive', 'virtual_fs_archive.tar')

print(output_archive)