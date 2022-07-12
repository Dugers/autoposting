from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


groups_menu_keyboard = InlineKeyboardMarkup()
add_group_button = InlineKeyboardButton("Добавить группу", callback_data="add_group")
delete_group_button = InlineKeyboardButton("Удалить группу", callback_data="del_group")
groups_menu_keyboard.add(add_group_button)
full_groups_menu_keyboard = InlineKeyboardMarkup(row_width=1)
full_groups_menu_keyboard.add(add_group_button, delete_group_button)

cancel_keyboard = InlineKeyboardMarkup()
cancel_button = InlineKeyboardButton("Отмена", callback_data="cancel")
cancel_keyboard.add(cancel_button)

post_edit_menu_keyboard = InlineKeyboardMarkup()
add_text_button = InlineKeyboardButton("✏️ Добавить текст ✏️", callback_data="edit_add_text")
edit_photo_button = InlineKeyboardButton("🖼️ Удалить фото/видео и добавить свои 🖼️", callback_data="edit_del_and_add_media")
edit_video_button = InlineKeyboardButton("📷 Добавить фото/видео 📷", callback_data="edit_add_media")
del_post_button = InlineKeyboardButton("❌ Не постить ❌", callback_data="del_post")
publish_post_button = InlineKeyboardButton("✔️ Запостить ✔️", callback_data="publish_post")
cancel_publish_post_button = InlineKeyboardButton("🗙 Отменить добавление постов 🗙", callback_data="cancel_publish_post")
post_edit_menu_keyboard.row(add_text_button).row(edit_photo_button).row(edit_video_button).row(del_post_button, publish_post_button).row(cancel_publish_post_button)

send_photo_video_keyboard = InlineKeyboardMarkup()
ready_photo_video_button = InlineKeyboardButton("Всё", callback_data="ready_add_photo_video")
send_photo_video_keyboard.add(ready_photo_video_button, cancel_button)

cancel_or_none_text_keyboard = InlineKeyboardMarkup()
none_text_button = InlineKeyboardButton("Сделать без текста", callback_data="none_text")
cancel_or_none_text_keyboard.add(none_text_button, cancel_button)

channels_keyboard = InlineKeyboardMarkup()
add_channel_button = InlineKeyboardButton("Добавить канал", callback_data="add_channel")
del_channel_button = InlineKeyboardButton("Удалить канал", callback_data="del_channel")
channels_keyboard.add(add_channel_button)
full_channels_keyboard = InlineKeyboardMarkup()
full_channels_keyboard.add(add_channel_button, del_channel_button)

channel_return = InlineKeyboardMarkup().add(InlineKeyboardButton("Вернуться обратно", callback_data="channel_return"))

autoposting_enabled_keyboard = InlineKeyboardMarkup()
autoposting_disabled_keyboard = InlineKeyboardMarkup()
autoposting_settings_button = InlineKeyboardButton("Настройки", callback_data="autoposting_settings")
autoposting_enable_button = InlineKeyboardButton("Включить", callback_data="autoposting_enable")
autoposting_disable_button = InlineKeyboardButton("Выключить", callback_data="autoposting_disable")
autoposting_enabled_keyboard.add(autoposting_settings_button, autoposting_disable_button)
autoposting_disabled_keyboard.add(autoposting_settings_button, autoposting_enable_button)

autoposting_settings_keyboard = InlineKeyboardMarkup()
autoposting_settings_channels = InlineKeyboardButton("Обновить список каналов", callback_data="autoposting_settings_channels")
autoposting_settings_timeout = InlineKeyboardButton("Изменить тамймаут", callback_data="autoposting_settings_timeout")
autoposting_settings_return = InlineKeyboardButton("Вернуться обратно", callback_data="autoposting_settings_return")
autoposting_settings_keyboard.row(autoposting_settings_channels).row(autoposting_settings_timeout).row(autoposting_settings_return)

autoposting_settings_channels_keyboard = InlineKeyboardMarkup()
autoposting_settings_channels_ready = InlineKeyboardButton("Всё", callback_data="autoposting_channels_ready")
autoposting_settings_channels_keyboard.row(autoposting_settings_channels_ready).row(cancel_button)