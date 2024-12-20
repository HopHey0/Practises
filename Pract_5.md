# Практическое занятие №5. Вопросы виртуализации

П.Н. Советов, РТУ МИРЭА

## Задача 1

Исследование виртуальной стековой машины CPython.

Изучите возможности просмотра байткода ВМ CPython.

```
import dis

def foo(x):
    while x:
        x -= 1
    return x + 1

print(dis.dis(foo))
```

Опишите по шагам, что делает каждая из следующих команд (приведите эквивалентное выражение на Python):

 11           0 LOAD_FAST                0 (x)
              2 LOAD_CONST               1 (10)
              4 BINARY_MULTIPLY
              6 LOAD_CONST               2 (42)
              8 BINARY_ADD
             10 RETURN_VALUE

## Решение:
### Байткод и пояснение:
```Python
11  0 LOAD_FAST                0 (x)           # Загружает значение переменной x в стек
    2 LOAD_CONST               1 (10)          # Загружает константу 10 в стек
    4 BINARY_MULTIPLY                          # Берёт две переменные из вершина стека и перемножает их (умножает значение x на 10)
    6 LOAD_CONST               2 (42)          # Загружает константу 42  стек
    8 BINARY_ADD                              # Берёт две переменные из вершины стека(x * 10 и 42) и складывает их
   10 RETURN_VALUE                            # Возвращает итоговое значение
```
### Эквивалент в Python:
```Python
def func(x):
    return (x * 10) + 42
```
## Задача 2

Что делает следующий байткод (опишите шаги его работы)? Это известная функция, назовите ее.

```
  5           0 LOAD_CONST               1 (1)
              2 STORE_FAST               1 (r)

  6     >>    4 LOAD_FAST                0 (n)
              6 LOAD_CONST               1 (1)
              8 COMPARE_OP               4 (>)
             10 POP_JUMP_IF_FALSE       30

  7          12 LOAD_FAST                1 (r)
             14 LOAD_FAST                0 (n)
             16 INPLACE_MULTIPLY
             18 STORE_FAST               1 (r)

  8          20 LOAD_FAST                0 (n)
             22 LOAD_CONST               1 (1)
             24 INPLACE_SUBTRACT
             26 STORE_FAST               0 (n)
             28 JUMP_ABSOLUTE            4

  9     >>   30 LOAD_FAST                1 (r)
             32 RETURN_VALUE
```
## Решение:
Этот байткод описывает вычисление факториала числа.
```Python
   5          0 LOAD_CONST               1 (1)      # Загружает константу 1
              2 STORE_FAST               1 (r)      # Сохраняет значение 1 в переменную r

  6     >>    4 LOAD_FAST                0 (n)      # Загружает значение n
              6 LOAD_CONST               1 (1)      # Загружает константу 1
              8 COMPARE_OP               4 (>)      # ? n > 1
             10 POP_JUMP_IF_FALSE        30         # Если предыдущая строка false - переходит к адресу 30

  7          12 LOAD_FAST                1 (r)      # Загружает значение r
             14 LOAD_FAST                0 (n)      # Загружает значение n
             16 INPLACE_MULTIPLY                    # Умножает n на r
             18 STORE_FAST               1 (r)      # Сохраняет результат в r

  8          20 LOAD_FAST                0 (n)      # Загружает значение n
             22 LOAD_CONST               1 (1)      # Загружает константу 1
             24 INPLACE_SUBTRACT                    # Вычитает 1 из n и сохраняет обратно
             26 STORE_FAST               0 (n)      # Сохраняет результат обратно в n
             28 JUMP_ABSOLUTE            4          # Переходит к адресу 4

  9     >>   30 LOAD_FAST                1 (r)      # Загружает значение r (итоговый результат)
             32 RETURN_VALUE                        # Возвращает r как результат функции
```
Эквивалент на Python соответственно:
```python
def factorial(n):
    r = 1
    while (n > 1):
        r *= n
        n -= 1
    return r
```

## Задача 3

Приведите результаты из задач 1 и 2 для виртуальной машины JVM (Java) или .Net (C#).

## Решение:
### Задача 1(Java):
```Java
public static int calculate(int x) {
        return x * 10 + 42;
    }
```
```JVM
  public static int calculate(int);
       0: iload_0
       1: bipush        10
       3: imul
       4: bipush        42
       6: iadd
       7: ireturn
```
### Задача 2(Java):
```Java
public static int factorial(int n){
    int r = 1;
    while (n > 1){
        r *= n;
        n -= 1;
    }
    return r;
}
```
```JVM
public static int factorial(int);
       0: iconst_1
       1: istore_1
       2: iload_0
       3: iconst_1
       4: if_icmple     
       7: iload_1
       8: iload_0
       9: imul
      10: istore_1
      11: iinc          
      14: goto         
      17: iload_1
      18: ireturn
```
## Задача 4

Работа с qemu. Скачать и установить ISO-образ Alpine Linux для виртуальных машин с официального сайта.
Создать с помощью qemu образ жесткого диска (опция -f qcow2). Объем диска 500 Мб.
Запустить Alpine Linux с CD-ROM.
Установить систему на sda. Изменить motd.
Загрузиться уже с sda.
Прислать полный список команд для установки и загрузки, а также скриншот с motd, где фигурируют ваши имя и фамилия.

## Задача 5

(после разбора на семинаре и написания у доски базовой части эмулятора древней игровой приставки CHIP-8)

1. Реализовать вывод на экран.
2. Добиться запуска Тетриса.
3. Реализовать ввод с клавиатуры.
4. Добиться успешной работы всех приложений.

[Архив эмулятора CHIP-8](chip.zip)

## Полезные ссылки

Compiler Explorer: https://godbolt.org/

Байткод CPython: https://docs.python.org/3/library/dis.html

QEMU для Windows: https://www.qemu.org/download/#windows
http://sovietov.com/tmp/mqemu.zip

Документация по QEMU: https://www.qemu.org/docs/master/system/index.html

Старая документация по QEMU (рус.): https://www.opennet.ru/docs/RUS/qemu_doc/

Образы Alpine Linux: https://alpinelinux.org/downloads/

Документация по игровому компьютеру CHIP-8: http://devernay.free.fr/hacks/chip8/C8TECH10.HTM

Учебник по созданию миниатюрной ОС: https://www.cs.bham.ac.uk/~exr/lectures/opsys/10_11/lectures/os-dev.pdf

Nasm: https://nasm.us/

Прерывания BIOS: http://www.ctyme.com/intr/int.htm

Игры в загрузочном секторе: https://github.com/nanochess/Invaders
