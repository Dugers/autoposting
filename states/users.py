from aiogram.dispatcher.filters.state import StatesGroup, State


class GroupState(StatesGroup):
    name_or_id = State()


class PostState(StatesGroup):
    method = State()
    data = State()


class ChannelState(StatesGroup):
    channel_id = State()


class AutopostingState(StatesGroup):
    data = State()