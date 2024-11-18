import argparse
from tar1 import VirtualFileSystem
from gui import run_gui

def parse_args():
    parser = argparse.ArgumentParser(description="Shell emulator")
    parser.add_argument("log", help="Лог-файл содержит все действия во время последнего сеанса работы с эмулятором.")
    parser.add_argument("fs_archive", help="Путь к tar архиву виртуальной файловой системы")
    parser.add_argument("start_script", help="Путь к txt первые команды")

    return parser.parse_args()

def main():
    args = parse_args()
    # Создаем объект виртуальной файловой системы
    fs = VirtualFileSystem(args.fs_archive)

    # Запускаем GUI с эмулятором оболочки
    run_gui(args.log, fs, args.fs_archive,args.start_script)

if __name__ == "__main__":
    main()



# Для запуска эмулятора из командной строки:
# python dz.py log.file.xml virtual_fs_archive.tar start_script.txt
# Для запуска с графическим интерфейсом:
# python dz.py --gui log.file.xml virtual_fs_archive.tar init_script.sh
# python dz.py <log.file.xml> <fs_archive> <init_script>
# python dz.py log.file.xml virtual_fs_archive.tar init_script.sh
# python dz.py <log.file.xml> <path_to_fs.tar>
# python dz.py log.file.xml virtual_fs_archive.tar
