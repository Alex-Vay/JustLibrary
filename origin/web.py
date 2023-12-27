import os
import threading
import customtkinter
from PIL import ImageTk, Image
from customtkinter import CTk
from main import createTable, extractMetadata, addBook, updateField, filterBooks
from tkinter import filedialog, colorchooser
import sqlite3
import io
from statistics import startTimer, stopTimer, getStatistics, cleanStatistics
from virtual_assistant.chatgpt_functions import getResponse, getSimilarBooks, getBookInfo, getBookAnalogies, explainTerm, retellText


def getReaderSettings():
    try:
        with open("readerSettings.txt", "r") as f:
            settings = f.read().split()
        for i in range(len(settings)):
            try:
                settings[i] = int(settings[i])
            except: pass
        return settings
    except: return [36, 10, "#000000", "#FFFFFF"]


window = CTk()
# window.overrideredirect(1) #убирает возможность закрыть/свернуть/ужать приложение
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))

FONTCOF = 18 / 26
SPACECOF = 42 / 26
TEXTSIZE, TEXTSPACING, TEXTCOLOR, READERCOLOR = getReaderSettings()
CHANGEVALUE = 2
bookPath = ''
currentBook = ''
currentText = ''

index = customtkinter.CTkFrame(window, fg_color="#99621E")
myLibrary = customtkinter.CTkFrame(window, fg_color="#99621E")
reader = customtkinter.CTkFrame(window, fg_color="#99621E")
navigation = customtkinter.CTkFrame(window, fg_color="#B8860B")
frames = [index, myLibrary, reader]
navigation.place(x=0, y=0, relheight=1)

search = ImageTk.PhotoImage(file="img/search.png")
robot = ImageTk.PhotoImage(file="img/robot.png")
logo = ImageTk.PhotoImage(file="img/logo.png")
delete = ImageTk.PhotoImage(file="img/delete.jpg")
isReaderOpen = False


def showFrame(frame):
    global startIndex, endIndex, bookPath
    for i in frames:
        if frame is not reader:
            endIndex = readerTextBox.index(f"@1920,1080")
            try: updateField(bookPath, "last_fragment", endIndex)
            except: pass
            checkOpenReader()
        if frame is index:
            statisticsLabel.configure(text=getStatistics())
        if frame is not i:
            i.pack_forget()
    frame.pack(expand=True, fill="both")


def getBookText(bookId):
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    cursor.execute("SELECT text FROM books WHERE id=?", (bookId,))
    book_text = cursor.fetchone()[0]
    conn.close()
    return book_text


def openBookText(bookId):
    global bookPath
    book_text = getBookText(bookId)
    readerTextBox.configure(state="normal")
    readerTextBox.delete("0.0", "end")
    readerTextBox.insert("0.0", book_text)
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    cursor.execute("SELECT path FROM books WHERE id=?", (bookId,))
    bookPath = cursor.fetchone()[0]
    readerTextBox.see(currentBookLastFragment(bookPath))
    readerTextBox.configure(state="disabled")
    showFrame(reader)


def getBooksId(arguments=None):
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books'")
    result = cursor.fetchone()
    if result is None: return
    else:
        if (arguments is None):
            cursor.execute("SELECT id FROM books")
            books = cursor.fetchall()
            cursor.execute("SELECT * FROM books")
            booksFetch = cursor.fetchall()
            conn.close()
            return booksFetch, books[-1][0] if books else None
        else:
            booksFetch, books = filterBooks(arguments)
            return booksFetch, books if books else None


def currentBookLastFragment(path):
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT last_fragment FROM books WHERE path= '{path}'")
    return cursor.fetchone()[0]


def checkBook(path):
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM books WHERE path= '{path}'")
    return cursor.fetchone()


