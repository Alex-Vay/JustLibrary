import os
import g4f
import httpx
from langdetect import detect
from openai import OpenAI

numberSimilarBooks = 7


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
            )
            if (detect(response) == "en"):
                currentProviderIndex += 1
                continue
            return response
        except: currentProviderIndex += 1
    return g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "интеллектульный помощник", "content": message}],
    )


def getSimilarBooks(bookName):
    return getResponse("Приведи список из" + str(numberSimilarBooks) + "похожих на " + bookName + "книг")


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