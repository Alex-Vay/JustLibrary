import customtkinter as tk
my_w = tk.CTk()
my_w.geometry("300x120")  # Size of the window
my_w.title("www.plus2net.com")  # Adding a title

l3 = tk.CTkLabel(my_w,  text='Select One', width=15 )
l3.grid(row=2,column=1)

my_list = ["PHP","MySQL","Python","HTML"]
options = tk.StringVar(my_w)
options.set(my_list[1]) # default value

om1 =tk.CTkOptionMenu(my_w, variable=options, values=my_list)
om1.grid(row=2,column=2)

str_out=tk.StringVar(my_w)
str_out.set("Output")

l2 = tk.CTkLabel(my_w,  textvariable=str_out, width=10 )
l2.grid(row=2,column=4)

lab = customtkinter.CTkLabel(window, textvariable=str_out)
lab.place(x=400, y=400)
def my_show(*args):
    str_out.set(options.get())

options.trace('w',my_show)
my_w.mainloop()  # Keep the window open