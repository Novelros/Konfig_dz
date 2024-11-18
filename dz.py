import argparse
from tar1 import VirtualFileSystem
from gui import run_gui

def parse_args():
    parser = argparse.ArgumentParser(description="Shell emulator")
    parser.add_argument("username", help="Имя пользователя для приглашения")
    parser.add_argument("fs_archive", help="Путь к tar архиву виртуальной файловой системы")
    parser.add_argument("start_script", help="Путь к txt первые команды")

    return parser.parse_args()

def main():
    args = parse_args()
    # Создаем объект виртуальной файловой системы
    fs = VirtualFileSystem(args.fs_archive)

    # Запускаем GUI с эмулятором оболочки
    run_gui(args.username, fs, args.fs_archive,args.start_script)

if __name__ == "__main__":
    main()



# Для запуска эмулятора из командной строки:
# python dz.py users virtual_fs_archive.tar start_script.txt
# Для запуска с графическим интерфейсом:
# python dz.py --gui username virtual_fs_archive.tar init_script.sh
# python dz.py <username> <fs_archive> <init_script>
# python dz.py user1 virtual_fs_archive.tar init_script.sh
# python dz.py <username> <path_to_fs.tar>
# python dz.py user virtual_fs_archive.tar
