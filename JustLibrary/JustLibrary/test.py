from tkinter import *
import customtkinter

window = customtkinter.CTk()
myLibrary = customtkinter.CTkFrame(window, fg_color="#99621E")

myLibrary.pack(fill='both', expand=True)

# Создаем виджет прокрутки
scrollbar = customtkinter.CTkScrollbar(myLibrary)
scrollbar.pack(side=RIGHT, fill=Y)

# Создаем холст (Canvas) для фрейма с книгами
canvas = Canvas(myLibrary, yscrollcommand=scrollbar.set)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

# Привязываем виджет прокрутки к холсту
scrollbar.configure(command=canvas.yview)

# Создаем фрейм для книг на холсте
books_frame = customtkinter.CTkFrame(canvas, fg_color="#99621E")
canvas.create_window((0, 0), window=books_frame, anchor='nw')

# Добавляем книги на фрейм
for i in range(100):
    # Создаем кнопку для каждой книги
    btn = customtkinter.CTkButton(books_frame, text=f"Книга {i+1}")
    btn.pack(side='top', anchor='w')

# Настраиваем прокрутку холста
books_frame.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

window.mainloop()
