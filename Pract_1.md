# Практическое занятие №1. Введение, основы работы в командной строке

П.Н. Советов, РТУ МИРЭА

Научиться выполнять простые действия с файлами и каталогами в Linux из командной строки. Сравнить работу в командной строке Windows и Linux.

## Задача 1

Вывести отсортированный в алфавитном порядке список имен пользователей в файле passwd (вам понадобится grep).
## Решение:
![image](https://github.com/user-attachments/assets/5ab203c4-7339-4350-abc9-524648e35728)


## Задача 2

Вывести данные /etc/protocols в отформатированном и отсортированном порядке для 5 наибольших портов, как показано в примере ниже:

```
[root@localhost etc]# cat /etc/protocols ...
142 rohc
141 wesp
140 shim6
139 hip
138 manet
```
## Решение:
![image](https://github.com/user-attachments/assets/dc5a21be-07e3-4ef3-92bd-8c65bd08a7e7)

## Задача 3

Написать программу banner средствами bash для вывода текстов, как в следующем примере (размер баннера должен меняться!):

```
[root@localhost ~]# ./banner "Hello from RTU MIREA!"
+-----------------------+
| Hello from RTU MIREA! |
+-----------------------+
```

Перед отправкой решения проверьте его в ShellCheck на предупреждения.

## Решение:
```Bash
#!/bin/bash

text="$1"
length=${#text}

banner_width=$((length + 4))

border=$(printf "%-${banner_width}s" "+" | tr ' ' '-')

echo "$border"
echo "| $text |"
echo "$border"
```
![image](https://github.com/user-attachments/assets/7b02252d-6671-4446-b0d4-e9b4ab3fbeda)


## Задача 4

Написать программу для вывода всех идентификаторов (по правилам C/C++ или Java) в файле (без повторений).

Пример для hello.c:

```
h hello include int main n printf return stdio void world
```
## Решение:
![image](https://github.com/user-attachments/assets/959c9fcf-57e3-4b0c-bc3e-a32b6d1c5527)
```Bash
#!/bin/bash
file=$1
grep -o '\b[_a-zA-Z][_a-zA-Z0-9]*\b' "$file" | sort | uniq
```

## Задача 5

Написать программу для регистрации пользовательской команды (правильные права доступа и копирование в /usr/local/bin).

Например, пусть программа называется reg:

```
./reg banner
```

В результате для banner задаются правильные права доступа и сам banner копируется в /usr/local/bin.
##Решение:
```Bash
#!/bin/bash
BIN_DIR="C:/Conf_work"

cp "$1" "$BIN_DIR/"

echo "Adding $BIN_DIR to PATH..."
export PATH="$BIN_DIR:$PATH"

echo "Now you can run the program by just typing its name in the terminal."
```
![image](https://github.com/user-attachments/assets/888931f8-2c52-4e1b-97e8-0b9756a04b68)


## Задача 6

Написать программу для проверки наличия комментария в первой строке файлов с расширением c, js и py.
##Решение:
```Bash
#!/bin/bash
check_comment() {
    file=$1
    extension="${file##*.}"
    
    if [[ "$extension" == "c" || "$extension" == "js" || "$extension" == "py" ]]; then
        first_line=$(head -n 1 "$file")
        
        case $extension in
            c)
                if [[ "$first_line" =~ ^\s*// ]]; then
                    echo "Файл $file: комментарий в первой строке."
                else
                    echo "Файл $file: нет комментария в первой строке."
                fi
                ;;
            js)
                if [[ "$first_line" =~ ^\s*// ]]; then
                    echo "Файл $file: комментарий в первой строке."
                else
                    echo "Файл $file: нет комментария в первой строке."
                fi
                ;;
            py)
                if [[ "$first_line" =~ ^\s*# ]]; then
                    echo "Файл $file: комментарий в первой строке."
                else
                    echo "Файл $file: нет комментария в первой строке."
                fi
                ;;
            *)
                # Если файл не с нужным расширением
                echo "Файл $file не имеет нужного расширения (c, js, py)."
                ;;
        esac
    else
        echo "Файл $file не имеет нужного расширения (c, js, py)."
    fi
}
check_comment "$1"
```
![image](https://github.com/user-attachments/assets/020ed9bf-72ec-4006-8794-dcfa10356357)


## Задача 7

Написать программу для нахождения файлов-дубликатов (имеющих 1 или более копий содержимого) по заданному пути (и подкаталогам).
##Решение:
```Bash
#!/bin/bash
directory="$1"
declare -A file_hashes

find "$directory" -type f | while read -r file; do
    hash=$(sha256sum "$file" | awk '{ print $1 }')
    if [[ -n "${file_hashes[$hash]}" ]]; then
        echo "Дубликат найден: $file и ${file_hashes[$hash]}"
    else
        file_hashes["$hash"]="$file"
    fi
done
```
![image](https://github.com/user-attachments/assets/f366bb03-c5d3-401f-a804-d9b7ee8bde9b)

## Задача 8

Написать программу, которая находит все файлы в данном каталоге с расширением, указанным в качестве аргумента и архивирует все эти файлы в архив tar.
##Решение:
```Bash
#!/bin/bash
directory="$1"
extension="$2"

shopt -s nullglob
files=("$directory"/*."$extension")

archive_name="${directory%/}.tar"
tar -cvf "$archive_name" -C "$directory" $(basename -a "${files[@]}")

echo "Архив '$archive_name' успешно создан."

```
![image](https://github.com/user-attachments/assets/26ffc6f3-f0f4-4fc0-81c1-076e0df8e8cb)


## Задача 9

Написать программу, которая заменяет в файле последовательности из 4 пробелов на символ табуляции. Входной и выходной файлы задаются аргументами.

## Задача 10

Написать программу, которая выводит названия всех пустых текстовых файлов в указанной директории. Директория передается в программу параметром. 

## Полезные ссылки

Линукс в браузере: https://bellard.org/jslinux/

ShellCheck: https://www.shellcheck.net/

Разработка CLI-приложений

Общие сведения

https://ru.wikipedia.org/wiki/Интерфейс_командной_строки
https://nullprogram.com/blog/2020/08/01/
https://habr.com/ru/post/150950/

Стандарты

https://www.gnu.org/prep/standards/standards.html#Command_002dLine-Interfaces
https://www.gnu.org/software/libc/manual/html_node/Argument-Syntax.html
https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html

Реализация разбора опций

Питон

https://docs.python.org/3/library/argparse.html#module-argparse
https://click.palletsprojects.com/en/7.x/
