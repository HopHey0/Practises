# 1. Клонирование репозитория

Склонируйте репозиторий с исходным кодом и тестами:

```
git clone <URL репозитория>
cd <директория проекта>
```

# 2. Установка зависимостей при запуске

```
pip install subprocess

```

# Создайте виртуальное окружение

```bash
# Активируйте виртуальное окружение
python -m venv venv
# Для Windows:
venv\Scripts\activate
# Для MacOS/Linux:
source venv/bin/activate
```


# 3. Структура проекта
Проект содержит следующие файлы и директории:
```bash
unittests.py              # файл для тестирования
config.yaml             # конфигурационный файл 
hw2.py                  # файл с программой
plantuml.jar           # plantuml - визуализатор
file.puml             # файл с выводом программы 
```

# 4. Запуск проекта
```bash
npm install express       #установка пакета npm install Axios  установленный пакет надо указать в config
py hw2.py config.yaml     # py файл с программой конфигурационный файл
```
