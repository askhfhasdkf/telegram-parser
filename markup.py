from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


menu_start = InlineKeyboardMarkup(row_width=1)
button = InlineKeyboardButton(
    text='приложение', callback_data='link'
)
button3 = InlineKeyboardButton(
    text='рассылка', callback_data='sendall'
)
menu_start.insert(button)
menu_start.insert(button3)


spam_menu = InlineKeyboardMarkup(row_width=2)
button1 = InlineKeyboardButton(
    text='создать аккаунт', callback_data='spam'
)
button2 = InlineKeyboardButton(
    text='запустить', callback_data='start'
)
button4 = InlineKeyboardButton(
    text='добавить чат', callback_data='add_chat'
)
spam_menu.insert(button1)
spam_menu.insert(button2)
spam_menu.insert(button4)
