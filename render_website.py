import argparse
import json
import math
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
from pathlib import Path


def on_reload():
    render_index_pages(template, books_description, step)
    print("template changed.  reloading.")


def render_index_pages(template, books_description, step):
    books_count = len(books_description)
    total_pages = math.ceil(books_count / step)
    page_numbers = list(range(1, total_pages + 1))

    folder = 'pages'
    os.makedirs(folder, exist_ok=True)
    page_number = 1

    for books in range(0, books_count, step):
        rendered_page = template.render(
            books=list(chunked(books_description[books:books + step], 2)),
            page_numbers=page_numbers,
            current_page=page_number,
            next_page=page_number + 1,
            previous_page=page_number - 1,
        )
        filename = f'index{page_number}.html'
        filename_path = os.path.join(folder, filename)
        with open(filename_path, 'w', encoding='utf-8') as file:
            file.write(rendered_page)
        page_number += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Library creater (tululu.org)'
    )
    parser.add_argument('--books',
                        default=20,
                        help='Books per page (default 20)'
                        )
    args = parser.parse_args()

    step = int(args.books)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    old_pages = sorted(Path('pages').glob('*.*'))
    for file in old_pages:
        os.unlink(file)

    try:
        with open("books_description.json", "r",
                  encoding='utf-8') as book_file:
            books_description_json = book_file.read()
    except FileNotFoundError:
        print('File "books_description.json" does not exist')
        exit()
    books_description = json.loads(books_description_json)

    render_index_pages(template, books_description, step)

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', )
