import time
import os

try:
    with open("statistic.txt", "r") as file:
        total_time, word_counter = file.read().split('\t')
        word_counter = word_counter/60*total_time
except:
    word_counter = 0
    total_time = 0
is_reading_window = False
start_time = None
end_time = None
reading_speed = word_counter/total_time*60

def start_statistics():
    global is_reading_window, start_time
    is_reading_window = True
    start_time = time.time()
    #Пока не совсем понимаю как будет считываться текст в приложении
    #word_counter += ???
    # reading_speed = word_counter / total_time * 60

def stop_statistics():
    global is_reading_window, end_time, total_time
    if is_reading_window:
        is_reading_window = False
        end_time = time.time()
        total_time += end_time - start_time
        # reading_speed = word_counter / total_time * 60

def clear_statistics():
    total_time = 0
    word_counter = 0
    reading_speed = word_counter / total_time * 60
    try: os.remove("statistic.txt")
    except: pass

def updat_time():
    label.config(text=f"Время чтения {total_time}   Скорость чтения {reading_speed} слов в минуту")
    root.after(100, updat_time)

def save_data_on_exit():
    global total_time
    with open("statistic.txt", "w") as file:
        file.write(f"Время чтения {total_time}   Скорость чтения {reading_speed} слов в минуту")
