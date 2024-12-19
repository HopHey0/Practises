# 1. Клонирование репозитория

Склонируйте репозиторий с исходным кодом и тестами:

```
git clone <URL репозитория>
cd <директория проекта>
```

# 2. Установка зависимостей при запуске

```
pip install tarfile
pip install argparse
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
tests.py              # файл для тестирования 
emulator.py                  # файл с программой
testdir.zip           # тестовый архив для работы
somename.csv           # файл с логами(имя зависит от ввода
```

# 4. Запуск проекта
```bash
py emulator.py username testdir.zip somename.csv    # py программа с эмулятором, имя пользователя, архив, файл с логами
```
