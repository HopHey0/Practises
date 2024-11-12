# Практическое задание №4. Системы контроля версий

П.Н. Советов, РТУ МИРЭА

Работа с Git.

## Задача 1

На сайте https://onlywei.github.io/explain-git-with-d3 или http://git-school.github.io/visualizing-git/ (цвета могут отличаться, есть команды undo/redo) с помощью команд эмулятора git получить следующее состояние проекта (сливаем master с first, перебазируем second на master): см. картинку ниже. Прислать свою картинку.

## Решение
![image](https://github.com/user-attachments/assets/655a80a7-3a8b-4142-bc33-714bf821e736)
```
git commit
git tag in
git branch first
git branch second
git commit
git commit
git checkout first
git commit
git commit
git checkout second
git commit
git commit
git checkout master
git merge first
git checkout second
git rebase master
git checkout master
git merge second
git checkout in!

```


## Задача 2

Создать локальный git-репозиторий. Задать свои имя и почту (далее – coder1). Разместить файл prog.py с какими-нибудь данными. Прислать в текстовом виде диалог с git.
## Решение
```
Aorus@HOME-PC MINGW64 ~/Desktop/Pract_4 (master)
$ git init
Initialized empty Git repository in C:/Users/Aorus/Desktop/Pract_4/.git/

Aorus@HOME-PC MINGW64 ~/Desktop/Pract_4 (master)
$ git config user.name "coder1"

Aorus@HOME-PC MINGW64 ~/Desktop/Pract_4 (master)
$ git config user.email "example@mail.com"

Aorus@HOME-PC MINGW64 ~/Desktop/Pract_4 (master)
$ echo "print('Holy cow')" >> prog.py

Aorus@HOME-PC MINGW64 ~/Desktop/Pract_4 (master)
$ git add prog.py

Aorus@HOME-PC MINGW64 ~/Desktop
git commit

[master (root-commit) e21e93f] First commit
 1 file changed, 1 insertion(+)
 create mode 100644 prog.py

Aorus@HOME-PC MINGW64 ~/Desktop/Pract_4 (master)
$ git log
commit e21e93f80b4d8a6dde8369919dfbdb937fcd62e0 (HEAD -> master)
Author: coder1 <example@mail.com>
Date:   Wed Nov 13 00:15:30 2024 +0300

    First commit


```

## Задача 3

Создать рядом с локальным репозиторием bare-репозиторий с именем server. Загрузить туда содержимое локального репозитория. Команда git remote -v должна выдать информацию о server! Синхронизировать coder1 с server.

Клонировать репозиторий server в отдельной папке. Задать для работы с ним произвольные данные пользователя и почты (далее – coder2). Добавить файл readme.md с описанием программы. Обновить сервер.

Coder1 получает актуальные данные с сервера. Добавляет в readme в раздел об авторах свою информацию и обновляет сервер.

Coder2 добавляет в readme в раздел об авторах свою информацию и решает вопрос с конфликтами.

Прислать список набранных команд и содержимое git log.

Пример лога коммитов:

```
*   commit a457d748f0dab75b4c642e964172887de3ef4e3e
|\  Merge: 48ce283 d731ba8
| | Author: Coder 2 <coder2@corp.com>
| | Date:   Sun Oct 11 11:27:09 2020 +0300
| | 
| |     readme fix
| | 
| * commit d731ba84014d603384cc3287a8ea9062dbb92303
| | Author: Coder 1 <coder1@corp.com>
| | Date:   Sun Oct 11 11:22:52 2020 +0300
| | 
| |     coder 1 info
| | 
* | commit 48ce28336e6b3b983cbd6323500af8ec598626f1
|/  Author: Coder 2 <coder2@corp.com>
|   Date:   Sun Oct 11 11:24:00 2020 +0300
|   
|       coder 2 info
| 
* commit ba9dfe9cb24316694808a347e8c36f8383d81bbe
| Author: Coder 2 <coder2@corp.com>
| Date:   Sun Oct 11 11:21:26 2020 +0300
| 
|     docs
| 
* commit 227d84c89e60e09eebbce6c0b94b41004a4541a4
  Author: Coder 1 <coder1@corp.com>
  Date:   Sun Oct 11 11:11:46 2020 +0300
  
      first commit
```
##Решение
```
cd ~/Desktop/Pract_4
git init --bare ~/server
git remote add server ~/server
git push server master
git remote -v

cd ~/Desktop
git clone server clone
cd clone
git config user.name "coder2"
git config user.email "example2@meil.com"
echo "Sample" > readme.md
git add readme.md
git commit -m "Add readmi file"
git push origin master

cd ~/Desktop/Pract_4
git pull server master
echo -e "Authors: coder1" >> readme.md
git add readme.md
git commit -m "Add author in readme file"
git push server master

cd ~/Desktop/clone
git pull origin master
echo "coder2" >> readme.md
git add readme.md
git commit -m "Another author to readme file"
git push origin master

git log --oneline --graph --all
```
Логи:

```
* 49cbcfe (HEAD -> master, origin/master) Another author to readme file
* 73d4a1e Add readmi file

```
## Задача 4

Написать программу на Питоне (или другом ЯП), которая выводит список содержимого всех объектов репозитория. Воспользоваться командой "git cat-file -p". Идеальное решение – не использовать иных сторонних команд и библиотек для работы с git.

## Полезные ссылки

Git

Учебник (рус.): https://git-scm.com/book/ru/v2

Шпаргалка (рус.): https://training.github.com/downloads/ru/github-git-cheat-sheet/

Официальная документация: https://git-scm.com/docs

Эксцентричный доклад Л. Торвальдса о Git: https://www.youtube.com/watch?v=4XpnKHJAok8

Дерево Меркла: http://cryptowiki.net/index.php?title=Дерево_Merkle

Git for Windows: https://git-scm.com/download/win

Репозиторий chibicc: https://github.com/rui314/chibicc.git

Игра по git: https://learngitbranching.js.org/?locale=ru_RU

SHA-1

Описание алгоритма: https://ru.wikipedia.org/wiki/SHA-1

Вероятность хеш-коллизии: https://preshing.com/20110504/hash-collision-probabilities/

https://ru.m.wikipedia.org/wiki/Парадокс_дней_рождения

https://security.googleblog.com/2017/02/announcing-first-sha1-collision.html
