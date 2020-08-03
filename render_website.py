import argparse
import json
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
from pathlib import Path


def on_reload():
    render_index_pages(env, chunks)
    print("template changed.  reloading.")


def render_index_pages(env, chunks):
    template = env.get_template('template.html')
    max_page_number = len(chunks)

    folder = 'pages'
    os.makedirs(folder, exist_ok=True)

    for page_number, books in enumerate(chunks):
        current_page_number = page_number

        rendered_page = template.render(
            books=books,
            current_page_number = current_page_number,
            max_page_number = max_page_number,
        )
        filename = f'index{page_number}.html'
        filename_path = os.path.join(folder, filename)
        with open(filename_path, 'w', encoding='utf-8') as file:
            file.write(rendered_page)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Library creater (tululu.org)'
    )
    parser.add_argument('--books',
                        default=20,
                        help='Books per page (default 20)'
                        )
    args = parser.parse_args()

    books_per_page = int(args.books)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    old_pages = Path('pages').glob('*.*')
    for old_page in old_pages:
        os.unlink(old_page)

    try:
        with open("books_description.json", "r",
                  encoding='utf-8') as book_file:
            books_description_json = book_file.read()
    except FileNotFoundError:
        print('File "books_description.json" does not exist')
        exit()
    books_description = json.loads(books_description_json)
    chunks = list(chunked(books_description, books_per_page))

    render_index_pages(env, chunks)
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', )
