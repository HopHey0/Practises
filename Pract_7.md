# Практическое занятие №7. Генераторы документации

П.Н. Советов, РТУ МИРЭА

## Задача 1

Реализовать с помощью математического языка LaTeX нижеприведенную формулу:

![image](https://github.com/user-attachments/assets/109314c9-6a07-4f35-8d9b-bc4efdd2e034)

Прислать код на LaTeX и картинку-результат, где, помимо формулы, будет указано ФИО студента.

## Решение:

```LaTeX
\documentclass{article}
\usepackage{amsmath} 

\title{Task_1}
\author{mishavsit }
\date{November 2024}

\begin{document}

\[
\int\limits_{x}^{\infty} \frac{dt}{t(t^2-1)\log t} = 
\int\limits_{x}^{\infty} \frac{1}{t \log t} 
\left( \sum_m t^{-2m} \right) dt = 
\sum_m \int\limits_{x}^{\infty} \frac{t^{-2m}}{t\log t} \, dt 
\overset{(u = t^{-2m})}{=} 
-\sum_m \operatorname{li}(x^{-2m})
\]

\bigskip

\textbf{Name:} Student Sitnov M.V.

\end{document}

```
![image](https://github.com/user-attachments/assets/fbcba8f7-4d04-405a-bc9a-a12bf813d2c7)

## Задача 2

На языке PlantUML реализовать диаграмму на рисунке ниже. Прислать текст на PlantUML и картинку-результат, в которой ФИО студента заменены Вашими собственными.
Обратите внимание на оформление, желательно придерживаться именно его, то есть без стандартного желтого цвета и проч. Чтобы много не писать используйте псевдонимы с помощью ключевого слова "as".

Используйте [онлайн-редактор](https://plantuml-editor.kkeisuke.com/).

![image](https://github.com/user-attachments/assets/aa052379-cb9c-4f8a-a32e-33f349954cba)

## Решение:
```PlantUML
# PlantUML Editor

@startuml
actor "Студент Ситнов М.В." as Student
database "Piazza" as Piazza
actor "Преподаватель" as Teacher

Teacher -> Piazza: Публикация задачи
activate Piazza
Piazza --> Teacher: Задача опубликована
deactivate Piazza


Student --> Piazza: Поиск задач
activate Piazza
Piazza --> Student: Получение задачи
deactivate Piazza

Student -> Piazza: Публикация решения
activate Piazza
Piazza --> Student: Решение опубликовано
deactivate Piazza

Teacher -> Piazza: Поиск решений
activate Piazza
Piazza --> Teacher: Решение найдено
Teacher -> Piazza: Публикация оценки
Piazza --> Teacher: Оценка опубликована
deactivate Piazza

Student -> Piazza: Проверка оценки
Piazza --> Student: Оценка получена

@enduml
```
![image](https://github.com/user-attachments/assets/e90f5281-8370-4968-ae63-edd5883e92de)


## Задача 3

Описать какой-либо алгоритм сортировки с помощью noweb. Язык реализации не важен. Прислать nw-файл, pdf-файл и файл с исходным кодом. В начале pdf-файла должно быть указано ваше авторство. Добавьте, например, где-то в своем тексте сноску: \footnote{Разработал Фамилия И.О.}
Дополнительное задание: сравните "грамотное программирование" с Jupyter-блокнотами (см. https://github.com/norvig/pytudes/blob/master/ipynb/BASIC.ipynb), опишите сходные черты, различия, перспективы того и другого.

## Решение:
```noweb
\documentclass{report}
\usepackage[utf8]{inputenc}
\usepackage[russian]{babel}
\usepackage{listings}  % Подключение пакета для кода

\begin{document}

\chapter{Алгоритм сортировки пузырьком}

Этот документ описывает алгоритм сортировки пузырьком с использованием noweb.

\section{Описание алгоритма}

Алгоритм сортировки пузырьком многократно проходит через список, сравнивая соседние элементы и меняя их местами, если они стоят в неправильном порядке.

\subsection{Шаги алгоритма}

1. Проходим по списку.
2. Сравниваем соседние элементы.
3. Меняем их местами, если они стоят в неправильном порядке.
4. Повторяем процесс, пока список не станет отсортированным.

\section{Исходный код}

\subsection{Алгоритм сортировки пузырьком}

\begin{lstlisting}[language=Python]
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

if __name__ == "__main__":
    array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", array)
    sorted_array = bubble_sort(array)
    print("Sorted array:", sorted_array)
\end{lstlisting}

\footnote{Разработал Ситнов МВ} 

\section{Заключение}

Алгоритм сортировки пузырьком является простым, но неэффективным для больших наборов данных, так как его временная сложность составляет \(O(n^2)\).

\end{document}

```
Файлы:
[bubble_sort.nw](https://github.com/HopHey0/Practises/blob/main/bubble_sort.nw)


## Задача 4

Выбрать программный проект из нескольких файлов (лучше свой собственный), состоящий из нескольких файлов. Получить для него документацию в Doxygen. Язык реализации не важен. Должны быть сгенерированы: описания классов и функций, диаграммы наследования, диаграммы графа вызовов функции. Прислать pdf-файл с документацией (см. latex/make.bat), в котором будет указано ваше авторство. Необходимо добиться корректного вывода русского текста.
 
## Задача 5

Выбрать программный проект на Python (лучше свой собственный), состоящий из нескольких файлов. Получить для него документацию в Doxygen. Должны быть сформированы: руководство пользователя и руководство программиста. Руководство программиста должно содержать описание API, полученное с использованием расширения autodoc. Для каждого из модулей должна присутствовать диаграмма наследования и подробное описание классов и функций (назначение, описание параметров и возвращаемых значений), извлеченных из docstring. Прислать pdf-файл с документацией, в котором будет указано ваше авторство и весь авторский текст приведен на русском языке.

## Полезные ссылки

**LaTeX**

http://grammarware.net/text/syutkin/TextInLaTeX.pdf

https://grammarware.net/text/syutkin/MathInLaTeX.pdf

https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes

https://www.overleaf.com/learn/latex/XeLaTeX

**Noweb**

https://www.pbr-book.org/3ed-2018/Introduction/Literate_Programming

https://www.cs.tufts.edu/~nr/noweb/

**Doxygen**

https://www.doxygen.nl/index.html

https://habr.com/ru/post/252101/

**Sphinx**

https://www.sphinx-doc.org/en/master/

https://sphinx-ru.readthedocs.io/ru/latest/index.html

https://breathe.readthedocs.io/en/latest/


**PlantUML**

https://plantuml.com/ru/

https://pdf.plantuml.net/PlantUML_Language_Reference_Guide_ru.pdf

**Mermaid**

https://mermaid.js.org/

https://mermaid.live/edit

https://mermaid.js.org/

https://mermaid.live/edit
