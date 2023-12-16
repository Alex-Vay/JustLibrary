import customtkinter
from PIL import ImageTk, Image
from customtkinter import CTk
from main import create_table, extract_metadata, add_book, update_field
from tkinter import filedialog
import sqlite3
import io
from statistics import start_timer, stop_timer, get_statistics, clear_statistics

window = CTk()
# window.overrideredirect(1) #убирает возможность закрыть/свернуть/ужать приложение
#window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))
window.geometry("{0}x{1}+0+0".format(1920, 1080))

FONTCOF = 18 / 26
SPACECOF = 42 / 26
TEXTSIZE = 36
bookID = -1
#line = round(1020 / (TEXTSIZE * (FONTCOF + SPACECOF) - FONTCOF * TEXTSIZE * 0.9))

index = customtkinter.CTkFrame(window, fg_color="#99621E")
myLibrary = customtkinter.CTkFrame(window, fg_color="#99621E")
reader = customtkinter.CTkFrame(window, fg_color="#99621E")
navigation = customtkinter.CTkFrame(window, fg_color="#B8860B")
frames = [index, myLibrary, reader]
navigation.place(x=0, y=0, relheight=1)

search = ImageTk.PhotoImage(file="img/search.png")
robot = ImageTk.PhotoImage(file="img/robot.png")
logo = ImageTk.PhotoImage(file="img/logo.png")
isReaderOpen = False


def show_frame(frame):
    global start_index, end_index
    for i in frames:
        if frame is not reader:
            #start_index = readerTextBox.index("@0,0")
            end_index = readerTextBox.index(f"@1920,1080")
            try:
                update_field(bookID[0], "last_fragment", end_index)
            except: pass
            check_open_reader()
        if frame is index:
            statisticsLabel.configure(text=get_statistics())
        if frame is not i:
            i.pack_forget()
    frame.pack(expand=True, fill="both")


def get_cover(book_id):
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    cursor.execute("SELECT cover FROM books WHERE id=?", (book_id,))
    cover_data = cursor.fetchone()[0]
    conn.close()
    return cover_data


def get_books_id():
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
        conn.close()
        return books_fetch, books[-1][0] if books else None


