import sqlite3
import epub_meta
from tkinter import Tk, filedialog
import requests

root = Tk()

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
                 language_book TEXT DEFAULT 'Нет данных'
                 
                 )''')
    conn.commit()
    conn.close()


def get_books():
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books'")
    result = cursor.fetchone()
    if result is None:
        print("Книги еще не добавлены!")
    else:
        cursor.execute("SELECT * FROM books")
        metadata = cursor.fetchall()
        print(*metadata, sep = "\n")
        conn.close()


def update_books(metadata, book_id):
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title=?, author=?, publisher=?, description=?, subject=?, date_book=?, language_book=? WHERE id=?",
              (metadata['title'], (metadata['author']), metadata['publisher'],
               metadata['description'], metadata['date'], metadata['language']))
    conn.commit()
    conn.close()

def add_book(metadata):
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title = ? AND publisher=?", (metadata['title'], metadata['publisher']))
    isAlreadyExist = cursor.fetchone()
    answer = 'да'

    if isAlreadyExist:
        answer = input("Книга уже добавлена, хотете добавить её еще раз? (да / нет) ")
    if answer.lower()[0] == 'д':
        cursor.execute('''
            INSERT INTO books (title, author, publisher, description, date_book, language_book)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (metadata['title'], (metadata['author']), metadata['publisher'],
                   metadata['description'], metadata['date'], metadata['language']))
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
                'publisher': publisher,
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
    try:
        book = epub_meta.get_epub_metadata(file)
        metadata = {
            'title': str(book.title),
            'author': str(book.authors).strip("[]'"),
            'publisher': str(book.publisher),
            'description': str(book.description).replace('\xa0', ' '),
            'date' : book.date,
            'language': str(book.language),
            'toc' : str(book.toc),
        }
        return metadata
    except epub_meta.EpubParseError as e:
        print(f"Ошибка при извлечении метаданных: {e}")
        return None


while True:
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()

    print('-'*20)
    print('1. Добавить книгу')
    print('2. Показать все книги')
    print('3. Удалить все книги')
    print('4. Выйти')
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
else:
    print('Некорректный выбор. Попробуйте снова!')
