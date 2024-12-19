import argparse
import csv
import sys
import time
import zipfile
from datetime import datetime

# Парсинг аргументов командной строки
def parse_args():
    parser = argparse.ArgumentParser(description="Эмулятор shell для UNIX-подобной ОС.")
    parser.add_argument("user", help="Имя пользователя для приглашения.")
    parser.add_argument("vfs", help="Путь к zip-архиву виртуальной файловой системы.")
    parser.add_argument("log", help="Путь к лог-файлу (CSV).")
    return parser.parse_args()

# Инициализация вфс
def load_vfs(zip_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            vfs = {}
            for file in zf.namelist():
                parts = file.strip('/').split('/')
                current = vfs
                for part in parts[:-1]:
                    if part not in current or not isinstance(current[part], dict):
                        current[part] = {}
                    current = current[part]
                # Определяем, файл это или папка
                if file.endswith('/'):
                    current[parts[-1]] = {}  # Папка
                else:
                    current[parts[-1]] = zf.read(file)  # Файл
        return vfs
    except FileNotFoundError:
        print("Ошибка: указанный архив не найден.")
        sys.exit(1)

def log_action(log_path, user, command, mode='a'):
    with open(log_path, mode=mode, newline='', encoding='utf-8') as log_file:
        writer = csv.writer(log_file)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), user, command])

def handle_ls(path, current_dir, root_dir):
    target_dir = navigate_to_path(path, current_dir, root_dir)
    if target_dir is None:
        print(f"Ошибка: Директория '{path}' не найдена.")
    elif isinstance(target_dir, dict):
        items = [item for item in target_dir if item != ".."]
        if items:
            max_len = max(len(item) for item in items) + 2
            cols = 80 // max_len
            for i, item in enumerate(items):
                print(item.ljust(max_len), end="")
                if (i + 1) % cols == 0:
                    print()
            if len(items) % cols != 0:
                print()
        else:
            print("Пустая директория.")
    else:
        print(f"Ошибка: '{path}' не является директорией.")

def handle_cd(path, current_dir, root_dir, current_path):
    flag = False
    if "//" in path:
        print(f"Ошибка: неверный путь '{path}'.")
        return current_dir, current_path
    if "../" in path:
        flag = True
    path = path.strip('/')
    parts = path.split('/')

    for part in parts:
        if part == "..":
            if current_path:
                current_path.pop()
                current_dir = navigate_to_path('/'.join(current_path), root_dir, root_dir)
            elif flag != True:
                print("Ошибка: уже находитесь в корневой директории.")
        elif part and part in current_dir and isinstance(current_dir[part], dict):
            current_path.append(part)
            current_dir = current_dir[part]
        else:
            print(f"Ошибка: Директория '{part}' не найдена.")
            return current_dir, current_path
    return current_dir, current_path

def navigate_to_path(path, current_dir, root_dir):
    if path in {".", ""}:
        return current_dir
    parts = path.split('/')
    target_dir = current_dir if not path.startswith("/") else root_dir
    for part in parts:
        if part == "..":
            target_dir = root_dir if target_dir == root_dir else target_dir.get("..", root_dir)
        elif part and part in target_dir:
            target_dir = target_dir[part]
        else:
            return None
    return target_dir

def handle_tree(directory, prefix=""):
    contents = [item for item in directory.keys() if item != ".."]
    for index, item in enumerate(contents):
        connector = "└── " if index == len(contents) - 1 else "├── "
        print(f"{prefix}{connector}{item}")
        if isinstance(directory[item], dict):
            child_prefix = prefix + ("    " if index == len(contents) - 1 else "│   ")
            handle_tree(directory[item], child_prefix)

def handle_uptime(start_time):
    elapsed = time.time() - start_time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Текущее системное время: {current_time}")
    print(f"Время работы эмулятора: {elapsed:.2f} секунд.")

def handle_echo(command):
    print(command)

def shell(user, vfs, log_path):
    current_dir = vfs
    root_dir = vfs
    current_path = []
    start_time = time.time()
    log_action(log_path, user, "Session started", mode='w')

    while True:
        try:
            prompt = f"{user}@shell:{'/'.join(current_path) or '/'}> "
            command = input(prompt).strip()
            log_action(log_path, user, command)
            if command == "exit":
                print("Завершение работы.")
                break
            elif command.startswith("ls"):
                path = command[3:].strip() or "."
                handle_ls(path, current_dir, root_dir)
            elif command.startswith("cd "):
                _, path = command.split(maxsplit=1)
                current_dir, current_path = handle_cd(path, current_dir, root_dir, current_path)
            elif command == "tree":
                handle_tree(root_dir)
            elif command == "uptime":
                handle_uptime(start_time)
            elif command.startswith("echo "):
                handle_echo(command[5:].strip())
            else:
                print("Неизвестная команда.")
        except KeyboardInterrupt:
            print("\nЗавершение работы.")
            break

# Запуск программы
if __name__ == "__main__":
    args = parse_args()
    vfs = load_vfs(args.vfs)
    shell(args.user, vfs, args.log)
    log_action(args.log, args.user, "Session ended")
