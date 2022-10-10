from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from helpers import match_intent
from model import User, Category, Cost


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

    def create_new_user(self, message):
        """ Внести нового пользователя в базу данных """
        user = User(name=message.from_user.username, telegram_id=int(message.from_user.id))
        with self.session() as session:
            try:
                session.add(user)
                session.commit()
            except Exception as e:
                raise

    def get_all_categories(self):
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
            if text.lower() in item_category.name.lower() or match_intent(pattern=item_category.pattern, text=text):
                return item_category
            if 'other' in item_category.slug:
                other = item_category
        return other

    def set_cost(self, user_id, data):
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
            date=datetime.utcnow() + timedelta(hours=6)
        )
        with self.session() as session:
            try:
                session.add(cost)
                session.commit()
            except Exception as e:
                raise
