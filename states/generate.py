from aiogram.fsm.state import State, StatesGroup


class GenerateStates(StatesGroup):
    waiting_description = State()
    waiting_style = State()
    waiting_color = State()
    waiting_shape = State()
