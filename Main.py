import telebot
import urllib
import requests
from bs4 import BeautifulSoup

from keyboa import Keyboa
bot = telebot.TeleBot('1834705224:AAF_PjtpCiJYIweJWBKZFSqg6LaAmJrb63s')



meat_t = -1
uid = 0
n = 0
m = 0
k = 0.4

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global uid
    uid = message.from_user.id
    bot.reply_to(message, f'Приятно познакомиться, {message.from_user.first_name}. Я бот, созданный для помощи людям, собирающимся поехать на шашлыки.')

    Meat = [
      [{'Свинина':'10'}, {'Говядина':'11'}], [{'Баранина':'12'}, {'Курица':'13'}]
    ]

    kb_Meat = Keyboa(items=Meat, copy_text_to_callback=True).keyboard

    bot.send_message(
        chat_id=uid, reply_markup=kb_Meat,
        text='Какое мясо вы предпочитаете: свинину, говядину,баранину или курицу?')

@bot.callback_query_handler(func=lambda call: call.data.startswith('1'))
def meat_finder(call):
    global meat_t, k

    if call.data == '10':
       meat_t = 0
    elif call.data == '11':
       meat_t = 1
    elif call.data == '12':
       meat_t = 2
    elif call.data == '13':
       meat_t = 3
       k += 0.1

    bot.send_message(
        chat_id=uid,
        text='Какое предпологаемое количество гостей на вашей встрече?')


@bot.message_handler(content_types=['text'])
def guest_amount(message):
    global n, uid
    n = float(message.text)

    var = [[{'2-3 часа':'20'}, {'4-6 часов':'21'}], {'от 7 и до победного':'22'}]

    kb_time = Keyboa(items=var, copy_text_to_callback=True).keyboard

    bot.send_message(
        chat_id=uid, reply_markup=kb_time,
        text='Как долго планируете отдыхать?')

@bot.callback_query_handler(func=lambda call: call.data.startswith('2'))
def last_menu(call):
    global k
    if call.data == '21':
       k += 0.1
    elif call.data == '22':
       k += 0.2

    global n, uid, m

    m = round(n * k, 1)

    var = [{'Рецепт приготовления':'30'}, {'Список покупок':'31'}, {'Рекомендованная цена мяса':'32'}]

    kb_recipe = Keyboa(items=var, copy_text_to_callback=True).keyboard

    bot.send_message(
        chat_id=uid, reply_markup=kb_recipe,
        text=f'Рекомендованное количество мяса - {m} кг')

