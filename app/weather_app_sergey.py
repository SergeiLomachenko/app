from flask import Flask, render_template, jsonify
import requests
import logging
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from datetime import datetime
import time
import schedule
from werkzeug.urls import quote

def connect_to_database():
    max_retries = 5
    retries = 0
    while retries < max_retries:
        try:
            engine = create_engine('mysql+pymysql://sergey:1111@mariadb:3306/weather_sergey?charset=utf8mb4')
            Base.metadata.create_all(engine)
            return engine
        except Exception as e:
            print(f"Не могу достучаться до БД: {e}")
            retries += 1
            time.sleep(5)  
    else:
        print("Невозможно достучаться до БД.")
        return None

time.sleep(10)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True)
    city = Column(String(255))
    temperature = Column(Integer)
    feels_like = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

engine = connect_to_database()

Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

def get_weather():
    try:
        city = 'Минск'
        url = 'https://api.openweathermap.org/data/2.5/weather?q='+quote(city)+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
        weather_data = requests.get(url).json()
        temperature = round(weather_data['main']['temp'])
        temperature_feels = round(weather_data['main']['feels_like'])
        logger.info('Сейчас в городе %s %s°C', city, temperature)
        logger.info('Ощущается как %s°C', temperature_feels)

        # Сохраняем данные в базу данных
        weather_entry = WeatherData(city=city, temperature=temperature, feels_like=temperature_feels)
        with session_scope() as session:
            session.add(weather_entry)
            session.commit()  # Закрываем сессию и сохраняем результаты

    except Exception as e:
        logger.exception("An error occurred:")

schedule.every(1).minutes.do(get_weather)

while True:
    schedule.run_pending()
    time.sleep(1)
