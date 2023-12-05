import os
import time

import g4f
import httpx
from langdetect import detect
from openai import OpenAI

number_similar_books = 7

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

def get_response(message):
    api_key = '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'
    os.environ["OPENAI_API_KEY"] = api_key
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


def get_response2(message):
    _providers = [
        g4f.Provider.GeekGpt,
        g4f.Provider.ChatBase,
        g4f.Provider.GPTalk,
        g4f.Provider.GptForLove,
        g4f.Provider.AItianhuSpace,
        g4f.Provider.Liaobots,
    ]
    current_provider_index = 0
    while (current_provider_index < len(_providers)):
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message}],
                provider=_providers[current_provider_index],
                #stream=True,
            )
            if (detect(response) == "en"):
                current_provider_index += 1
                continue
            return response
            #print(_providers[current_provider_index])
            # for message in response: #возможно переписать на ялд чтобы возвращал как бы онлайн
            #     yield (message)
            ## for i in get_response("Гарри Потер и философский камень"):
            ##     print(i, end="")
        except: current_provider_index += 1
    return g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "интеллектульный помощник", "content": message}],
    )


'''
планируется подлючить эту функцию на кнопку (допустим при нажатии пкм по книге появиться кнопка "найди похожие")
'''
def get_similar_books(book_name):
    return get_response("Приведи список из" + str(number_similar_books) + "похожих на " + book_name + "книг")
#Приведи просто список (без дополнительных фраз или словосочетаний, помимо названия книг)\из" + str(number_similar_books) + "похожих на " + book_name + "книг")


'''
планируется подлючить эту функцию на кнопку внутри читалки при выделенном тексте (допустим при выделении появиться кнопка "объясни")
'''
def explain_term(term):
    if (len(term.split()) > 2):
        return get_response("Объясни значение фразы " + term)
    return get_response("Объясни значение слова " + term)

def get_book_info(book_name):
    return get_response("Приведи только достоверные исторические факты о книге " + book_name)

def get_book_analogies(book_name):
    return get_response("Приведи примеры только реально существующих фильмов и пьес по книге " + book_name)

def retell_text(text_8k_limited):
    try:
        return get_response("Перескажи текст:\n" + text_8k_limited)
    except:
        return "Текст слишном большой для пересказа, для лучшего понимания советуем прочитать его самостоятельно)"

print(retell_text(input()))
print(get_similar_books("Капитанская дочка"))
print(explain_term("Клан"))
print(get_book_info("Капитанская дочка"))
print(get_book_analogies("Капитанская дочка"))
