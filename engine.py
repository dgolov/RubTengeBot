import os
import re

from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from model import Answer, User, Category, Cost


class EngineSessionFactory:
    """ Класс для обработки сессии SQLAlchemy. """
    def __init__(self, uri):
        engine = create_engine(uri, encoding='utf-8', echo=False)
        self.session_factory = sessionmaker(bind=engine, autocommit=False)
        self.session = scoped_session(self.session_factory)

    def get_user_by_telegram_id(self, telegram_id):
        """ Получить пользователя по telegram_id """
        with self.session() as session:
            ret = session.query(User).filter_by(telegram_id=telegram_id).first()
        return ret

    def create_new_user(self, message) -> None:
        """ Внести нового пользователя в базу данных """
        user = User(name=message.from_user.username, telegram_id=int(message.from_user.id))
        with self.session() as session:
            try:
                session.add(user)
                session.commit()
            except Exception as e:
                raise

    def get_all_categories(self) -> list:
        """ Получения списка всех категорий расходов """
        with self.session() as session:
            ret = session.query(Category).all()
        return ret

    def get_category_by_slug(self, slug):
        """ Получение категории по ключу """
        with self.session() as session:
            ret = session.query(Category).filter_by(slug=slug).first()
        return ret

    def check_category(self, text):
        """ Вычисление актуальной категории из текста сообщения """
        categories = self.get_all_categories()
        other = None

        for item_category in categories:
            if text.lower() in item_category.name.lower() or match_intent(item_category.pattern, text):
                return item_category
            if 'other' in item_category.slug:
                other = item_category
        return other

    def set_cost(self, user_id, data) -> None:
        """ Занести расход в базу данных """
        category_data = data.get('category')
        user = self.get_user_by_telegram_id(user_id)
        category = self.get_category_by_slug(category_data) if category_data.startswith('category') \
            else self.check_category(category_data)

        cost = Cost(
            user_id=user.id,
            category_id=category.id,
            sum_rub=data.get('sum_rub'),
            sum_tng=data.get('sum_tng'),
            date=datetime.utcnow() + timedelta(hours=6),
            test=True if int(os.environ.get('DEBUG')) else False
        )
        with self.session() as session:
            try:
                session.add(cost)
                session.commit()
            except Exception as e:
                raise

    def get_answer_list(self, type_answer) -> list:
        """ Получение ответов по ключу """
        with self.session() as session:
            ret = session.query(Answer).filter_by(type=type_answer).all()
        return ret

    def get_statistics(self, telegram_user_id: int, period: dict = None) -> dict:
        """ Получение статистики
        :param telegram_user_id: id пользователя телеграм
        :param period: период отчета
        :return: кортеж из суммы в тенге и суммы в рублях
        """
        categories_dict = {}
        statistics = {
            'total': {
                'tng_sum': 0,
                'rub_sum': 0,
            },
            'categories': {}
        }
        with self.session() as session:
            user = self.get_user_by_telegram_id(telegram_id=telegram_user_id)
            categories = self.get_all_categories()
            for category in categories:
                categories_dict[category.id] = category.name

            cost_query = session.query(Cost).filter_by(user_id=user.id)

            if not int(os.environ.get('DEBUG')):
                print(1)
                cost_query = cost_query.filter_by(test=False)

            if period:
                cost_query = cost_query.filter(Cost.date >= period.get('start'), Cost.date <= period.get('end')).all()
            else:
                cost_query = cost_query.all()
            for cost in cost_query:
                statistics['total']['tng_sum'] += cost.sum_tng
                statistics['total']['rub_sum'] += cost.sum_rub
                if not statistics['categories'].get(categories_dict[cost.category_id], None):
                    statistics['categories'][categories_dict[cost.category_id]] = {
                        'tng_sum': cost.sum_tng,
                        'rub_sum': cost.sum_rub,
                    }
        return statistics


def match_intent(pattern, text):
    """ Check patterns """
    result = re.match(rf'{pattern}', text)
    return result is not None