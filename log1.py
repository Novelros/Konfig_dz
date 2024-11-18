import xml.etree.ElementTree as ET

def create_log(log_file_path):
    log_root = ET.Element("log_file")
    ET.ElementTree(log_root).write(log_file_path)
    print(f"Лог-файл {log_file_path} успешно создан.")

if __name__ == "__main__":
    log_file_path = input("Введите путь к файлу журнала (например, log.xml): ")
    create_log(log_file_path)