import requests
import telebot
from connect import TOKEN, save_user_data
from button import main_menu, main_submenu1_view, main_submenu2_view, main_submenu3_view, menu_back, create_submenu1, \
    menu_back2, main_feedback
from other import global_list, UserDataDBs, user_data
from telebot import types

bot = telebot.TeleBot(TOKEN)




#########################                                                                              ######################################################
######################### Функция для создания inline-клавиатуры с кнопками "Предыдущая" и "Следующая" ######################################################
#########################                                                                              ######################################################
def create_inline_keyboard(index, data_list, counts, data_url):
    print(index, data_list, counts, data_url)
    keyboard = types.InlineKeyboardMarkup()
    bask = types.InlineKeyboardButton(text='Назад', callback_data='back_menu')
    send_messages = types.InlineKeyboardButton(text='Написать', url=(data_url[index]))
    if counts == 1:
        keyboard.add(send_messages)
        keyboard.add(bask)
    else:
        # Если это не последний элемент в списке, добавляем кнопку "Следующая"
        if index == len(data_list) - 1:
            button_next = types.InlineKeyboardButton('Следующая', callback_data='pass_r')
            button_previous = types.InlineKeyboardButton('Предыдущая', callback_data='previous')
            keyboard.row(button_previous, send_messages, button_next)
            keyboard.add(bask)
        # Если это не первый элемент в списке, добавляем кнопку "Предыдущая"
        if index == 0:
            button_next = types.InlineKeyboardButton('Следующая', callback_data='next')
            button_previous = types.InlineKeyboardButton('Предыдущая', callback_data='pass_l')
            keyboard.row(button_previous, send_messages, button_next)
            keyboard.add(bask)
        if index > 0 and index < len(data_list) - 1:
            button_next = types.InlineKeyboardButton('Следующая', callback_data='next')
            button_previous = types.InlineKeyboardButton('Предыдущая', callback_data='previous')
            keyboard.row(button_previous, send_messages, button_next)
            keyboard.add(bask)
    return keyboard



############################                                                               ######################################################
############################ Функция для отправки формы для заполнения данных пользователя ######################################################
############################                                                               ######################################################
def send_user_data_form(message, db_tables_index):
    chat_id = message.chat.id
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)  # Удаление сообщения
    bot.register_next_step_handler_by_chat_id(chat_id, get_username, user_data, db_tables_index)
    # меню
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='Отмена', callback_data='back_stop'))
    return menu


def get_username(message, user_data, db_tables_index):
    chat_id = message.chat.id
    user_data.username = message.text  # записывает Имя
    bot.send_message(chat_id, "Введите Сумму:")  # отправка сообщения
    bot.register_next_step_handler_by_chat_id(chat_id, get_money, user_data, db_tables_index)



def get_money(message, user_data, db_tables_index):
    chat_id = message.chat.id
    try:
        user_data.money = int(message.text)  # записывает Имя
        bot.send_message(chat_id, "Введите Описание")  # отправка сообщения
        bot.register_next_step_handler_by_chat_id(chat_id, get_occupation, user_data, db_tables_index)
    except ValueError:
        bot.send_message(chat_id, "Введите корректную сумму:")
        bot.register_next_step_handler_by_chat_id(chat_id, get_money, user_data, db_tables_index)


def get_occupation(message, user_data, db_tables_index):
    chat_id = message.chat.id
    user_data.occupation = message.text
    bot.send_message(chat_id, "Введите Вашу ссылку на телеграм канал\nПример: https://t.me/mynik")  # отправка сообщения
    bot.register_next_step_handler_by_chat_id(chat_id, get_url, user_data, db_tables_index)



def get_url(message, user_data, db_tables_index):
    chat_id = message.chat.id
    try:
        response = requests.get(message.text)
        if response.status_code == 200:
            user_data.url = message.text
            save_user_data(chat_id, user_data, db_tables_index)
            bot.send_message(chat_id, "🎁Данные сохранены🎁")
            bot.send_photo(message.chat.id, photo=open('imgaes.jpg', 'rb'),
                           caption="🌴Раздел меню🌴\n🎁Здесь ты можешь выбрать разделы интересующие тебя🎁")
        else:
            bot.send_message(chat_id, "Введите корректный URL:")
            bot.register_next_step_handler_by_chat_id(chat_id, get_url, user_data, db_tables_index)
    except:
        bot.send_message(chat_id, "Введите корректный URL:")
        bot.register_next_step_handler_by_chat_id(chat_id, get_url, user_data, db_tables_index)



