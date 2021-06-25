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


def price_find(url):
    page = requests.get(url)

    variable = BeautifulSoup(page.text, "html.parser")

    Price = variable.find("div",
                          {"class": "Product__priceItem Product__priceItem--main js-product-price-item"}).text

    Price = Price.replace(' ', '')
    price_i = float(Price[0: int(len(Price) / 2) - 4])
    return(price_i)

def photo_upload(photo_url):
    f = open('out.jpg', 'wb')
    f.write(urllib.request.urlopen(
        photo_url).read())
    f.close()
    img = open('out.jpg', 'rb')
    bot.send_photo(uid, img)
    img.close()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global uid

    if uid == 0:
        bot.reply_to(message,
                     f'Приятно познакомиться, {message.from_user.first_name}. Я бот, созданный для помощи людям, собирающимся поехать на шашлыки.')

    uid = message.from_user.id

    Meat = [
      [{'Свинина':'10'}, {'Говядина':'11'}], [{'Баранина':'12'}, {'Курица':'13'}]
    ]

    kb_Meat = Keyboa(items=Meat, copy_text_to_callback=True).keyboard

    bot.send_message(
        chat_id=uid, reply_markup=kb_Meat,
        text='Какое мясо вы предпочитаете: свинину, говядину, баранину или курицу?')


@bot.callback_query_handler(func=lambda call: call.data.startswith('01'))
def back_to_meat_t(call):
    Meat = [
        [{'Свинина': '10'}, {'Говядина': '11'}], [{'Баранина': '12'}, {'Курица': '13'}]
    ]

    kb_Meat = Keyboa(items=Meat, copy_text_to_callback=True).keyboard

    bot.send_message(
        chat_id=uid, reply_markup=kb_Meat,
        text='Какое мясо вы предпочтёте в этот раз: свинину, говядину, баранину или курицу?')


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

    var = [[{'2-3 часа':'20'}, {'4-6 часов':'21'}], {'от 7 и до победного':'22'}]

    kb_time = Keyboa(items=var, copy_text_to_callback=True).keyboard

    if message.text.isdigit():
        n = float(message.text)
        bot.send_message(
            chat_id=uid, reply_markup=kb_time,
            text='Как долго планируете отдыхать?')

    else:
        bot.send_message(
            chat_id=uid,
            text='Это, конечно, хорошо, но не могли ли бы Вы ввести количество гостей числом, пожалуйста')


@bot.callback_query_handler(func=lambda call: call.data.startswith('2'))
def last_menu(call):
    global k
    if call.data == '21':
       k += 0.1
    elif call.data == '22':
       k += 0.2

    global n, uid, m

    m = round(n * k, 1)

    var = [{'Пошаговый рецепт приготовления':'30'}, {'Ссылка на видео-рецепт приготовления':'33'}, {'Список покупок':'31'},
           {'Рекомендованная цена продуктов':'32'}, {'Изменить вводные данные':'01'}]

    kb_recipe = Keyboa(items=var, copy_text_to_callback=True).keyboard

    bot.send_message(
        chat_id=uid, reply_markup=kb_recipe,
        text=f'Рекомендованное количество мяса - {m} кг')


