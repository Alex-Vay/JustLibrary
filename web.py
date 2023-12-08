import customtkinter
from customtkinter import CTk
from PIL import ImageTk
from main import create_table, extract_metadata, add_book
from tkinter import filedialog

window = CTk()
#window.overrideredirect(1) убирает возможность закрыть/свернуть/ужать приложение
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))

index = customtkinter.CTkFrame(window, fg_color="#99621E")
myLibrary = customtkinter.CTkFrame(window, fg_color="#99621E")
navigation = customtkinter.CTkFrame(window, fg_color="#B8860B")
reader = customtkinter.CTkFrame(window, fg_color="#000000")
frames = [index, myLibrary, reader]
navigation.place(x=0, y=0, relheight=1)

search = ImageTk.PhotoImage(file="img/search.png")
robot = ImageTk.PhotoImage(file="img/robot.png")


def show_frame(frame):
    frame.pack(expand=True, fill="both")
    for i in frames:
        if frame is not i:
            print(i)
            i.pack_forget()


def click_to_add_book():
    #из-за ряда функций, которые ждут ответа от пользователя, может уйти в бесконечную загрузку
    print('Выберете файл')
    selectedFile = filedialog.askopenfilename()
    create_table()
    metadata = extract_metadata(selectedFile)
    if (isinstance(metadata, str)):
        print(metadata)
        return
    add_book(metadata)


def exit_app():
    window.quit()


def clear_entryVirtualAssistant(event):
    entryVirtualAssistant.delete(0, customtkinter.END)


def clear_entryMyLibrary(event):
    entryMyLibrary.delete(0, customtkinter.END)


labelIndex = customtkinter.CTkLabel(index, text="Главная", text_color="#BDB76B")
labelIndex.configure(font=("Verdana", 64, "bold"))
labelIndex.place(x=800, y = 10)

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



btn2Index = customtkinter.CTkButton(navigation, text="Добавить книгу", command=click_to_add_book)
btn2Index.configure(font=("Verdana", 16, "bold"), width=90,
                   text_color="#99621E",
                   fg_color="#B8860B",
                   border_width=3,
                   border_color="black",
                   corner_radius=10,
                   hover_color="#F0E68C")
btn2Index.place(x=830, y=400)



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
labelMyLibrary.place(x=700, y=10)

btnMain = customtkinter.CTkButton(navigation, text="Главная", command=lambda: show_frame(index))
btnMain.configure(font=("Verdana", 32, "bold"), width=50,
                  fg_color="#99621E",
                  hover_color="#F0E68C",
                  text_color="#B8860B",
                  border_width=3,
                  border_color="black",
                  corner_radius=10,)
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

btnExit = customtkinter.CTkButton(navigation, text="Выйти", command=exit_app)
btnExit.configure(font=("Verdana", 42, "bold"), width=160,
                     fg_color="#FF7F50",
                     hover_color="#FF4500",
                     text_color="#DC143C",
                     border_width=5,
                     border_color="black",
                     corner_radius=10)
btnExit.place(x=10, y=780)

show_frame(index)
window.mainloop()