def click_to_add_book():
    global bookID
    selectedFile = filedialog.askopenfilename()
    create_table()
    metadata = extract_metadata(selectedFile)
    if isinstance(metadata, str):
        return metadata
    add_book(metadata)
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM books WHERE path= '{metadata['path']}'")
    result = cursor.fetchone()
    bookID = result
    readerTextBox.configure(state="normal")
    readerTextBox.delete("0.0", "end")
    readerTextBox.insert("0.0", metadata['text'])
    readerTextBox.configure(state="disabled")
    show_frame(reader)

    books_fetch, _ = get_books_id()

    for i, book in enumerate(books_fetch):
        cover_data = get_cover(book[0])
        image = Image.open(io.BytesIO(cover_data))
        resized_image = image.resize((150, 200))
        cover_image = ImageTk.PhotoImage(resized_image)

        num_books_in_row = i % 5
        x = 250 + num_books_in_row * 250
        y = 200 + (i // 5) * 200

        new_btn = customtkinter.CTkButton(myLibrary, image=cover_image,
                                          text="",
                                          fg_color="#99621E",
                                          hover_color="#F0E68C",
                                          border_width=3,
                                          border_color="black",
                                          corner_radius=10)
        new_btn.place(x=x, y=y)


def display_books_on_startup():
    create_table()
    books_fetch, latest_book_id = get_books_id()

    if not books_fetch:
        print("No books added yet")
        show_frame(index)
    else:
        for i, book in enumerate(books_fetch):
            cover_data = get_cover(book[0])
            if cover_data:
                image = Image.open(io.BytesIO(cover_data))
                resized_image = image.resize((150, 200))
                cover_image = ImageTk.PhotoImage(resized_image)

                num_books_in_row = i % 5
                x = 250 + num_books_in_row * 250
                y = 200 + (i // 5) * 200

                new_btn = customtkinter.CTkButton(myLibrary, image=cover_image,
                                                  text="",
                                                  fg_color="#99621E",
                                                  hover_color="#F0E68C",
                                                  border_width=3,
                                                  border_color="black",
                                                  corner_radius=10)
                new_btn.image = cover_image
                new_btn.place(x=x, y=y)


def clear():
    global start_index, end_index
    clear_statistics()
    start_index = '1.0'
    end_index = 0


def exit_app():
    window.quit()


def clear_entryVirtualAssistant(event):
    entryVirtualAssistant.delete(0, customtkinter.END)


def clear_entryMyLibrary(event):
    entryMyLibrary.delete(0, customtkinter.END)


labelIndex = customtkinter.CTkLabel(index, text="Главная", text_color="#BDB76B")
labelIndex.configure(font=("Verdana", 64, "bold"))
labelIndex.place(x=600, y=10)

labelLogo = customtkinter.CTkLabel(index, image=logo, text="")
labelLogo.place(x=1300, y=10)

recentlyOpened = customtkinter.CTkLabel(index, text="Недавно открытые:", text_color="#BDB76B")
recentlyOpened.configure(font=("Verdana", 50, "bold"))
recentlyOpened.place(x=210, y=250)

entryVirtualAssistant = customtkinter.CTkEntry(index, justify='center')
entryVirtualAssistant.configure(font=("Verdana", 22, "bold"), width=420, height=60,
                                border_width=3,
                                corner_radius=10,
                                border_color="black",
                                fg_color="#B8860B")
entryVirtualAssistant.insert(5, "Введите запрос...")
entryVirtualAssistant.bind("<Button-1>", clear_entryVirtualAssistant)
entryVirtualAssistant.place(x=400, y=100)

btnIndex = customtkinter.CTkButton(index, text="Виртуальный\n помощник", compound="right", image=robot)
btnIndex.configure(font=("Verdana", 16, "bold"), width=90,
                   text_color="#99621E",
                   fg_color="#B8860B",
                   border_width=3,
                   border_color="black",
                   corner_radius=10,
                   hover_color="#F0E68C")
btnIndex.place(x=830, y=100)

statisticsLabel = customtkinter.CTkButton(index, text=get_statistics(), command=clear)
statisticsLabel.configure(font=("Verdana", 24, "bold"))
statisticsLabel.place(x=800, y=770)

entryMyLibrary = customtkinter.CTkEntry(myLibrary, justify='center')
entryMyLibrary.configure(font=("Verdana", 18, "bold"), width=500, height=35,
                         border_width=3,
                         corner_radius=10,
                         border_color="black",
                         fg_color="#B8860B")
entryMyLibrary.insert(5, "Искать здесь...")
entryMyLibrary.bind("<Button-1>", clear_entryMyLibrary)
entryMyLibrary.place(x=470, y=100)

btnMyLibrary = customtkinter.CTkButton(myLibrary, text="Искать", image=search, compound="left")
btnMyLibrary.configure(font=("Verdana", 16, "bold"), width=90, height=35,
                       text_color="#99621E",
                       fg_color="#B8860B",
                       border_width=3,
                       border_color="black",
                       corner_radius=10,
                       hover_color="#F0E68C")
btnMyLibrary.place(x=980, y=100)

labelMyLibrary = customtkinter.CTkLabel(myLibrary, text="Моя библиотека", text_color="#BDB76B")
labelMyLibrary.configure(font=("Verdana", 64, "bold"))
labelMyLibrary.place(x=480, y=10)

readerTextBox = customtkinter.CTkTextbox(reader)
readerTextBox.place(x=200, y=0)
readerTextBox.configure(font=("Calibre", TEXTSIZE),
                        width=1720, height=1020,
                        wrap="word",
                        state="disabled")

btnMain = customtkinter.CTkButton(navigation, text="Главная", command=lambda: show_frame(index))
btnMain.configure(font=("Verdana", 32, "bold"), width=50,
                  fg_color="#99621E",
                  hover_color="#F0E68C",
                  text_color="#B8860B",
                  border_width=3,
                  border_color="black",
                  corner_radius=10)
btnMain.place(x=10, y=60)

btnLibrary = customtkinter.CTkButton(navigation, text="Моя\nбиблиотека", command=lambda: show_frame(myLibrary))
btnLibrary.configure(font=("Verdana", 22, "bold"), width=30,
                     fg_color="#99621E",
                     hover_color="#F0E68C",
                     text_color="#B8860B",
                     border_width=3,
                     border_color="black",
                     corner_radius=10)
btnLibrary.place(x=10, y=150)

btnReader = customtkinter.CTkButton(navigation, text="Читалка", command=lambda: show_frame(reader))
btnReader.configure(font=("Verdana", 32, "bold"), width=170, height=60,
                    fg_color="#99621E",
                    hover_color="#F0E68C",
                    text_color="#B8860B",
                    border_width=3,
                    border_color="black",
                    corner_radius=10)
btnReader.place(x=10, y=240)

btnAddBook = customtkinter.CTkButton(navigation, text="Добавить\nкнигу", command=click_to_add_book)
btnAddBook.configure(font=("Verdana", 22, "bold"), width=170,
                     fg_color="#99621E",
                     hover_color="#F0E68C",
                     text_color="#B8860B",
                     border_width=3,
                     border_color="black",
                     corner_radius=10)
btnAddBook.place(x=10, y=330)

btnExit = customtkinter.CTkButton(navigation, text="Выйти", command=exit_app)
btnExit.configure(font=("Verdana", 42, "bold"), width=160,
                  fg_color="#FF7F50",
                  hover_color="#FF4500",
                  text_color="#DC143C",
                  border_width=5,
                  border_color="black",
                  corner_radius=10)
btnExit.place(x=10, y=780)

start_index = '1.0'
end_index = 0


def check_open_reader():
    global isReaderOpen, start_index, end_index
    if reader.winfo_ismapped() and not isReaderOpen:
        start_timer()
        isReaderOpen = True
    else:
        if not reader.winfo_ismapped() and isReaderOpen:
            isReaderOpen = False
            #visible_text = readerTextBox.get(start_index, end_index)
            visible_text = readerTextBox.get(start_index, end_index)
            start_index = end_index
            print("-"*20)
            stop_timer(visible_text)
    window.after(1000, check_open_reader)


display_books_on_startup()
show_frame(index)
window.mainloop()