@bot.callback_query_handler(func=lambda call: call.data.startswith('3'))
def main_menu(call):
    global m, uid, meat_t

    if call.data == '30' and meat_t == 0:
        bot.send_message(
            chat_id=uid,
            text=f'В миску наливаем растительное масло, добавляем {round(2 / 3 * m)} ч. л. черного перца, {round(2 / 3 * m)} ст. л. соевого соуса,{round(1 / 3 * m)} ст. л. соли, {round(1 / 9 * m, 1)} стакана сладкого соуса чили, {round(2 / 3 * m)} ст. ложки семян кинзы, {round(2 / 3 * m)} ч. л. сладкой паприки, {round(4 / 3 * m)} зубчика измельченного чеснока. Хорошо размешиваем.')
        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-file-svinina_1.jpg').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()

        bot.send_message(
            chat_id=uid,
            text=f'Мясо режем на кубики размером с грецкий орех (кусочки по 30-40 г), укладываем в маринад и тщательно перемешиваем. Оставляем в закрытой посуде минимум на 3 часа для маринования.')
        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-file-svinina_2.jpg').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()

        bot.send_message(
            chat_id=uid,
            text=f'Маринованное мясо нанизываем на шампуры и обжариваем на углях до готовности (с каждой стороны приблизительно по 5 минут). Не пережарьте!')
        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-file-svinina_3.jpg').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()


    elif call.data == '31' and meat_t == 0:
        bot.send_message(
            chat_id=uid,
            text=f"Свинина - {m} кг"
                 '\n'
                 f"Масло растительное - {round(100 / 3 * m)} грамм"
                 '\n'
                 f"Чёрный молотый перец - {round(2 / 3 * m)} ч. л."
                 '\n'
                 f"Соль - {round(1 / 3 * m)} ст. л."
                 '\n'
                 f"Сладкая паприка - {round(2 / 3 * m)} ч. л."
                 '\n'
                 f"Чеснок - {round(4 / 3 * m)} зубчика(-ов)"
                 '\n'
                 f"Соевый соус - {round(2 / 3 * m)} ст. л."
                 '\n'
                 f"Сладкий соус чили - {round(1 / 9 * m, 1)} стакана"
                 '\n'
                 f"Молотые семена кинзы - {round(2 / 3 * m)} ст. ложки"
        )


    elif call.data == '30' and meat_t == 1:
        bot.send_message(
            chat_id=uid,
            text=f'Готовим маринад: кладём в миску {round(1.5 / 2.5 * m, 1)} с. л. семян кинзы, {round(1.5 / 2.5 * m, 1)} с. л. зиры, {round(1.5 / 2.5 * m, 1)} с. л. соли, {round(2 / 2.5 * m, 1)} ч. л. молотой сладкой паприки, {round(2 / 2.5 * m, 1)} ч. л. молотого чёрного перца..')
        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-govyazhego-antrekota_1-1-300x225.jpg').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()

        bot.send_message(
            chat_id=uid,
            text=f'{round(4 / 2.5 * m)} луковицы чистим моем и нарезаем полукольцами, добавляем в миску со специями и перемешиваем.')
        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-govyazhego-antrekota_2-1-300x225.jpg').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()

        bot.send_message(
            chat_id=uid,
            text=f'{m} кг говяжьего антрекота нарезаем на шашлык, кубиками со стороной приблизительно 2 сантиметра, массой приблизительно по 20 грамм')
        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-govyazhego-antrekota_3-1-300x225.jpg').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()

        bot.send_message(
            chat_id=uid,
            text=f'Кладём мясо в маринад и хорошо перемешиваем, добавляем {round(150 / 2.5 * m)} мл газированной воды и опять тщательно перемешиваем.')
        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-govyazhego-antrekota_4-300x225.jpg').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()

        bot.send_message(
            chat_id=uid,
            text=f'В закрытой посуде ставим в холодильник, минимум, на 3 часа (можно держать мясо в маринаде и сутки, и двое).')
        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-govyazhego-antrekota_5-300x225.jpg').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()

        bot.send_message(
            chat_id=uid,
            text=f'Нанизываем на шашлычные палочки по 5 кусочков и жарим на углях на умеренном огне с двух сторон приблизительно по 4 минуты с каждой стороны, до готовности.')
        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-govyazhego-antrekota_6-300x225.jpg').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()

        bot.send_message(
            chat_id=uid,
            text=f'Готовый шашлык из говяжьего антрекота подаём к столу со свежей лепёшкой.')
        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-govyazhego-antrekota_8-300x225.jpg').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()


    elif call.data == '31' and meat_t == 1:
        bot.send_message(
            chat_id=uid,
            text=f"Говяжий антрекот - {m} кг"
                 '\n'
                 f"Лук - {round(4 / 2.5 * m)} шт"
                 '\n'
                 f"Кинза семена - {round(1.5 / 2.5 * m)} ст. л."
                 '\n'
                 f"Зира - {round(1.5 / 2.5 * m)} ст. л."
                 '\n'
                 f"Паприка сладкая - {round(2 / 2.5 * m)} ч. л."
                 '\n'
                 f"Молотый чёрный перец - {round(2 / 2.5 * m)} ч. л."
                 '\n'
                 f"Соль - {round(1.5 / 2.5 * m)} ст. л."
                 '\n'
                 f"Газированная вода - {round(150 / 2.5 * m)} мл"
        )


    elif call.data == '30' and meat_t == 2:
        bot.send_message(
            chat_id=uid,
            text=f'Для приготовления шашлыка из филе баранины снимаем мякоть с седла барашка или с корейки.')
        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://www.videoculinary.ru/wp-content/uploads/2013/08/shashlyk-iz-file-barashka_1.jpg').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()

        bot.send_message(
            chat_id=uid,
            text=f'Нарезаем мясо кубиками, со стороной 1.5см.')
        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://www.videoculinary.ru/wp-content/uploads/2013/08/shashlyk-iz-file-barashka_2.jpg').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()

        bot.send_message(
            chat_id=uid,
            text=f'Мясо нанизываем на шампуры по 4 кусочка на каждый, если мясо не жирное, можно добавить баранье курдючное сало, так же нарезанное кубиками.')
        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://www.videoculinary.ru/wp-content/uploads/2013/08/shashlyk-iz-file-barashka_3.jpg').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()

        bot.send_message(
            chat_id=uid,
            text=f'Для посыпания шашлыка во время жарки в отдельной посуде смешиваем специи: {round(2 / 2 * m)} ст. л. крупной соли, {round(2 / 2 * m)} ст. л. крупно помолотой зиры, {round(1 / 2 * m)} ст. л. сладкой паприки и {round(1 / 2 * m)} ч. л. молотого чёрного перца.')
        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://www.videoculinary.ru/wp-content/uploads/2013/08/shashlyk-iz-file-barashka_4.jpg').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()

        bot.send_message(
            chat_id=uid,
            text=f'Жарим шашлык на умеренном огне 3.5-4 минуты с каждой стороны, во время жарки посыпаем шашлык специями.')
        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://www.videoculinary.ru/wp-content/uploads/2013/08/shashlyk-iz-file-barashka_5.jpg').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()


    elif call.data == '31' and meat_t == 2:
        bot.send_message(
            chat_id=uid,
            text=f"Филе баранье - {m} кг"
                 '\n'
                 f"Сало баранье курдючное - по необходимости"
                 '\n'
                 f"Крупная соль - {round(2 / 2 * m)} ст. л."
                 '\n'
                 f"Зира - {round(2 / 2 * m)} ст. л."
                 '\n'
                 f"Сладкая паприка - {round(1 / 2 * m)} ст. л."
                 '\n'
                 f"Чёрный перец - {round(1 / 2 * m)} ч. л."
        )


    elif call.data == '30' and meat_t == 3:
        bot.send_message(
            chat_id=uid,
            text=f'Маринад: кладём в миску {round(2 * m)} ч.л. сладкой паприки, {round(2 * m)} ч.л. соли, {round(2 * m)} ст.л. зиры, {round(1 * m)} ч.л. молотого чёрного перца, {round(2 * m)} измельчённых зубчика(-ов) чеснока и {round(100 * m)} г растительного масла. Тщательно перемешиваем. Маринад готов.')
        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-kurinyh-okorochkov_1.jpg').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()

        bot.send_message(
            chat_id=uid,
            text=f'Нарезаем мясо на кусочки весом приблизительно по 20 г и кладём в маринад. Хорошо перемешиваем и оставляем в закрытой посуде в холодильнике минимально на 3 часа.')
        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-kurinyh-okorochkov_2.jpg').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()

        bot.send_message(
            chat_id=uid,
            text=f'Маринованное мясо нанизываем на шампуры по 4-5 кусочков. Жарим на углях на умеренном огне по 3 - 4 минуты с каждой стороны.')
        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-kurinyh-okorochkov_3.jpg').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()


    elif call.data == '31' and meat_t == 3:
        bot.send_message(
            chat_id=uid,
            text=f"Куриные окорочка - {m} кг"
                 '\n'
                 f"Молотая сладкая паприка - {round(2 * m)} ч. л."
                 '\n'
                 f"Соль - {round(2 * m)} ч. л."
                 '\n'
                 f"Зира - {round(2 * m)} ст. л."
                 '\n'
                 f"Молотый чёрный перец - {round(1 * m)} ч. л."
                 '\n'
                 f"Чеснок - {round(2 * m)} зубчика(-ов)"
                 '\n'
                 f"Растительное масло - {round(100 * m)} грамм"
        )


    elif call.data == '32' and meat_t == 0:

        url = 'https://vkusvill.ru/goods/vyrezka-svinaya-gp-27633.html'

        page = requests.get(url)

        variable = BeautifulSoup(page.text, "html.parser")

        Price = variable.find("div",
                              {"class": "Product__priceItem Product__priceItem--main js-product-price-item"}).text

        Price = Price.replace(' ', '')
        price_i = float(Price[0: int(len(Price) / 2) - 4])

        bot.send_message(
            chat_id=uid,
            text=f'Цена взята с сайта https://vkusvill.ru')

        bot.send_message(
            chat_id=uid,
            text=f'Вырезка свиная ГП, {m} кг {price_i * m} руб.')

        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://img.vkusvill.ru/site/27633_1_27056.jpg?205').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()


    elif call.data == '32' and meat_t == 1:

        url = 'https://vkusvill.ru/goods/govyadina-lopatka-bez-kosti-501.html'

        page = requests.get(url)

        variable = BeautifulSoup(page.text, "html.parser")

        Price = variable.find("div",
                              {"class": "Product__priceItem Product__priceItem--main js-product-price-item"}).text

        Price = Price.replace(' ', '')
        price_i = float(Price[0: int(len(Price) / 2) - 4])

        bot.send_message(
            chat_id=uid,
            text=f'Цена взята с сайта https://vkusvill.ru')

        bot.send_message(
            chat_id=uid,
            text=f'Вырезка свиная ГП, {m} кг {price_i * m} руб.')

        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://img.vkusvill.ru/site/501_1_50544.JPG?175').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()


    elif call.data == '32' and meat_t == 2:

        url = 'https://vkusvill.ru/goods/yagnyenok-na-zharkoe-myaso-est-okhl-200-nbsp-g--45650.html'

        page = requests.get(url)

        variable = BeautifulSoup(page.text, "html.parser")

        Price = variable.find("div",
                              {"class": "Product__priceItem Product__priceItem--main js-product-price-item"}).text

        Price = Price.replace(' ', '')
        price_i = float(Price[0: int(len(Price) / 2) - 4]) * 5

        bot.send_message(
            chat_id=uid,
            text=f'Цена взята с сайта https://vkusvill.ru')

        bot.send_message(
            chat_id=uid,
            text=f'Вырезка свиная ГП, {m} кг {price_i * m} руб.')

        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://img.vkusvill.ru/site/45650_1_45673.jpg?127').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()


    elif call.data == '32' and meat_t == 3:

        url = 'https://vkusvill.ru/goods/file-grudki-tsyplenka-488.html'

        page = requests.get(url)

        variable = BeautifulSoup(page.text, "html.parser")

        Price = variable.find("div",
                              {"class": "Product__priceItem Product__priceItem--main js-product-price-item"}).text

        Price = Price.replace(' ', '')
        price_i = float(Price[0: int(len(Price) / 2) - 4])

        bot.send_message(
            chat_id=uid,
            text=f'Цена взята с сайта https://vkusvill.ru')

        bot.send_message(
            chat_id=uid,
            text=f'Вырезка свиная ГП, {m} кг {price_i * m} руб.')

        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(
            'https://img.vkusvill.ru/site/488_1_36153.jpg?25').read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(uid, img)
        img.close()

    back = [{'Назад': '23'}]

    kb_back = Keyboa(items=back, copy_text_to_callback=True).keyboard

    bot.send_message(
        chat_id=uid, reply_markup=kb_back,
        text=f'Хотите вернуться назад?')

bot.polling(none_stop=True)