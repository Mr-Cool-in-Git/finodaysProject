import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'

    id = sa.Column(sa.Integer, primary_key=True)
    number = sa.Column(sa.String)
    id_client = sa.Column(sa.Integer)
    type = sa.Column(sa.String)
    amount = sa.Column(sa.Numeric(10, 2))

class History(Base):
    __tablename__ = 'histories'

    id = sa.Column(sa.Integer, primary_key=True)
    id_client = sa.Column(sa.Integer)
    id_account = sa.Column(sa.Integer)
    date = sa.Column(sa.Date)
    amount = sa.Column(sa.Numeric(10, 2))
    income = sa.Column(sa.Boolean)
    payment_kind = sa.Column(sa.String)
    second_account = sa.Column(sa.String)

class Client(Base):
    __tablename__ = 'clients'

    id = sa.Column(sa.Integer, primary_key=True)
    login = sa.Column(sa.String)
    password = sa.Column(sa.String)