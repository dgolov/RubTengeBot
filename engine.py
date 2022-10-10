from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from model import User


class EngineSessionFactory:
    """ Класс для обработки сессии SQLAlchemy. """
    def __init__(self, uri):
        engine = create_engine(uri, encoding='utf-8', echo=False)
        self.session_factory = sessionmaker(bind=engine, autocommit=False)
        self.session = scoped_session(self.session_factory)

    def get_user_by_telegram_id(self, telegram_id):
        with self.session() as session:
            ret = session.query(User).filter_by(telegram_id=telegram_id).first()
        return ret

    def create_new_user(self, message):
        user = User(name=message.from_user.username, telegram_id=int(message.from_user.id))
        with self.session() as session:
            try:
                session.add(user)
                session.commit()
            except Exception as e:
                raise
