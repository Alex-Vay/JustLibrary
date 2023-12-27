import sqlite3
from tkinter import Tk, filedialog
import requests
from reader.reader import readBook
import multiprocessing
import pyttsx3
import keyboard

def createTable():
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
                 categories TEXT DEFAULT 'Нет данных',
                 last_fragment FLOAT DEFAULT '0.0'
                 )''')
    conn.commit()
    conn.close()

def filterBooks(arguments):
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    firstQuery = "SELECT id FROM books WHERE "
    secondQuery = "SELECT * FROM books WHERE "
    conditions = []
    columns = ['id', 'title', 'author', 'publisher', 'date_book', 'format', 'categories']
    for column in columns:
        conditions.append(f"{column} LIKE '%{arguments}%'")
    firstQuery += " OR ".join(conditions)
    secondQuery += " OR ".join(conditions)
    cursor.execute(firstQuery)
    books = cursor.fetchall()
    cursor.execute(secondQuery)
    books_fetch = cursor.fetchall()
    return books_fetch, books[-1][0] if books else None


def getBook(book, cursor):
    cursor.execute(f"SELECT * FROM books WHERE id= '{book}'")
    metadata = cursor.fetchone()
    conn.close()
    return metadata


def getBooks():
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
        booksFetch = cursor.fetchall()
        conn.close()
        return booksFetch


def updateBooks(metadata, path):
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title=?, author=?, publisher=?, description=?, date_book=?, language_book=?, " +
                   "text=?, categories=? WHERE path=?",
              (metadata['title'], (metadata['author']), metadata['publisher'],
               metadata['description'], metadata['date_book'], metadata['language_book'],
               metadata['text'], metadata['categories'], path))
    conn.commit()
    conn.close()

def updateField(bookPath, fieldName, text):
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    query = f"UPDATE books SET {fieldName}=? WHERE path=?"
    cursor.execute(query, (text, bookPath))
    conn.commit()


def addBook(metadata):
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE path=?", (metadata['path'],))
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


def searchBook(query):
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
            date = book.get('publishedDate', 'Нет данных')
            publisher = book.get('publisher', 'Нет данных')
            language = book.get('language', 'Нет данных')
            text = book.get('text', 'Нет данных')
            categories = book.get('categories', 'Нет данных')
            book_info = {
                'title': title,
                'author': str(author).strip("[]'"),
                'publisher': publisher,
                'description': description,
                'date_book': date,
                'language_book': language,
                'text': text,
                'categories':str(categories).strip("[]'"),
            }
            return book_info
        else:
            print('По заданному запросу ничего не удалось найти!')
            return None
    except requests.exceptions.RequestException as e:
        print('Ошибка при выполнении запроса:', e)
        return None


def extractMetadata(file):
    book = readBook(file)
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
    searchBook('Метро книга')
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
                createTable()
                metadata = extractMetadata(selectedFile)
                if (isinstance(metadata, str)):
                    print(metadata)
                    continue
                addBook(metadata)
            elif secondChoice == '2':
                createTable()
                newBook = searchBook(input('Введите название книги ') + 'книга')
                addBook(newBook)

        elif choice == '2':
            getBooks()
        elif choice == '3':
            cursor.execute('''DROP TABLE IF EXISTS books''')
            print("Книги удалены!")
        elif choice == '4':
            break
        elif choice == '5':
            book_id = input('Введите ид книги: ')
            field_name = input('Введите имя поля книги: ')
            text = input('Введите текст : ')
            updateField(book_id, field_name, text)
    else:
        print('Некорректный выбор. Попробуйте снова!')
