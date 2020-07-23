## Описание
Скрипт написан в образовательных целях, согласно Уроку №4 "Верстаем онлайн-библиотеку" модуля "Вёрстка для питониста", 

Скрипт создает локальный сайт на основании данных, полученных ранее, с [помощью Урока №3.](https://github.com/dej-e/library_parser.git)  

## Запуск

Для запуска скрипта у вас уже должен быть установлен Python 3.

- Скачайте код
- Установите зависимости командой `pip install -r requirements.txt`
- Поместите файл `books_description.json` и директории с картинками `images` и книгами `books` в директорию со скриптом.
- Запустите скрипт командой `python3 render_website.py`

В случае успешного запуска скрипт сгенерирет странички сайта.  
Странички будут лежать в папке `pages` и, например первая страничка, будет доступна по адресу: [http://127.0.0.1:5500/pages/index1.html](http://127.0.0.1:5500/pages/index1.html).

Пример работы скрипта также доступен на сайте: [https://dej-e.github.io/online_lib_layout/pages/index1.html](https://dej-e.github.io/online_lib_layout/pages/index1.html)

Для перехода по страничкам используйте *пагинатор*, расположенный над карточками с описанием книг.

 ## Аргументы командной строки

По умолчанию, на одной страничке располагается 20 карточек с описанием книг. Для указания произвольного количества книг на странице, используейте агрумент `books`. 
Например:
 - `python render_website.py --books 60` - отображаем на каждой страничке по 60 книжек.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).