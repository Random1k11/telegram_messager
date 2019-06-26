# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
import datetime



Base = declarative_base()

def db_connect():
    return create_engine('sqlite:///telegram_likes.db')

def create_table(engine):
    Base.metadata.create_all(engine)


engine = db_connect()
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()


class LikesTelegram(Base):

    __tablename__ = "likes_telegram"

    id_ = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    message_id = Column(Integer)
    user_id = Column(Integer)
    callback_data = Column(String(20))
    createt_date = Column(DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return self.callback_data



#create_table(engine)


class DataBase:

    def insert_row_to_db(self, values):
        row = LikesTelegram(chat_id=values[0], message_id=values[1], user_id=values[2], callback_data=values[3])
        session.add(row)
        session.commit()

    def get_value_from_db(self, message_id, user_id, value):
        val = getattr(session.query(LikesTelegram).filter(LikesTelegram.message_id == message_id, LikesTelegram.user_id == user_id).first(), value)
        return val

    def get_numbers_of_likes_or_dislikes(self, likes_or_dislikes):
        numbers = session.query(LikesTelegram).filter(LikesTelegram.callback_data == likes_or_dislikes).count()
        return numbers

    def check_existence_row_in_db(self, message_id, user_id):
        return session.query(LikesTelegram).filter(LikesTelegram.message_id == message_id, LikesTelegram.user_id == user_id).first()


    def delete_row_from_db(self, message_id, user_id):
        row = session.query(LikesTelegram).filter(LikesTelegram.message_id == message_id, LikesTelegram.user_id == user_id).delete()
        print('Удаляю!!!!!!!')
        # session.delete(row)
        session.commit()

create_table(engine)
