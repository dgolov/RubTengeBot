from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMExpend(StatesGroup):
    """ Cost states class """
    sum = State()
    category = State()


class FSMStatistic(StatesGroup):
    """ Statistic states class """
    start = State()
