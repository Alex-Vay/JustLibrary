import time
import os
import re

words = 0
total_time = 0
start_time = 0


def get_statistics():
    global total_time, words
    try:
        with open("statistic.txt", "r") as file:
            statistics = file.read().split()
            total_time, words = float(statistics[0]), int(statistics[1])
            #word_counter = word_counter/60*total_time
    except:
        pass
    return f"Время чтения: {round(total_time/3600, 4)} часов   Скорость чтения: {int(0 if total_time == 0 else words/total_time*60)} слов в минуту"


def start_timer():
    global start_time
    start_time = time.time()
    print(start_time)


def stop_timer(text_path):
    global start_time, total_time, words
    end_time = time.time()
    print(start_time)
    print(end_time)
    total_time += end_time - start_time
    words += count_words(text_path)
    save_data_on_exit()


def clear_statistics():
    global total_time, words
    total_time = 0
    words = 0
    try:
        os.remove("statistic.txt")
    except:
        pass
    get_statistics()


def count_words(text_part):
    return len(text_part.split())


def save_data_on_exit():
    global total_time, words
    with open("statistic.txt", "w") as file:
        file.write(f"{total_time} {words}")
