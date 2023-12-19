import os
import g4f
import httpx
from langdetect import detect
from openai import OpenAI

numberSimilarBooks = 7

# Работает с пересказом текстов, но только по ссылке, я не нашел как перестроить это на текст
# def yandexGpt (text30k):
#     import requests
#     endpoint = 'https://300.ya.ru/api/sharing-url'
#     response = requests.post(
#         endpoint,
#         json={
#             'article_url': 'https://habr.com/ru/news/729422/'
#         },
#         headers={'Authorization': 'OAuth !token!'}
#     )
#
#     print(response.text)

def getResponse(message):
    apiKey = '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'
    os.environ["OPENAI_API_KEY"] = apiKey
    client = OpenAI(
        http_client=httpx.Client(
        proxies="http://RFk9wC:Q8AS8q@46.232.14.84:8000",
        ),
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "user",
             "content": message
            }
        ],
    )
    return response.choices[0].message.content


def getResponse2(message):
    _providers = [
        g4f.Provider.GeekGpt,
        g4f.Provider.ChatBase,
        g4f.Provider.GPTalk,
        g4f.Provider.GptForLove,
        g4f.Provider.AItianhuSpace,
        g4f.Provider.Liaobots,
    ]
    currentProviderIndex = 0
    while (currentProviderIndex < len(_providers)):
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message}],
                provider=_providers[currentProviderIndex],
                #stream=True,
            )
            if (detect(response) == "en"):
                currentProviderIndex += 1
                continue
            return response
            #print(_providers[currentProviderIndex])
            # for message in response: #возможно переписать на ялд чтобы возвращал как бы онлайн
            #     yield (message)
            ## for i in get_response("Гарри Потер и философский камень"):
            ##     print(i, end="")
        except: currentProviderIndex += 1
    return g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "интеллектульный помощник", "content": message}],
    )


'''
планируется подлючить эту функцию на кнопку (допустим при нажатии пкм по книге появиться кнопка "найди похожие")
'''
def getSimilarBooks(bookName):
    return getResponse("Приведи список из" + str(numberSimilarBooks) + "похожих на " + bookName + "книг")
#Приведи просто список (без дополнительных фраз или словосочетаний, помимо названия книг)\из" + str(number_similar_books) + "похожих на " + book_name + "книг")


'''
планируется подлючить эту функцию на кнопку внутри читалки при выделенном тексте (допустим при выделении появиться кнопка "объясни")
'''
def explainTerm(term):
    if (len(term.split()) > 2):
        return getResponse("Объясни значение фразы " + term)
    return getResponse("Объясни значение слова " + term)

def getBookInfo(bookName):
    return getResponse("Приведи только достоверные исторические факты о книге " + bookName)

def getBbookAnalogies(bookName):
    return getResponse("Приведи примеры только реально существующих фильмов и пьес по книге " + bookName)

def retellText(text8kLimited):
    try:
        return getResponse("Перескажи текст:\n" + text8kLimited)
    except:
        return "Текст слишном большой для пересказа, для лучшего понимания советуем прочитать его самостоятельно)"

print(retellText(input()))
print(getSimilarBooks("Капитанская дочка"))
print(explainTerm("Клан"))
print(getBookInfo("Капитанская дочка"))
print(getBbookAnalogies("Капитанская дочка"))
