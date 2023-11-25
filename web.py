import tkinter as tk

def show_frame(frame):
    frame.tkraise()

window = tk.Tk()
window.title("Индивидуальная библиотека")
window.geometry("1920x1200")
window.overrideredirect(1)
window.state('zoomed')
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

index = tk.Frame(window)
myLibrary = tk.Frame(window)

for frame in (index, myLibrary):
    frame.grid(row=0, column=0, sticky='nsew')

entryMyLibrary = tk.Entry(myLibrary, width=50, justify='center', font="Verdana 10")
entryMyLibrary.place(x=505, y=100)

labelMyLibrary = tk.Label(myLibrary, text="Моя библиотека", font="Verdana 48")
labelMyLibrary.pack()

btnMyLibrary = tk.Button(myLibrary, text="Искать", font="Verdana 10", width=15)
btnMyLibrary.place(x=920, y=98)

btnMain = tk.Button(myLibrary, text="Главная", font="Verdana 16", width=15, command=lambda: show_frame(index))
btnMain.place(x=10, y=30)

btnLibrary = tk.Button(myLibrary, text="Моя библиотека", font="Verdana 16", width=15, command=lambda: show_frame(myLibrary))
btnLibrary.place(x=10, y=110)


entryVirtualAssistant = tk.Entry(index, borderwidth=0, justify='left', font="Verdana 14")
entryVirtualAssistant.place(x=370, y=100, height=40, width=400)

labelIndex = tk.Label(index, text="Главная", font="Verdana 48")
labelIndex.pack()

btnIndex = tk.Button(index, text="Виртуальный\n помощник", font="Verdana 10", width=15)
btnIndex.place(x=780, y=98)

btnMain = tk.Button(index, text="Главная", font="Verdana 16", width=15, command=lambda: show_frame(index))
btnMain.place(x=10, y=30)

btnLibrary = tk.Button(index, text="Моя библиотека", font="Verdana 16", width=15, command=lambda: show_frame(myLibrary))
btnLibrary.place(x=10, y=110)


show_frame(index)
window.mainloop()