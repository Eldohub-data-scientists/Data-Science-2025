# database.py
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Prediction(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    label = Column(String(10), nullable=False)
    confidence = Column(Float, nullable=False)
    model = Column(String(20), default='CLASSIC')  # NEW
    timestamp = Column(DateTime, default=datetime.utcnow)

def init_db():
    engine = create_engine('sqlite:///predictions.db')
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()