@bot.callback_query_handler(func=lambda call: call.data.startswith('3'))
def main_menu(call):
    global m, uid, meat_t, n
    price_total = 0

    if call.data == '30' and meat_t == 0:
        bot.send_message(
            chat_id=uid,
            text=f'В миску наливаем растительное масло, добавляем {round(2 / 3 * m)} ч. л. черного перца, {round(2 / 3 * m)} ст. л. соевого соуса,{round(1 / 3 * m)} ст. л. соли, {round(1 / 9 * m, 1)} стакана сладкого соуса чили, {round(2 / 3 * m)} ч. л. сладкой паприки, {round(4 / 3 * m)} зубчика измельченного чеснока. Хорошо размешиваем.')

        photo_upload('https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-file-svinina_1.jpg')

        bot.send_message(
            chat_id=uid,
            text=f'Мясо режем на кубики размером с грецкий орех (кусочки по 30-40 г), укладываем в маринад и тщательно перемешиваем. Оставляем в закрытой посуде минимум на 3 часа для маринования.')

        photo_upload('https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-file-svinina_2.jpg')

        bot.send_message(
            chat_id=uid,
            text=f'Маринованное мясо нанизываем на шампуры и обжариваем на углях до готовности (с каждой стороны приблизительно по 5 минут). Не пережарьте!')

        photo_upload('https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-file-svinina_3.jpg')


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
        )


    elif call.data == '30' and meat_t == 1:
        bot.send_message(
            chat_id=uid,
            text=f'Готовим маринад: кладём в миску {round(1.5 / 2.5 * m, 1)} с. л. зиры, {round(1.5 / 2.5 * m, 1)} с. л. соли, {round(2 / 2.5 * m, 1)} ч. л. молотой сладкой паприки, {round(2 / 2.5 * m, 1)} ч. л. молотого чёрного перца..')

        photo_upload('https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-govyazhego-antrekota_1-1-300x225.jpg')

        bot.send_message(
            chat_id=uid,
            text=f'{round(4 / 2.5 * m)} луковицы чистим моем и нарезаем полукольцами, добавляем в миску со специями и перемешиваем.')

        photo_upload('https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-govyazhego-antrekota_2-1-300x225.jpg')

        bot.send_message(
            chat_id=uid,
            text=f'{m} кг говяжьего антрекота нарезаем на шашлык, кубиками со стороной приблизительно 2 сантиметра, массой приблизительно по 20 грамм')

        photo_upload('https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-govyazhego-antrekota_3-1-300x225.jpg')

        bot.send_message(
            chat_id=uid,
            text=f'Кладём мясо в маринад и хорошо перемешиваем, добавляем {round(150 / 2.5 * m)} мл газированной воды и опять тщательно перемешиваем.')

        photo_upload('https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-govyazhego-antrekota_4-300x225.jpg')

        bot.send_message(
            chat_id=uid,
            text=f'В закрытой посуде ставим в холодильник, минимум, на 3 часа (можно держать мясо в маринаде и сутки, и двое).')

        photo_upload('https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-govyazhego-antrekota_5-300x225.jpg')

        bot.send_message(
            chat_id=uid,
            text=f'Нанизываем на шашлычные палочки по 5 кусочков и жарим на углях на умеренном огне с двух сторон приблизительно по 4 минуты с каждой стороны, до готовности.')

        photo_upload('https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-govyazhego-antrekota_6-300x225.jpg')

        bot.send_message(
            chat_id=uid,
            text=f'Готовый шашлык из говяжьего антрекота подаём к столу со свежей лепёшкой.')

        photo_upload('https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-govyazhego-antrekota_8-300x225.jpg')


    elif call.data == '31' and meat_t == 1:
        bot.send_message(
            chat_id=uid,
            text=f"Говяжий антрекот - {m} кг"
                 '\n'
                 f"Лук - {round(4 / 2.5 * m)} шт"
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

        photo_upload('https://www.videoculinary.ru/wp-content/uploads/2013/08/shashlyk-iz-file-barashka_1.jpg')

        bot.send_message(
            chat_id=uid,
            text=f'Нарезаем мясо кубиками, со стороной 1.5см.')

        photo_upload('https://www.videoculinary.ru/wp-content/uploads/2013/08/shashlyk-iz-file-barashka_2.jpg')

        bot.send_message(
            chat_id=uid,
            text=f'Мясо нанизываем на шампуры по 4 кусочка на каждый, если мясо не жирное, можно добавить баранье курдючное сало, так же нарезанное кубиками.')

        photo_upload('https://www.videoculinary.ru/wp-content/uploads/2013/08/shashlyk-iz-file-barashka_3.jpg')

        bot.send_message(
            chat_id=uid,
            text=f'Для посыпания шашлыка во время жарки в отдельной посуде смешиваем специи: {round(2 / 2 * m)} ст. л. крупной соли, {round(2 / 2 * m)} ст. л. крупно помолотой зиры, {round(1 / 2 * m)} ст. л. сладкой паприки и {round(1 / 2 * m)} ч. л. молотого чёрного перца.')

        photo_upload('https://www.videoculinary.ru/wp-content/uploads/2013/08/shashlyk-iz-file-barashka_4.jpg')

        bot.send_message(
            chat_id=uid,
            text=f'Жарим шашлык на умеренном огне 3.5-4 минуты с каждой стороны, во время жарки посыпаем шашлык специями.')

        photo_upload('https://www.videoculinary.ru/wp-content/uploads/2013/08/shashlyk-iz-file-barashka_5.jpg')


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

        photo_upload('https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-kurinyh-okorochkov_1.jpg')

        bot.send_message(
            chat_id=uid,
            text=f'Нарезаем мясо на кусочки весом приблизительно по 20 г и кладём в маринад. Хорошо перемешиваем и оставляем в закрытой посуде в холодильнике минимально на 3 часа.')

        photo_upload('https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-kurinyh-okorochkov_2.jpg')

        bot.send_message(
            chat_id=uid,
            text=f'Маринованное мясо нанизываем на шампуры по 4-5 кусочков. Жарим на углях на умеренном огне по 3 - 4 минуты с каждой стороны.')

        photo_upload('https://www.videoculinary.ru/wp-content/uploads/2011/06/shashlyk-iz-kurinyh-okorochkov_3.jpg')


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

        bot.send_message(
            chat_id=uid,
            text=f'Цена взята с сайта https://vkusvill.ru')

        price_i = price_find('https://vkusvill.ru/goods/vyrezka-svinaya-gp-27633.html')
        price_total += price_i * m

        bot.send_message(
            chat_id=uid,
            text=f'Вырезка свиная ГП, {m} кг {price_i * m} руб.')

        photo_upload('https://img.vkusvill.ru/site/27633_1_27056.jpg?205')

        price_i = price_find('https://vkusvill.ru/goods/maslo-podsolnechnoe-neraf-vysokooleinovoe-steklo-36966.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Масло подсолнечное нераф. высокоолеиновое, стекло {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/36966_1_36791.jpg?116')

        price_i = price_find('https://vkusvill.ru/goods/perets-chernyy-molotyy-10-nbsp-g-16844.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Перец черный молотый, 10 г, {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/16844_1_14951.jpg?234')

        price_i = price_find('https://vkusvill.ru/goods/sol-pishchevaya-iletskaya-pomol-1-31619.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Соль пищевая «Илецкая», помол №1, {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/31619_1_29109.jpg?36')

        price_i = price_find('https://vkusvill.ru/goods/paprika-molotaya-16360.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Паприка молотая, {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/16360_1_14945.jpg?234')

        price_i = price_find('https://vkusvill.ru/goods/chesnok-17456.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Чеснок, {price_i} руб./ кг.')

        photo_upload('https://img.vkusvill.ru/site/17456_1_33359.jpg?5')

        price_i = price_find('https://vkusvill.ru/goods/sous-soevyy-16353.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Соус соевый, {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/16353_1_36808.jpg?234')

        price_i = price_find('https://vkusvill.ru/goods/sous-chim-chim-sladkiy-chili-300-nbsp-g-48721.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Соус Чим-Чим Сладкий Чили, {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/48721_1_53346.jpg?113')

        bot.send_message(
            chat_id=uid,
            text=f'Итоговая стоимость составит {price_total} руб.')

        bot.send_message(
            chat_id=uid,
            text=f'Это по {round(price_total / n)} руб. с каждого, если вы скидываетесь)')


    elif call.data == '32' and meat_t == 1:

        bot.send_message(
            chat_id=uid,
            text=f'Цена взята с сайта https://vkusvill.ru')

        price_i = price_find('https://vkusvill.ru/goods/govyadina-lopatka-bez-kosti-501.html')
        price_total += price_i * m

        bot.send_message(
            chat_id=uid,
            text=f'Говядина лопатка, без кости, {m} кг {price_i * m} руб.')

        photo_upload('https://img.vkusvill.ru/site/501_1_50544.JPG?175')

        price_i = price_find('https://vkusvill.ru/goods/luk-molodoy-repchatyy-22788.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Лук молодой репчатый {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/22788_1_54205.JPG?13')

        price_i = price_find('https://vkusvill.ru/goods/zira-38455.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Зира {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/38455_1_41520.jpg?156')

        price_i = price_find('https://vkusvill.ru/goods/paprika-molotaya-16360.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Паприка молотая {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/16360_1_14945.jpg?234')

        price_i = price_find('https://vkusvill.ru/goods/perets-chernyy-molotyy-10-nbsp-g-16844.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Перец черный молотый, 10 г, {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/16844_1_14951.jpg?234')

        price_i = price_find('https://vkusvill.ru/goods/sol-pishchevaya-iletskaya-pomol-1-31619.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Соль пищевая «Илецкая», помол №1, {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/31619_1_29109.jpg?36')

        price_i = price_find('https://vkusvill.ru/goods/voda-rodnikovaya-gazirovannaya-500-ml-17826.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Вода родниковая газированная, 500 мл, {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/17826_1_52539.jpg?102')

        bot.send_message(
            chat_id=uid,
            text=f'Итоговая стоимость составит {price_total} руб.')

        bot.send_message(
            chat_id=uid,
            text=f'Это по {round(price_total / n)} руб. с каждого, если вы скидываетесь)')


    elif call.data == '32' and meat_t == 2:

        bot.send_message(
            chat_id=uid,
            text=f'Цена взята с сайта https://vkusvill.ru')

        price_i = price_find('https://vkusvill.ru/goods/yagnyenok-na-zharkoe-myaso-est-okhl-200-nbsp-g--45650.html')
        price_total += price_i * m * 5

        bot.send_message(
            chat_id=uid,
            text=f'Ягнёнок на жаркое Мясо Есть! охл., {m} кг {price_i * m * 5} руб.')

        photo_upload('https://img.vkusvill.ru/site/45650_1_45673.jpg?127')

        price_i = price_find('https://vkusvill.ru/goods/salo-belorusskoe-narezka-21722.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Сало баранье курдючное найти почти нереально, поэтому можно использовать это \n Сало «Белорусское», нарезка {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/21722_1_21100.jpg?135')

        price_i = price_find('https://vkusvill.ru/goods/sol-pishchevaya-iletskaya-pomol-1-31619.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Соль пищевая «Илецкая», помол №1 {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/31619_1_29109.jpg?36')

        price_i = price_find('https://vkusvill.ru/goods/zira-38455.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Зира {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/38455_1_41520.jpg?156')

        price_i = price_find('https://vkusvill.ru/goods/paprika-molotaya-16360.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Паприка молотая {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/16360_1_14945.jpg?234')

        price_i = price_find('https://vkusvill.ru/goods/perets-chernyy-molotyy-10-nbsp-g-16844.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Перец черный молотый, 10 г, {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/16844_1_14951.jpg?234')

        bot.send_message(
            chat_id=uid,
            text=f'Итоговая стоимость составит {price_total} руб.')

        bot.send_message(
            chat_id=uid,
            text=f'Это по {round(price_total / n)} руб. с каждого, если вы скидываетесь)')


    elif call.data == '32' and meat_t == 3:

        bot.send_message(
            chat_id=uid,
            text=f'Цена взята с сайта https://vkusvill.ru')

        price_i = price_find('https://vkusvill.ru/goods/file-grudki-tsyplenka-488.html')
        price_total += price_i * m

        bot.send_message(
            chat_id=uid,
            text=f'Филе грудки цыпленка, {m} кг {price_i * m} руб.')

        photo_upload('https://img.vkusvill.ru/site/488_1_36153.jpg?25')

        price_i = price_find('https://vkusvill.ru/goods/sol-pishchevaya-iletskaya-pomol-1-31619.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Соль пищевая «Илецкая», помол №1 {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/31619_1_29109.jpg?36')

        price_i = price_find('https://vkusvill.ru/goods/zira-38455.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Зира {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/38455_1_41520.jpg?156')

        price_i = price_find('https://vkusvill.ru/goods/paprika-molotaya-16360.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Паприка молотая {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/16360_1_14945.jpg?234')

        price_i = price_find('https://vkusvill.ru/goods/perets-chernyy-molotyy-10-nbsp-g-16844.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Перец черный молотый, 10 г, {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/16844_1_14951.jpg?234')

        price_i = price_find('https://vkusvill.ru/goods/maslo-podsolnechnoe-neraf-vysokooleinovoe-steklo-36966.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Масло подсолнечное нераф. высокоолеиновое, стекло {price_i} руб.')

        photo_upload('https://img.vkusvill.ru/site/36966_1_36791.jpg?116')

        price_i = price_find('https://vkusvill.ru/goods/chesnok-17456.html')
        price_total += price_i

        bot.send_message(
            chat_id=uid,
            text=f'Чеснок, {price_i} руб./ кг.')

        photo_upload('https://img.vkusvill.ru/site/17456_1_33359.jpg?5')

        bot.send_message(
            chat_id=uid,
            text=f'Итоговая стоимость составит {price_total} руб.')

        bot.send_message(
            chat_id=uid,
            text=f'Это по {round(price_total / n)} руб. с каждого, если вы скидываетесь)')


    elif call.data == '33' and meat_t == 0:

        bot.send_message(
            chat_id=uid,
            text=f'https://youtu.be/KGuH4CWN3DA?list=PLQzBJgojWxHPsKHnPxq5Nki4HTyLcxOyN')


    elif call.data == '33' and meat_t == 1:

        bot.send_message(
            chat_id=uid,
            text=f'https://youtu.be/TtgVFkk4kf4?list=PLQzBJgojWxHPsKHnPxq5Nki4HTyLcxOyN')


    elif call.data == '33' and meat_t == 2:

        bot.send_message(
            chat_id=uid,
            text=f'https://youtu.be/NbiAFDRN2oM?list=PLQzBJgojWxHPsKHnPxq5Nki4HTyLcxOyN')


    elif call.data == '33' and meat_t == 3:

        bot.send_message(
            chat_id=uid,
            text=f'https://youtu.be/fibrZS7uj1Q?list=PLQzBJgojWxHPsKHnPxq5Nki4HTyLcxOyN')


    back = [{'Назад': '23'}]

    kb_back = Keyboa(items=back, copy_text_to_callback=True).keyboard

    bot.send_message(
        chat_id=uid, reply_markup=kb_back,
        text=f'Хотите вернуться назад?')


bot.polling(none_stop=True)