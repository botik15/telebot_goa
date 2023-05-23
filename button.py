from telebot import types
from connect import select_db, db_tables


# Создаем начальное меню
def main_menu():
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='📒 Выбрать услугу 📒', callback_data='main_submenu1_view_button_1'))
    menu.add(types.InlineKeyboardButton(text='🙌🏽 Разместить услугу 🙌🏽', callback_data='main_submenu1_view_button_2'))
    # menu.add(types.InlineKeyboardButton(text='🎁 Найти услугу по ключевым словам 🎁', callback_data='main_submenu1_view_button_3'))
    # menu.add(types.InlineKeyboardButton(text='🏝 Узнать лайфхаки о подготовке к поездке и жизни в Индии', callback_data='button4'))
    # menu.add(types.InlineKeyboardButton(text='Oформить визу', callback_data='button5'))
    # menu.add(types.InlineKeyboardButton(text='💗 Найти компанию в Гоа', callback_data='button6'))
    # menu.add(types.InlineKeyboardButton(text='🔍 Для просмотра полного списка команд 🔍', callback_data='commands'))
    return menu




# Создаем меню для Меню 1
def main_submenu1_view():
    counts1 = len(select_db(db_tables, 0)[0])
    counts2 = len(select_db(db_tables, 1)[0])
    counts3 = len(select_db(db_tables, 2)[0])
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text=f'Красота, здоровье ({counts1} шт.)', callback_data='view_job_0'))
    menu.add(types.InlineKeyboardButton(text=f'Транспорт, перевозки ({counts2} шт.)', callback_data='view_job_1'))
    menu.add(types.InlineKeyboardButton(text=f'Ремонт и отделка ({counts3} шт.)', callback_data='view_job_2'))
    menu.add(types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='back'))
    return menu


# Создаем меню для Меню 2
def main_submenu2_view():
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='Красота, здоровье', callback_data='create_job_0'))
    menu.add(types.InlineKeyboardButton(text='Транспорт, перевозки', callback_data='create_job_1'))
    menu.add(types.InlineKeyboardButton(text=f'Ремонт и отделка', callback_data='create_job_2'))
    menu.add(types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='back'))
    return menu

def menu_back():
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='Назад', callback_data='back_menu'))
    return menu

def main_feedback():
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='Написать', url=('https://t.me/ibotik')))
    menu.add(types.InlineKeyboardButton(text='Назад', callback_data='back_menu2'))
    return menu

def menu_back2():
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='Назад', callback_data='back_menu2'))
    return menu




# Создаем меню для Меню 2
def main_submenu3_view():
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='Категория меню 3 - 1', callback_data='submenu1'))
    menu.add(types.InlineKeyboardButton(text='Категория меню 3 -  2', callback_data='submenu2'))
    menu.add(types.InlineKeyboardButton(text=f'Категория меню 3 - 3', callback_data='submenu3'))
    menu.add(types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='back'))
    return menu


# Создаем меню для Подменю 1.1
def create_submenu1():
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='Подменю 1.1.1', callback_data='subsubmenu1'))
    menu.add(types.InlineKeyboardButton(text='Подменю 1.1.2', callback_data='subsubmenu2'))
    menu.add(types.InlineKeyboardButton(text='Назад', callback_data='back_menu'))
    return menu

