from sqlalchemy import create_engine, Table, Column, Integer, String, Text, MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import sys
sys.path.append('..')
from common.variables import *
import datetime


class ClientDatabase:
    """
    Класс - оболочка для работы с базой данных клиента.
    Использует SQLite базу данных, реализован с помощью
    SQLAlchemy ORM. Используется классический подход.
    """
    Base = declarative_base()

    class KnownUsers(Base):
        '''
        Класс - отображение таблицы зарегистрировнных пользователей.
        '''
        __tablename__ = 'known_users'
        id = Column(Integer, primary_key=True)
        username = Column(String)

        def __init__(self, username):
            self.username = username

    class MessageHistory(Base):
        '''
        Класс - отображение для таблицы истории переданных сообщений.
        '''
        __tablename__ = 'message_history'
        id = Column(Integer, primary_key=True)
        from_user = Column(String)
        to_user = Column(String)
        message = Column(Text)
        date = Column(DateTime)

        def __init__(self, from_user, to_user, message):
            self.from_user = from_user
            self.to_user = to_user
            self.message = message
            self.date = datetime.datetime.now()

    class Contacts(Base):
        '''
        Класс - отображение для таблицы контактов.
        '''
        __tablename__ = 'contacts'
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)

        def __init__(self, contact):
            self.name = contact

    def __init__(self, name):
        path = os.path.dirname(os.path.realpath(__file__))
        filename = f'client_{name}.db3'
        self.engine = create_engine(f'sqlite:///{os.path.join(path, filename)}', echo=False, pool_recycle=7200,
                                    connect_args={'check_same_thread': False})

        self.Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.session.query(self.Contacts).delete()
        self.session.commit()

    def add_contact(self, contact):
        """ Метод добавляющий контакт в базу данных. """
        if not self.session.query(self.Contacts).filter_by(name=contact).count():
            contact_row = self.Contacts(contact)
            self.session.add(contact_row)
            self.session.commit()

    def del_contact(self, contact):
        """ Метод, очищающий таблицу со списком контактов. """
        self.session.query(self.Contacts).filter_by(name=contact).delete()
        self.session.commit()

    def add_users(self, users_list):
        """ Метод, заполняющий таблицу известных пользователей. """
        self.session.query(self.KnownUsers).delete()
        for user in users_list:
            new_user = self.KnownUsers(user)
            self.session.add(new_user)
        self.session.commit()

    def save_message(self, from_user, to_user, message):
        """ Метод, сохраняющий сообщение в базе данных. """
        new_message = self.MessageHistory(from_user, to_user, message)
        self.session.add(new_message)
        self.session.commit()

    def get_contacts(self):
        """ Метод, возвращающий список всех контактов. """
        return [contact[0] for contact in self.session.query(self.Contacts.name).all()]

    def get_users(self):
        """ Метод возвращающий список всех известных пользователей. """
        return [user[0] for user in self.session.query(self.KnownUsers.username).all()]

    def check_user(self, user):
        """ Метод, проверяющий существование пользователя. """
        if self.session.query(self.KnownUsers).filter_by(username=user).count():
            return True
        else:
            return False

    def check_contact(self, contact):
        """ Метод, проверяющий существвование контакта. """
        if self.session.query(self.Contacts).filter_by(name=contact).count():
            return True
        else:
            return False

    def get_history(self, from_user=None, to_user=None):
        """ Метод, возвращающий историю сообщений определенного пользователя. """
        query = self.session.query(self.MessageHistory)
        if from_user:
            query = query.filter_by(from_user=from_user)
        if to_user:
            query = query.filter_by(to_user=to_user)
        return [(history_row.from_user, history_row.to_user, history_row.message, history_row.date)
                for history_row in query.all()]

    def contacts_clear(self):
        """ Метод, очищающий таблицу со списком контактов. """
        self.session.query(self.Contacts).delete()
        self.session.commit()


if __name__ == '__main__':
    test_db = ClientDatabase('test1')
    for i in ['test2', 'Bob', 'Alice']:
        test_db.add_contact(i)
    test_db.add_contact('test2')
    test_db.add_users(['test1', 'Bob', 'Alice', 'Ann', 'test2'])
    test_db.save_message('test1', 'test2', f'Привет! я тестовое сообщение от {datetime.datetime.now()}!')
    test_db.save_message('test2', 'test1', f'Привет! я другое тестовое сообщение от {datetime.datetime.now()}!')
    print(test_db.get_contacts())
    print(test_db.get_users())
    print(test_db.check_user('test1'))
    print(test_db.check_user('test10'))
    print(test_db.get_history('test2'))
    print(test_db.get_history(to_user='test2'))
    print(test_db.get_history('test3'))
    test_db.del_contact('test4')
    print(test_db.get_contacts())
