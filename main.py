import requests
import telebot
from bs4 import BeautifulSoup as b

URL = 'https://cbr.ru/currency_base/daily/'
API_KEY = '6316752896:AAHK18e4I-TSFQFbFLu_UfZFiC_sW65_ALk'

def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    currencies = soup.find_all('td')                                ### на сайте по тегам ТД нашел строки таблицы для каждой валюты и далее их отсортировал, как в видосе
    clear_currencies = [c.text for c in currencies]
    a = 0                                                           ### тут задал счетчик количества шагов в списке, грубо говоря (там, насколько помню, +-215 элементов)
    united_currencies = []                                          ### шаг выше нужен, чтоб отдельные 215 элементов объединить в строку из 5 (как собс-но в таблице)
    for i in range(len(clear_currencies) // 5):                     ### тут погнали бегать соответственно по элементам и их объединять
        clear_currencies_str = ' '.join(clear_currencies[a:5 + a])  ### тут и счетчик пригодился бегаем от нулевого и через каждые пять
        united_currencies.append(clear_currencies_str)              ### ну и через аппенд завожу каждую объединенную строку в новый список (саму строку я просто переопределяю каждый проход)
        a += 5                                                      ### ну в конце само собой увеличиваем значение счетчика, чтобы двигаться по списку
    return united_currencies

list_of_currencies = parser(URL)                                    ### тут дофига атрибутов или как их там из видоса, в принципе можно и даже нужно почитать документацию бьютифулсупа(сам я еще не читал нихуя)

bot = telebot.TeleBot(API_KEY)                                      ### ну и атрибутов ТГ библы

@bot.message_handler(commands=['start'])                            ### это соответственно работа с запросом в чате и далее на нее ответ в хеллоу

def hello(message):
    bot.send_message(message.chat.id, 'Здравствуйте! Чтобы узнать курс интересующей Вас валюты, введите его полное название на русском или сокращенное название на английском языке.')

@bot.message_handler(content_types=['text'])
def currencies(message):
    temp_curr = ''                                                  ### тут задал тоже прокладку так ее назовем, она пригодится для условий
    for e in list_of_currencies:                                    ### бегу по элементам в списке
        if message.text.lower() in e.lower():                       ### работаю с нижним регистром и там и тут, сначала забыл элементы понизить, тогда некоторые валюты просто не принимало в запрос и писало, что неверно
            temp_curr += e                                          ### долларов дофега и не то, чтобы я дохуя универсальный код написал, но валюты все плюсуем в переменную, которую выдаем (пока так)
    if temp_curr != '':                                             ### соответственно, если введена лабуда, то запрос = отсос или нет не отсос :)
        bot.send_message(message.chat.id, temp_curr)
    else:
        bot.send_message(message.chat.id, 'Ваш запрос некорректен. Попробуйте снова!')

bot.polling()                                                       ### это постоянный чек чата на наличие новых смсок :3