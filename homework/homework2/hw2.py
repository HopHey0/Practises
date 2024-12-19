import yaml
import json
import os
import sys
from pathlib import Path
from typing import Dict, Set


def parse_config(file_path: str) -> Dict[str, str]:
    with open(file_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def parse_dependencies(package_name: str, base_path: str, max_depth: int, current_depth: int = 0) -> Dict[str, Set[str]]:
    if current_depth >= max_depth:
        return {}

    dependencies = {}

    def collect_dependencies(package: str, path: str):
        package_json_path = Path(path) / package / "package.json"
        if not package_json_path.exists():
            print(f"Файл {package_json_path} не найден. Пропускаю {package}.", file=sys.stderr)
            return

        with open(package_json_path, 'r', encoding='utf-8') as f:
            try:
                package_data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Ошибка чтения {package_json_path}: {e}", file=sys.stderr)
                return

        if "dependencies" in package_data:
            deps = set(package_data["dependencies"].keys())
            dependencies[package] = deps
            for dep in deps:
                if dep not in dependencies:
                    collect_dependencies(dep, path)

    collect_dependencies(package_name, base_path)
    return dependencies


def generate_plantuml(dependencies: Dict[str, Set[str]]) -> str:
    plantuml = ["@startuml"]
    for package, deps in dependencies.items():
        for dep in deps:
            plantuml.append(f'  "{package}" -> "{dep}"')
    plantuml.append("@enduml")
    return "\n".join(plantuml)


def main():
    if len(sys.argv) != 2:
        print("Использование: py hw2.py <путь_к_конфигурационному_файлу>", file=sys.stderr)
        sys.exit(1)

    config_path = sys.argv[1]
    if not os.path.exists(config_path):
        print(f"Конфигурационный файл {config_path} не найден.", file=sys.stderr)
        sys.exit(1)

    config = parse_config(config_path)
    
    package_name = config.get("package_name")
    output_path = config.get("output_file")
    max_depth = config.get("max_depth", float('inf'))

    if not all([package_name, output_path]):
        print("Ошибка: Конфигурационный файл должен содержать все обязательные поля.", file=sys.stderr)
        sys.exit(1)

    base_path = "./node_modules" 
    dependencies = parse_dependencies(package_name, base_path, max_depth)

    if not dependencies:
        print(f"Не удалось найти зависимости для пакета {package_name}.", file=sys.stderr)
        sys.exit(1)

    plantuml_code = generate_plantuml(dependencies)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(plantuml_code)
    
    print(f"Граф зависимостей сохранен в {output_path}.")
    
    print(plantuml_code)


if __name__ == "__main__":
    main()