def clickToAddBook():
    global bookPath
    myLibrary.nothingWasFound.destroy()
    selectedFile = filedialog.askopenfilename()
    createTable()
    if checkBook(selectedFile):
        bookPath = selectedFile
        conn = sqlite3.connect('metadata.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT text FROM books WHERE path= '{bookPath}'")
        text = cursor.fetchone()[0]
    else:
        metadata = extractMetadata(selectedFile)
        if isinstance(metadata, str):
            return metadata
        text = metadata['text']
        if len(text) > 25000:
            addBook(metadata)
        bookPath = metadata["path"]
    readerTextBox.configure(state="normal")
    readerTextBox.delete("0.0", "end")
    readerTextBox.insert("0.0", text)
    try:
        readerTextBox.see(currentBookLastFragment(bookPath))
    except: pass
    readerTextBox.configure(state="disabled")
    showFrame(reader)
    displayBooks()


def getCover(bookId):
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    cursor.execute("SELECT cover FROM books WHERE id=?", (bookId,))
    cover_data = cursor.fetchone()[0]
    if cover_data is not None:
        return cover_data
    else:
        cursor.execute("SELECT path FROM books WHERE id=?", (bookId,))
        fileName = cursor.fetchone()[0].split('/')[-1]
        return fileName


libraryOptions = ["Опции", "Удалить книгу", "Найти похожие", "Информация", "По мотивам книги", "Изменить поля"]
currentOption = customtkinter.StringVar(window)
currentOption.set(libraryOptions[0])
menu = customtkinter.CTkOptionMenu(window, variable=currentOption, values=libraryOptions)

def showMenu(book, x, y):
    currentOption = customtkinter.StringVar(window)
    currentOption.set(libraryOptions[0])
    menu.configure(variable=currentOption)
    currentOption.trace('w', lambda *args: myShow(book, currentOption))
    menu.place(x=x, y=y)


def hideMenu():
    menu.place(x=-1000, y=-1000)


def myShow(*args):
    global currentBook
    currentOption = args[1]
    action = currentOption.get()
    currentBook = args[0]
    match action[0]:
        case "Н": startAnswer(similarBookResponse)
        case "И": startAnswer(bookInfoResponse)
        case "П": startAnswer(bookAnalogiesResponse)


def similarBookResponse():
    global currentBook
    response = getSimilarBooks(currentBook[1])
    additionalFrame = openAdditionalFrame(response)
    additionalFrame.focus()


def bookInfoResponse():
    global currentBook
    response = getBookInfo(currentBook[1])
    additionalFrame = openAdditionalFrame(response)
    additionalFrame.focus()


def bookAnalogiesResponse():
    global currentBook
    response = getBookAnalogies(currentBook[1])
    additionalFrame = openAdditionalFrame(response)
    additionalFrame.focus()


def processText():
    global currentText
    try:
        text = readerTextBox.get("sel.first", "sel.last")
        currentText = text
        if len(text.split()) > 4:
            startAnswer(retellTextResponse)
        else:
            startAnswer(explainTermResponse)
    except: pass


def retellTextResponse():
    global currentText
    response = retellText(currentText)
    additionalFrame = openAdditionalFrame(response)
    additionalFrame.focus()


def explainTermResponse():
    global currentText
    response = explainTerm(currentText)
    additionalFrame = openAdditionalFrame(response)
    additionalFrame.focus()


def parseTitle(title):
    parsedTitle = ''
    for i, symbol in enumerate(title):
        if i % 20 == 0:
            parsedTitle+="\n"
        parsedTitle+=symbol
    return parsedTitle


def createBoxForBook(i, coverData, frame, y1, book):
    newBtn = customtkinter.CTkButton(frame)
    try:
        image = Image.open(io.BytesIO(coverData))
        resizedImage = image.resize((150, 200))
        coverImage = ImageTk.PhotoImage(resizedImage)
        newBtn.configure(image=coverImage, text='')
    except:
        newBtn.configure(text=parseTitle(coverData), width=150, height=200)
    newBtn.configure(fg_color="#99621E",
                     hover_color="#F0E68C",
                     border_width=3,
                     border_color="black",
                     corner_radius=10)
    numBooksInRow = i % 5
    x = 250 + numBooksInRow * 250
    y = y1 if y1 == 350 else 200 + (i // 5) * 200
    newBtn.bind("<Button-1>", lambda event: openBookText(book[0]))
    newBtn.bind("<Button-3>", lambda event: showMenu(book, x, y))
    newBtn.bind("<Double-Button-3>", lambda event: hideMenu())
    newBtn.place(x=x, y=y)



def addCategoryForBook(bookPath):
    query = entryMyLibrary.get()
    updateField(bookPath, 'categories', query)


def displayBooks(query=None):
    createNothingWasFound()
    createTable()
    booksFetch, latestBookId = getBooksId(query)
    children = myLibrary.winfo_children()
    libraryBooks = len([child for child in children if isinstance(child, customtkinter.CTkButton)])
    if not booksFetch:
        print("No books added yet")
    else:
        myLibrary.nothingWasFound.destroy()
        for i, book in enumerate(booksFetch):
            bookPath = booksFetch[i][13]
            coverData = getCover(book[0])
            if i + 2 >= libraryBooks:
                createBoxForBook(i, coverData, myLibrary, 200, booksFetch[i])
        clearAllBooksMainPage()
        for i, book in enumerate(booksFetch[-5:], start=0):
            bookPath = booksFetch[i][13]
            coverData = getCover(book[0])
            createBoxForBook(i, coverData, index, 350, booksFetch[i])


def clearAllBooksMainPage():
    for book in index.winfo_children():
        if isinstance(book, customtkinter.CTkButton) and book != index.btnIndex and book != index.statisticsLabel:
            book.destroy()


def ClickToFindBooks():
    clearAllWidgetsBooks()
    myLibrary.nothingWasFound.destroy()
    query = entryMyLibrary.get()
    displayBooks(query)

def clearAllWidgetsBooks():
    for book in myLibrary.winfo_children():
        if isinstance(book, customtkinter.CTkButton) and book != myLibrary.btnMyLibrary and book != myLibrary.btnDelete:
            book.destroy()


def deleteBooks():
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS books''')
    conn.close()
    clearAllWidgetsBooks()
    createNothingWasFound()


def checkSize(size, num):
    return True if (size + num >= 0) else False


def changeFont(num):
    global TEXTSIZE
    if not(checkSize(TEXTSIZE, num)): return
    TEXTSIZE += num
    readerTextBox.configure(font=("Calibre", TEXTSIZE))


def changeTextSpacing(num):
    global TEXTSPACING
    if not (checkSize(TEXTSPACING, num)): return
    TEXTSPACING += num
    readerTextBox.configure(spacing3=TEXTSPACING)


def saveReaderSettings():
    with open("readerSettings.txt", "w") as f:
        f.write(f"{TEXTSIZE} {TEXTSPACING} {TEXTCOLOR} {READERCOLOR}")


def changeColor(item):
    global TEXTCOLOR, READERCOLOR
    color = colorchooser.askcolor()[1]
    match(item):
        case "text":
            TEXTCOLOR = color
            readerTextBox.configure(text_color=TEXTCOLOR)
        case "reader":
            READERCOLOR = color
            readerTextBox.configure(fg_color=READERCOLOR)


def clean():
    global startIndex, endIndex
    cleanStatistics()
    startIndex = '1.0'
    endIndex = 0

def cleanReaderSettings():
    try:
        os.remove("readerSettings.txt")
    except:
        pass
    TEXTSIZE, TEXTSPACING, TEXTCOLOR, READERCOLOR = getReaderSettings()
    readerTextBox.configure(font=("Calibre", TEXTSIZE), text_color=TEXTCOLOR,
                            fg_color=READERCOLOR, spacing3=TEXTSPACING)


def exitApp():
    saveReaderSettings()
    window.quit()


def clearEntryVirtualAssistant(event):
    entryVirtualAssistant.delete(0, customtkinter.END)


def clearEntryMyLibrary(event):
    entryMyLibrary.delete(0, customtkinter.END)


isDarkMode = False
def click_to_toggle_mode():
    global isDarkMode
    isDarkMode = not isDarkMode
    if isDarkMode:
        btnAddBook.configure(fg_color="black", text_color="#808080", hover_color="#696969")
        btnReader.configure(fg_color="black", text_color="#808080", hover_color="#696969")
        btnLibrary.configure(fg_color="black", text_color="#808080", hover_color="#696969")
        btnMain.configure(fg_color="black", text_color="#808080", hover_color="#696969")
        btnMode.configure(fg_color="black", text_color="#808080", hover_color="#696969")
        navigation.configure(fg_color="#778899")
        index.configure(fg_color="#A9A9A9")
        myLibrary.configure(fg_color="#A9A9A9")
        labelIndex.configure(text_color="#696969")
        recentlyOpened.configure(text_color="#696969")
        labelMyLibrary.configure(text_color="#696969")
        entryVirtualAssistant.configure(fg_color="#2F4F4F")
        btnIndex.configure(fg_color="black", text_color="#808080", hover_color="#696969")
        btnMyLibrary.configure(fg_color="black", text_color="#808080", hover_color="#696969")
        entryMyLibrary.configure(fg_color="#2F4F4F")
        btnExit.configure(fg_color="black", text_color="#808080", hover_color="#696969")
    else:
        btnAddBook.configure(fg_color="#99621E", hover_color="#F0E68C", text_color="#B8860B", border_width=3, border_color="black", corner_radius=10)
        btnReader.configure(fg_color="#99621E",hover_color="#F0E68C",text_color="#B8860B",border_width=3,border_color="black",corner_radius=10)
        btnLibrary.configure(fg_color="#99621E", hover_color="#F0E68C", text_color="#B8860B", border_width=3, border_color="black", corner_radius=10)
        btnMain.configure(fg_color="#99621E", hover_color="#F0E68C", text_color="#B8860B", border_width=3, border_color="black", corner_radius=10)
        btnMode.configure(fg_color="#99621E", hover_color="#F0E68C", text_color="#B8860B", border_width=3, border_color="black", corner_radius=10)
        navigation.configure(fg_color="#B8860B")
        index.configure(fg_color="#99621E")
        myLibrary.configure(fg_color="#99621E")
        labelIndex.configure(text_color="#BDB76B")
        recentlyOpened.configure(text_color="#BDB76B")
        labelMyLibrary.configure(text_color="#BDB76B")
        btnExit.configure(font=("Verdana", 42, "bold"), width=160,fg_color="#FF7F50",hover_color="#FF4500",text_color="#DC143C",border_width=5,border_color="black",corner_radius=10)
        entryVirtualAssistant.configure(font=("Verdana", 22, "bold"), width=420, height=60,border_width=3,corner_radius=10,border_color="black",fg_color="#B8860B")
        btnIndex.configure(fg_color="#B8860B", hover_color="#F0E68C", text_color="#99621E", border_width=3, border_color="black", corner_radius=10)
        btnMyLibrary.configure(font=("Verdana", 16, "bold"), width=90, height=35,text_color="#99621E",fg_color="#B8860B",border_width=3,border_color="black",corner_radius=10,hover_color="#F0E68C")
        entryMyLibrary.configure(font=("Verdana", 18, "bold"), width=500, height=35,border_width=3,corner_radius=10,border_color="black",fg_color="#B8860B")


def startAnswer(question):
    thread = threading.Thread(target=question)
    thread.start()


def mainResponse():
    message = entryVirtualAssistant.get()
    response = getResponse(message)
    additionalFrame = openAdditionalFrame(response)
    additionalFrame.focus()


def openAdditionalFrame(text):
    additionalFrame = customtkinter.CTkToplevel(window)
    additionalFrame.geometry("700x400+600+300")
    textBox = customtkinter.CTkTextbox(additionalFrame)
    textBox.configure(font=("Calibre", TEXTSIZE),
                      width=700, height=400,
                      wrap="word", state="normal",
                      spacing3=TEXTSPACING,
                      text_color=TEXTCOLOR, fg_color=READERCOLOR)
    textBox.insert('0.0', text)
    textBox.configure(state="disabled")
    textBox.place(x=0, y=0)
    return additionalFrame



def createNothingWasFound():
    nothingWasFound = customtkinter.CTkLabel(myLibrary, text="Ничего не найдено", text_color="#BDB76B")
    myLibrary.nothingWasFound = nothingWasFound
    nothingWasFound.configure(font=("Verdana", 40, "bold"))
    nothingWasFound.place(x=600, y=350)


labelIndex = customtkinter.CTkLabel(index, text="Главная", text_color="#BDB76B")
labelIndex.configure(font=("Verdana", 64, "bold"))
labelIndex.place(x=600, y=10)

labelLogo = customtkinter.CTkLabel(index, image=logo, text="")
labelLogo.place(x=1300, y=10)

recentlyOpened = customtkinter.CTkLabel(index, text="Недавно добавленные:", text_color="#BDB76B")
recentlyOpened.configure(font=("Verdana", 50, "bold"))
recentlyOpened.place(x=210, y=250)

entryVirtualAssistant = customtkinter.CTkEntry(index, justify='center')
entryVirtualAssistant.configure(font=("Verdana", 22, "bold"), width=420, height=60,
                                border_width=3,
                                corner_radius=10,
                                border_color="black",
                                fg_color="#B8860B")
entryVirtualAssistant.insert(5, "Введите запрос...")
entryVirtualAssistant.bind("<Button-1>", clearEntryVirtualAssistant)
entryVirtualAssistant.place(x=400, y=100)

btnIndex = customtkinter.CTkButton(index, text="Виртуальный\n помощник", command=lambda: startAnswer(mainResponse),
                                   compound="right", image=robot)
btnIndex.configure(font=("Verdana", 16, "bold"), width=90,
                   text_color="#99621E",
                   fg_color="#B8860B",
                   border_width=3,
                   border_color="black",
                   corner_radius=10,
                   hover_color="#F0E68C")
index.btnIndex = btnIndex
btnIndex.place(x=830, y=100)

statisticsLabel = customtkinter.CTkButton(index, text=getStatistics(), command=clean)
statisticsLabel.configure(font=("Verdana", 24, "bold"))
index.statisticsLabel = statisticsLabel
statisticsLabel.place(x=800, y=770)

entryMyLibrary = customtkinter.CTkEntry(myLibrary, justify='center')
entryMyLibrary.configure(font=("Verdana", 18, "bold"), width=500, height=35,
                         border_width=3,
                         corner_radius=10,
                         border_color="black",
                         fg_color="#B8860B")

entryMyLibrary.insert(5, "Введите")
entryMyLibrary.bind("<Button-1>", clearEntryMyLibrary)
entryMyLibrary.place(x=470, y=100)


btnMyLibrary = customtkinter.CTkButton(myLibrary, text="Искать", command=ClickToFindBooks, image=search, compound="left")
myLibrary.btnMyLibrary = btnMyLibrary
btnMyLibrary.configure(font=("Verdana", 16, "bold"), width=90, height=35,
                       text_color="#99621E",
                       fg_color="#B8860B",
                       border_width=3,
                       border_color="black",
                       corner_radius=10,
                       hover_color="#F0E68C")
btnMyLibrary.place(x=980, y=100)

btnDelete = customtkinter.CTkButton(myLibrary, text="Удалить книги", command=deleteBooks)
myLibrary.btnDelete = btnDelete
btnDelete.configure(font=("Verdana", 16, "bold"), width=90, height=35,
                       text_color="#99621E",
                       fg_color="#B8860B",
                       border_width=3,
                       border_color="black",
                       corner_radius=10,
                       hover_color="#F0E68C")
btnDelete.place(x=1115, y=100)


labelMyLibrary = customtkinter.CTkLabel(myLibrary, text="Моя библиотека", text_color="#BDB76B")
labelMyLibrary.configure(font=("Verdana", 64, "bold"))
labelMyLibrary.place(x=480, y=10)


readerTextBox = customtkinter.CTkTextbox(reader)
readerTextBox.place(x=200, y=50)
readerTextBox.configure(font=("Calibre", TEXTSIZE),
                        width=1720, height=960,
                        wrap="word", state="disabled",
                        spacing3=TEXTSPACING,
                        text_color=TEXTCOLOR, fg_color=READERCOLOR)
readerTextBox.bind("<Button-3>", lambda event: processText())

readerFontIncrease = customtkinter.CTkButton(reader, text="Тт+", command=lambda: changeFont(CHANGEVALUE))
readerFontIncrease.place(x=200, y=0)
readerFontIncrease.configure(font=("Calibre", 24), width=45)

readerFontReduce = customtkinter.CTkButton(reader, text="Тт-", command=lambda: changeFont(-CHANGEVALUE))
readerFontReduce.place(x=260, y=0)
readerFontReduce.configure(font=("Calibre", 24), width=45)

readerSpaceIncrease = customtkinter.CTkButton(reader, text="A+", command=lambda: changeTextSpacing(CHANGEVALUE))
readerSpaceIncrease.place(x=320, y=0)
readerSpaceIncrease.configure(font=("Calibre", 24), width=45)

readerSpaceReduce = customtkinter.CTkButton(reader, text="A-", command=lambda: changeTextSpacing(-CHANGEVALUE))
readerSpaceReduce.place(x=380, y=0)
readerSpaceReduce.configure(font=("Calibre", 24), width=45)

readerTextColor = customtkinter.CTkButton(reader, text="Цвет текста", command=lambda: changeColor("text"))
readerTextColor.place(x=440, y=0)
readerTextColor.configure(font=("Calibre", 24), width=140)

readerReaderColor = customtkinter.CTkButton(reader, text="Цвет фона", command=lambda: changeColor("reader"))
readerReaderColor.place(x=600, y=0)
readerReaderColor.configure(font=("Calibre", 24), width=100)

readerReaderClean = customtkinter.CTkButton(reader, text="Очистить настройки", command=cleanReaderSettings)
readerReaderClean.place(x=1600, y=0)
readerReaderClean.configure(font=("Calibre", 24), width=100)

btnMain = customtkinter.CTkButton(navigation, text="Главная", command=lambda: showFrame(index))
btnMain.configure(font=("Verdana", 32, "bold"), width=50,
                  fg_color="#99621E",
                  hover_color="#F0E68C",
                  text_color="#B8860B",
                  border_width=3,
                  border_color="black",
                  corner_radius=10)
btnMain.place(x=10, y=60)

btnLibrary = customtkinter.CTkButton(navigation, text="Моя\nбиблиотека", command=lambda: showFrame(myLibrary))
btnLibrary.configure(font=("Verdana", 22, "bold"), width=30,
                     fg_color="#99621E",
                     hover_color="#F0E68C",
                     text_color="#B8860B",
                     border_width=3,
                     border_color="black",
                     corner_radius=10)
btnLibrary.place(x=10, y=150)

btnReader = customtkinter.CTkButton(navigation, text="Читалка", command=lambda: showFrame(reader))
btnReader.configure(font=("Verdana", 32, "bold"), width=170, height=60,
                    fg_color="#99621E",
                    hover_color="#F0E68C",
                    text_color="#B8860B",
                    border_width=3,
                    border_color="black",
                    corner_radius=10)
btnReader.place(x=10, y=240)

btnAddBook = customtkinter.CTkButton(navigation, text="Добавить\nкнигу", command=clickToAddBook)
btnAddBook.configure(font=("Verdana", 22, "bold"), width=170,
                     fg_color="#99621E",
                     hover_color="#F0E68C",
                     text_color="#B8860B",
                     border_width=3,
                     border_color="black",
                     corner_radius=10)
btnAddBook.place(x=10, y=330)

btnMode = customtkinter.CTkButton(navigation, text="Режимы", command=lambda: click_to_toggle_mode())
btnMode.configure(font=("Verdana", 32, "bold"), width=170, height=60,
                    fg_color="#99621E",
                    hover_color="#F0E68C",
                    text_color="#B8860B",
                    border_width=3,
                    border_color="black",
                    corner_radius=10)
btnMode.place(x=10, y=420)

btnExit = customtkinter.CTkButton(navigation, text="Выйти", command=exitApp)
btnExit.configure(font=("Verdana", 42, "bold"), width=160,
                  fg_color="#FF7F50",
                  hover_color="#FF4500",
                  text_color="#DC143C",
                  border_width=5,
                  border_color="black",
                  corner_radius=10)
btnExit.place(x=10, y=780)

startIndex = '1.0'
endIndex = 0


def checkOpenReader():
    global isReaderOpen, startIndex, endIndex
    if reader.winfo_ismapped() and not isReaderOpen:
        startTimer()
        isReaderOpen = True
    else:
        if not reader.winfo_ismapped() and isReaderOpen:
            isReaderOpen = False
            visible_text = readerTextBox.get(startIndex, endIndex)
            startIndex = endIndex
            print("-"*20)
            stopTimer(visible_text)
    window.after(1000, checkOpenReader)


displayBooks()
showFrame(index)
window.mainloop()