import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from http.server import HTTPServer, SimpleHTTPRequestHandler
from livereload import Server, shell
from more_itertools import chunked
import math, os


def on_reload():
    render_index_page('books_description.json')


def parse_json(filename):
    return json.load(open(filename, encoding='utf-8'))


def render_index_pages(template, books_description, step):
    books_count = len(books_description)
    total_pages = math.ceil(books_count / step)
    page_numbers = list(range(1, total_pages + 1))
    print(page_numbers)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template(template)

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


def main():
    try:
        with open("books_description.json", "r", encoding='utf-8') as my_file:
            books_description_json = my_file.read()
    except FileNotFoundError:
        print('File "books_description.json" does not exist')
        exit()
    books_description = json.loads(books_description_json)

    render_index_pages('template.html', books_description, 20)
    live_server = Server()
    live_server.watch('template.html', on_reload)

    render_index_pages('template.html', books_description, 20)
    # render_index_page(books_description)

    # server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    # server.serve_forever()
    #live_server.serve(root='pages/.')
    live_server.serve(root='.')


if __name__ == '__main__':
    main()
