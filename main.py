import sqlite3
from tkinter import Tk, filedialog
import requests
from reader.reader import read_book

def create_table():
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT DEFAULT 'Нет данных',
                 author TEXT DEFAULT 'Нет данных',
                 publisher TEXT DEFAULT 'Нет данных',
                 description TEXT DEFAULT 'Нет данных',
                 date_book INTEGER,
                 language_book TEXT DEFAULT 'Нет данных',
                 text TEXT DEFAULT 'Нет данных',
                 tags TEXT DEFAULT 'Нет данных',
                 format TEXT DEFAULT 'Нет данных',
                 cover TEXT DEFAULT 'Нет данных',
                 series TEXT DEFAULT 'Нет данных',
                 series_index INTEGER,
                 path TEXT DEFAULT 'Нет данных',
                 categories TEXT DEFAULT 'Нет данных'
                 )''')
    conn.commit()
    conn.close()

def get_book(book, cursor):
    cursor.execute(f"SELECT * FROM books WHERE id= '{book}'")
    metadata = cursor.fetchone()
    conn.close()
    return metadata



def get_books():
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books'")
    result = cursor.fetchone()
    if result is None:
        print("Книги еще не добавлены!")
    else:
        cursor.execute("SELECT id FROM books")
        books = cursor.fetchall()
        cursor.execute("SELECT * FROM books")
        books_fetch = cursor.fetchall()
        # для получения одной книги
        # for i in books: #list(map(lambda x: str(x).strip("(),"), books)):
        #     print(get_book(i[0], cursor))
        conn.close()
        return books_fetch


def update_books(metadata):
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title=?, author=?, publisher=?, description=?, subject=?, date_book=?, language_book=?, " +
                   "text=?, tags=?, format=?, cover=?, series=?, series_index=?, path=? WHERE id=?",
              (metadata['title'], (metadata['author']), metadata['publisher'],
               metadata['description'], metadata['date'], metadata['language'],
               metadata['text'], metadata['tags'], metadata['format'], metadata['cover'],
               metadata['series'], metadata['series_index'], metadata['path']))
    conn.commit()
    conn.close()

def update_field(book_id, field_name, text):
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE books SET {field_name} = ? WHERE id = ?", ((text, book_id)))
    conn.commit()


def add_book(metadata):
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE path=?", (metadata['path'],))
    isAlreadyExist = cursor.fetchone()
    if isAlreadyExist: return
    cursor.execute('''
        INSERT INTO books (title, author, publisher, description, date_book, language_book, text, tags, format, cover,
        series, series_index, path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (metadata['title'], (metadata['author']), metadata['publisher'],
           metadata['description'], metadata['date'], metadata['language'],
           metadata['text'], metadata['tags'], metadata['format'], metadata['cover'],
           metadata['series'], metadata['series_index'], metadata['path']))
    conn.commit()
    print("Книга добавлена!")


def search_book(query):
    url = 'https://www.googleapis.com/books/v1/volumes'
    params = {'q': query}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'items' in data:
            book = data['items'][0]['volumeInfo']
            title = book.get('title', 'Нет данных')
            author = book.get('authors', 'Нет данных')
            description = book.get('description', 'Нет данных')
            date = book.get('date', 'Нет данных')
            publisher = book.get('publisher', 'Нет данных')
            language = book.get('language', 'Нет данных')

            book_info = {
                'title': title,
                'author': str(author).strip("[]'"),
                #'publisher': publisher,
                'description': description,
                'date': date,
                'language': language,
            }
            return book_info

        else:
            print('По заданному запросу ничего не удалось найти!')
            return None

    except requests.exceptions.RequestException as e:
        print('Ошибка при выполнении запроса:', e)
        return None


def extract_metadata(file):
    book = read_book(file)
    try:
        text = book.text
        meta = book.metadata
        if not (isinstance(meta, str)):
            print(meta)
            metadata = {
                'title': str(meta.title),
                'author': str(meta.author_list).strip("[]'"),
                'publisher': str(meta.publish_info.publisher),
                'description': str(meta.description).replace('\xa0', ' '),
                'date': meta.publish_info.year,
                'language': str(meta.lang),
                'text': text,
                'tags': str(meta.tag_list).strip("[]'"),
                'format': meta.format,
                'cover': meta.cover_image_data,
                'series': meta.series,
                'series_index': meta.series_index,
                'path': meta.file
            }
            return metadata
        return {'title': None, 'author': None, 'publisher': None, 'description': None, 'date': None, 'language': None,
                'text': text, 'tags': None,  'format': None, 'cover': None, 'series': None, 'series_index': None, 'path': file}
    except:
        return book

if __name__ == "__main__":
    root = Tk()
    while True:
        conn = sqlite3.connect('metadata.db')
        cursor = conn.cursor()

        print('-'*20)
        print('1. Добавить книгу')
        print('2. Показать все книги')
        print('3. Удалить все книги')
        print('4. Выйти')
        print('5. Изменить поле')
        print(' ')
        choice = input('Выберите команду: ')

        if choice == '1':
            print('1. Добавить файл')
            print('2. Загрузить данные из интернета')
            print(' ')
            secondChoice = input('Выберите команду: ')
            if secondChoice == '1':
                print('Выберете файл')
                selectedFile = filedialog.askopenfilename()
                root.withdraw()
                create_table()
                metadata = extract_metadata(selectedFile)
                if (isinstance(metadata, str)):
                    print(metadata)
                    continue
                add_book(metadata)
            elif secondChoice == '2':
                create_table()
                newBook = search_book(input('Введите название книги ') + 'книга')
                add_book(newBook)

        elif choice == '2':
            get_books()
        elif choice == '3':
            cursor.execute('''DROP TABLE IF EXISTS books''')
            print("Книги удалены!")
        elif choice == '4':
            break
        elif choice == '5':
            book_id = input('Введите ид книги: ')
            field_name = input('Введите имя поля книги: ')
            text = input('Введите текст : ')
            update_field(book_id, field_name, text)
    else:
        print('Некорректный выбор. Попробуйте снова!')