############################                                                         ######################################################
############################ Создаем функцию, которая обрабатывает нажатия на кнопки ######################################################
############################                                                         ######################################################
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    ############################################# Кнопки с Раздела ВЫБОРА УСЛУГ #############################################
    if call.data == 'main_submenu1_view_button_1':
        bot.edit_message_media(chat_id=call.message.chat.id,
                               message_id=call.message.message_id,
                               media=telebot.types.InputMedia(type='photo', media=open('imgaes-pik.jpg', 'rb')),
                               reply_markup=main_submenu1_view())

    # Обрабатываем нажатие на кнопку главного меню
    elif call.data == 'main_submenu1_view_button_2':
        bot.edit_message_media(chat_id=call.message.chat.id,
                               message_id=call.message.message_id,
                               media=telebot.types.InputMedia(type='photo', media=open('imgaes-create.jpg', 'rb')),
                               reply_markup=main_submenu2_view())

    # Обрабатываем нажатие на кнопку главного меню
    elif call.data == 'main_submenu1_view_button_3':
        bot.edit_message_media(chat_id=call.message.chat.id,
                               message_id=call.message.message_id,
                               media=telebot.types.InputMedia(type='photo', media=open('imgaes-create.jpg', 'rb')),
                               reply_markup=main_submenu3_view())


    # Обрабатываем нажатие на кнопку "Вернуться в главное меню"
    elif call.data == 'back':
        bot.edit_message_media(chat_id=call.message.chat.id,
                               message_id=call.message.message_id,
                               media=telebot.types.InputMedia(type='photo', media=open('imgaes.jpg', 'rb')),
                               reply_markup=main_menu())


    ############################################# Кнопки Вернуться #############################################
    # Обрабатываем нажатие на кнопку "Вернуться в Меню 1"
    elif call.data == 'back_menu':
        bot.edit_message_media(chat_id=call.message.chat.id,
                               message_id=call.message.message_id,
                               media=telebot.types.InputMedia(type='photo', media=open('imgaes.jpg', 'rb')),
                               reply_markup=main_submenu1_view())    # Обрабатываем нажатие на кнопку "Вернуться в Меню 1"
    elif call.data == 'back_menu2':
        bot.edit_message_media(chat_id=call.message.chat.id,
                               message_id=call.message.message_id,
                               media=telebot.types.InputMedia(type='photo', media=open('imgaes.jpg', 'rb')),
                               reply_markup=main_menu())    # Обрабатываем нажатие на кнопку "Вернуться в Меню 1"

    # Обрабатываем нажатие на кнопку "Вернуться в Меню 1"
    elif call.data == 'back_stop':
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_photo(call.message.chat.id, photo=open('imgaes.jpg', 'rb'),
                       caption="Привет, ibotik!\nДобро пожаловать в бот\n🌴 услуги Гоа 🌴\nЗдесь ты можешь:\n"
                               "🎁 Бот постоянно развивается и обновляется, чтобы помочь тебе решить актуальные вопросы легче и быстрее! 🎁\n",
                       reply_markup=main_menu())


    ############################################# Выбор услуг #############################################
    elif call.data == 'view_job_0':
        # ссылка на телеграм канал  0 - индекс в массиве
        UserDataDBs.data_list = global_list(0)[0]
        UserDataDBs.data_url = global_list(0)[1]
        UserDataDBs.counts = global_list(0)[2]
        if UserDataDBs.counts == 0:
            bot.answer_callback_query(callback_query_id=call.id, text='Данная категория пуста')
        else:
            bot.edit_message_media(chat_id=call.message.chat.id,
                                   message_id=call.message.message_id,
                                   media=telebot.types.InputMedia(type='photo', caption=UserDataDBs.data_list[0],
                                                                  media=open('imgaes.jpg', 'rb')),
                                   reply_markup=create_inline_keyboard(0, UserDataDBs.data_list, UserDataDBs.counts,
                                                                       UserDataDBs.data_url))

    elif call.data == 'view_job_1':
        # ссылка на телеграм канал db_tables - массив с табилцами, 1 - индекс в массиве
        UserDataDBs.data_list = global_list(1)[0]
        UserDataDBs.data_url = global_list(1)[1]
        UserDataDBs.counts = global_list(1)[2]
        if UserDataDBs.counts == 0:
            bot.answer_callback_query(callback_query_id=call.id, text='Данная категория пуста')
        else:
            bot.edit_message_media(chat_id=call.message.chat.id,
                                   message_id=call.message.message_id,
                                   media=telebot.types.InputMedia(type='photo', caption=UserDataDBs.data_list[0],
                                                                  media=open('imgaes.jpg', 'rb')),
                                   reply_markup=create_inline_keyboard(0, UserDataDBs.data_list, UserDataDBs.counts, UserDataDBs.data_url))

    elif call.data == 'view_job_2':
        # ссылка на телеграм канал db_tables - массив с табилцами, 2 - индекс в массиве
        UserDataDBs.data_list = global_list(2)[0]
        UserDataDBs.data_url = global_list(2)[1]
        UserDataDBs.counts = global_list(2)[2]
        if UserDataDBs.counts == 0:
            bot.answer_callback_query(callback_query_id=call.id, text='Данная категория пуста')
        else:
            bot.edit_message_media(chat_id=call.message.chat.id,
                                   message_id=call.message.message_id,
                                   media=telebot.types.InputMedia(type='photo', caption=UserDataDBs.data_list[0],
                                                                  media=open('imgaes.jpg', 'rb')),
                                   reply_markup=create_inline_keyboard(0, UserDataDBs.data_list, UserDataDBs.counts, UserDataDBs.data_url))

    ############################################# Разместить услуг ##########################################################################################

    elif call.data == 'create_job_0':
        db_tables_index = 0
        bot.answer_callback_query(callback_query_id=call.id)
        bot.send_message(chat_id=call.message.chat.id, text="Форма заполнения данных\nВведите Ваше имя:",
                         reply_markup=send_user_data_form(call.message, db_tables_index))  # отправка сообщения

    elif call.data == 'create_job_1':
        db_tables_index = 1
        bot.answer_callback_query(callback_query_id=call.id)
        bot.send_message(chat_id=call.message.chat.id, text="Форма заполнения данных\nВведите Ваше имя:",
                         reply_markup=send_user_data_form(call.message, db_tables_index))  # отправка сообщения

    elif call.data == 'create_job_2':
        db_tables_index = 2
        bot.answer_callback_query(callback_query_id=call.id)
        bot.send_message(chat_id=call.message.chat.id, text="Форма заполнения данных\nВведите Ваше имя:",
                         reply_markup=send_user_data_form(call.message, db_tables_index))  # отправка сообщения


    ############################################# Кнопки туда сюда ##########################################################################################

    elif call.data == 'previous':

        index = UserDataDBs.data_list.index(call.message.caption) - 1
        bot.edit_message_media(chat_id=call.message.chat.id,
                               message_id=call.message.message_id,
                               media=telebot.types.InputMedia(type='photo', caption=UserDataDBs.data_list[index],
                                                              media=open('imgaes.jpg', 'rb')),
                               reply_markup=create_inline_keyboard(index, UserDataDBs.data_list, UserDataDBs.counts,
                                                                   UserDataDBs.data_url))

    elif call.data == 'next':
        index = UserDataDBs.data_list.index(call.message.caption) + 1
        bot.edit_message_media(chat_id=call.message.chat.id,
                               message_id=call.message.message_id,
                               media=telebot.types.InputMedia(type='photo', caption=UserDataDBs.data_list[index],
                                                              media=open('imgaes.jpg', 'rb')),
                               reply_markup=create_inline_keyboard(index, UserDataDBs.data_list, UserDataDBs.counts,
                                                                   UserDataDBs.data_url))

    elif call.data == 'pass_l':
        index = UserDataDBs.data_list.index(call.message.caption) + int(len(UserDataDBs.data_list) - 1)
        bot.edit_message_media(chat_id=call.message.chat.id,
                               message_id=call.message.message_id,
                               media=telebot.types.InputMedia(type='photo', caption=UserDataDBs.data_list[index],
                                                              media=open('imgaes.jpg', 'rb')),
                               reply_markup=create_inline_keyboard(index, UserDataDBs.data_list, UserDataDBs.counts,
                                                                   UserDataDBs.data_url))

    elif call.data == 'pass_r':
        index = UserDataDBs.data_list.index(call.message.caption) * 0
        bot.edit_message_media(chat_id=call.message.chat.id,
                               message_id=call.message.message_id,
                               media=telebot.types.InputMedia(type='photo', caption=UserDataDBs.data_list[index],
                                                              media=open('imgaes.jpg', 'rb')),
                               reply_markup=create_inline_keyboard(index, UserDataDBs.data_list, UserDataDBs.counts,
                                                                   UserDataDBs.data_url))
    ############################################# submenu3слайдер ##########################################################################################

    # Обрабатываем нажатие на кнопку Меню 1
    elif call.data == 'submenu1':
        # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Вы выбрали Подменю 1.1', reply_markup=create_submenu1())
        bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               media=telebot.types.InputMedia(type='photo', caption='Вы выбрали Катеогрия 1',
                                                              media=open('imgaes.jpg', 'rb')),
                               reply_markup=menu_back())

    elif call.data == 'submenu2':
        # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Вы выбрали Подменю 1.2')
        bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               media=telebot.types.InputMedia(type='photo', caption='Вы выбрали Катеогрия 2',
                                                              media=open('imgaes.jpg', 'rb')),
                               reply_markup=menu_back())

    elif call.data == 'submenu3':
        # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Вы выбрали Подменю 1.2')
        bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               media=telebot.types.InputMedia(type='photo', caption='Вы выбрали Катеогрия 3',
                                                              media=open('imgaes.jpg', 'rb')),
                               reply_markup=create_submenu1())

    elif call.data == 'commands':
        # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Вы выбрали Подменю 1.2')
        bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               media=telebot.types.InputMedia(type='photo', caption='Полный список команд:\n '
                                                                                    '🏝 Запуск бота -> /start\n'
                                                                                    '🔍Открыть меню: -> /menu\n'
                                                                                    '📒 Каталог услуг  -> /services\n'
                                                                                    '🔍 Поиск по ключевым словам -> /search\n'
                                                                                    '🙌🏽 Публикация услуги ->  /offer\n' 
                                                                                    '💭 Обратная связь -> /feedback\n'
                                                                                    '📣 Список команд -> /commands\n'
                                                                                    ,media=open('imgaes.jpg', 'rb')),
                               reply_markup=menu_back2())


    # Обрабатываем нажатие на кнопку Подменю 1.1
    elif call.data == 'subsubmenu1':
        bot.send_message(call.message.chat.id, 'Вы выбрали Подменю 1.1.1')

    elif call.data == 'subsubmenu2':
        bot.send_message(call.message.chat.id, 'Вы выбрали Подменю 1.1.2')


