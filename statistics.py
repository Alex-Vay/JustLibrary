import time
import os

words = 0
totalTime = 0
startTime = 0


def getStatistics():
    global totalTime, words
    try:
        with open("statistic.txt", "r") as file:
            statistics = file.read().split()
            totalTime, words = float(statistics[0]), int(statistics[1])
    except:
        pass
    return f"Время чтения: {round(totalTime / 3600, 4)} часов   Скорость чтения (в словах в минуту): {int(0 if totalTime == 0 else words / totalTime * 60)}"


def startTimer():
    global startTime
    startTime = time.time()
    print(startTime)


def stopTimer(text_path):
    global startTime, totalTime, words
    end_time = time.time()
    print(startTime)
    print(end_time)
    totalTime += end_time - startTime
    words += countWords(text_path)
    saveDataOnExit()


def cleanStatistics():
    global totalTime, words
    totalTime = 0
    words = 0
    try:
        os.remove("statistic.txt")
    except:
        pass
    getStatistics()


def countWords(text_part):
    return len(text_part.split())


def saveDataOnExit():
    global totalTime, words
    with open("statistic.txt", "w") as file:
        file.write(f"{totalTime} {words}")
