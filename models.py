from datetime import date, datetime
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Text
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class Sample(Base):
    __tablename__ = 'samples'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    category = Column(String(50), default='')
    size = Column(String(10), default='')
    color = Column(String(20), default='')
    status = Column(String(20), default='in')
    borrower = Column(String(100), default='')
    due = Column(String(20), default='')
    created_at = Column(DateTime, default=datetime.now)

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True, autoincrement=True)
    loan_id = Column(String(20), unique=True, nullable=False)
    item_name = Column(String(200), default='')
    borrower_name = Column(String(100), default='')
    loan_type = Column(String(20), default='博主')
    lend_date = Column(String(20), default='')
    due_date = Column(String(20), default='')
    tracking_no = Column(String(50), default='')
    status = Column(String(20), default='active')
    created_at = Column(DateTime, default=datetime.now)

class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    handle = Column(String(100), default='')
    contact_type = Column(String(20), default='博主')
    platform = Column(String(50), default='')
    fans = Column(String(20), default='')
    loan_count = Column(Integer, default=0)
    rating = Column(String(5), default='A')

class Tracking(Base):
    __tablename__ = 'trackings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tracking_no = Column(String(50), nullable=False)
    carrier = Column(String(20), default='')
    from_party = Column(String(100), default='')
    to_party = Column(String(100), default='')
    item_name = Column(String(200), default='')
    status = Column(String(20), default='transit')

def init_db(db_url='sqlite:///yakky.db'):
    engine = create_engine(db_url, echo=False)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    return Session(engine)
