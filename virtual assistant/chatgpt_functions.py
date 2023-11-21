import time
import g4f

number_similar_books = 7

def get_response(message):
    _providers = [
        g4f.Provider.GeekGpt,
        g4f.Provider.ChatBase,
        g4f.Provider.GPTalk,
        g4f.Provider.GptForLove,
        g4f.Provider.AItianhuSpace,
        g4f.Provider.Liaobots,
    ]
    current_provider_index = 0;
    while (current_provider_index < len(_providers)):
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message}],
                provider=_providers[current_provider_index],
                #stream=True,
            )
            return response
            #print(_providers[current_provider_index])
            # for message in response: #возможно переписать на ялд чтобы возвращал как бы онлайн
            #     yield (message)
            ## for i in get_response("Гарри Потер и философский камень"):
            ##     print(i, end="")
        except: current_provider_index += 1
    return g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}],
    )


'''
планируется подлючить эту функцию на кнопку (допустим при нажатии пкм по книге появиться кнопка "найди похожие")
'''
def get_similar_books(book_name):
    return get_response("Приведи список из" + str(number_similar_books) + "похожих на " + book_name + "книг")


'''
планируется подлючить эту функцию на кнопку внутри читалки при выделенном тексте (допустим при выделении появиться кнопка "объясни")
'''
def explain_term(term):
    if (len(term.split()) > 2):
        return get_response("Объясни значение фразы" + term)
    return get_response("Объясни значение слова" + term)

print(get_similar_books("Приключение барона Мюнхгаузена"))

