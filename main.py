import sqlite3
import epub_meta
from tkinter import Tk, filedialog

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


def get_metadata():
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books'")
    result = cursor.fetchone()
    if result is None:
        print("Книги еще не добавлены")
    else:
        cursor.execute("SELECT * FROM books")
        metadata = cursor.fetchall()
        print(*metadata, sep = "\n")
        conn.close()


def update_metadata(metadata, book_id):
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
    cursor.execute('''
        INSERT INTO books (title, author, publisher, description, date_book, language_book)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (metadata['title'], (metadata['author']), metadata['publisher'],
               metadata['description'], metadata['date'], metadata['language']))
    conn.commit()



def extract_metadata(file):
    try:
        book = epub_meta.get_epub_metadata(file)
        metadata = {
            'title': str(book.title),
            'author': str(book.authors).strip("[]"),
            'publisher': str(book.publisher),
            'description': str(book.description).replace('\xa0', ' '),
            'date' : book.date,
            'language': str(book.language),
            'toc' : str(book.toc),
        }
        metadata['author'] = metadata['author'].strip("'")
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
    print(' ' * 20)
    choice = input('Выберите команду:')

    if choice == '1':
        print('1. Добавить файл')
        #print('2. Ввести данные самостоятельно')
        secondChoice = input('Выберите действие: ')
        if secondChoice == '1':
            print('Выберете файл')
            selectedFile = filedialog.askopenfilename()
            root.withdraw()
            create_table()  # Создаем таблицу в базе данных
            metadata = extract_metadata(selectedFile)

            cursor.execute("SELECT * FROM books WHERE title = ?", (metadata['title'],))
            isAlreadyExist = cursor.fetchone()


            if isAlreadyExist:
                print("Книга уже добавлена")
            else:
                print("Книга добавлена")
                add_book(metadata)
    elif choice == '2':
        get_metadata()
    elif choice == '3':
        cursor.execute('''DROP TABLE IF EXISTS books''')
        print("Книги удалены")
    elif choice == '4':
        break
else:
    print('Некорректный выбор. Попробуйте снова.')