# @bot.message_handler(content_types=['text'])
# def message_reply(message):
#     bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
#     pass


############################                                                ######################################################
############################ Создаем функцию, которая обрабатывает команды  ######################################################
############################                                                ######################################################


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Привет, ibotik!\nДобро пожаловать в бот\n🌴 услуги Гоа 🌴\nЗдесь ты можешь:\nМного чего и список\nОткрыть меню: /menu"
                     "🎁 Бот постоянно развивается и обновляется, чтобы помочь тебе решить актуальные вопросы легче и быстрее! 🎁\n")


@bot.message_handler(commands=['menu'])
def help_command(message):
    bot.send_photo(message.chat.id, photo=open('imgaes.jpg', 'rb'),
                   caption="🌴Раздел меню🌴\n🎁Здесь ты можешь выбрать \nразделы интересующие тебя🎁",
                   reply_markup=main_menu())

@bot.message_handler(commands=['services'])
def help_command(message):
    bot.send_photo(message.chat.id, photo=open('imgaes.jpg', 'rb'),
                   caption="🌴Раздел Услуг🌴\n🎁Здесь ты можешь выбрать \nинтересующие тебя услуги🎁",
                   reply_markup=main_submenu1_view())


@bot.message_handler(commands=['offer'])
def help_command(message):
    bot.send_photo(message.chat.id, photo=open('imgaes.jpg', 'rb'),
                   caption="🌴Раздел меню🌴\n🎁Здесь ты можешь разместить \nинтересующие тебя услуги🎁",
                   reply_markup=main_submenu2_view())



