from ast import parse
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
groups_button = KeyboardButton("Список груп")
parse_button = KeyboardButton("Парсинг контента с груп")
create_post_button = KeyboardButton("Добавить новый пост")
channels_button = KeyboardButton("Список каналов")
autoposting_button = KeyboardButton("Автопостинг")
main_menu_keyboard.add(channels_button, groups_button, parse_button, autoposting_button, create_post_button)