@bot.message_handler(commands=['feedback'])
def help_command(message):
    bot.send_photo(message.chat.id, photo=open('imgaes.jpg', 'rb'),
                   caption="✨ Мы рады обратной связи.✨ \nНапиши нам, чтобы задать вопрос \nили предложить обновление ✨",
                   reply_markup=main_feedback())

@bot.message_handler(commands=['search'])
def help_command(message):
    bot.send_photo(message.chat.id, photo=open('imgaes.jpg', 'rb'),
                   caption="\n✨Ты можешь использовать одно или больше слов для поиска✨ \n"
                           "✨ Отправь сообщение с ключевыми словами без знаков препинания, и я найду для тебя подходящие объявления ✨",
                   reply_markup=menu_back2())

@bot.message_handler(commands=['commands'])
def help_command(message):
    bot.send_photo(message.chat.id, photo=open('imgaes.jpg', 'rb'),
                   caption='Полный список команд:\n '
                        '🏝 Запуск бота -> /start\n'
                        '🔍Открыть меню: -> /menu\n'
                        '📒 Каталог услуг  -> /services\n'
                        '🔍 Поиск по ключевым словам -> /search\n'
                        '🙌🏽 Публикация услуги ->  /offer\n' 
                        '💭 Обратная связь -> /feedback\n'
                        '📣 Список команд -> /commands\n',
                   reply_markup=menu_back2())



# Запускаем бота
bot.polling(none_stop=True)

# bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                        media=telebot.types.InputMedia(type='photo',caption='Введите имя:' , media=open('imgaes.jpg', 'rb')), reply_markup=send_user_data_form(call.message.chat.id))
# bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
