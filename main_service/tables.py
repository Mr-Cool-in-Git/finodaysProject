import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'

    id = sa.Column(sa.Integer, primary_key=True)
    kind = sa.Column(sa.String)
    amount = sa.Column(sa.Numeric(10, 2))
    description = sa.Column(sa.String, nullable=True)

class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    login = sa.Column(sa.String)
    password = sa.Column(sa.String)
    name = sa.Column(sa.String)
    token = sa.Column(sa.String)
    green_bank_id = sa.Column(sa.Integer)
    yellow_bank_id = sa.Column(sa.Integer)
    red_bank_id = sa.Column(sa.Integer)

class Budget(Base):
    __tablename__ = 'budgets'

    id = sa.Column(sa.Integer, primary_key=True)
    amount = sa.Column(sa.Numeric(10, 2))
    f1 = sa.Column(sa.Integer)
    f2 = sa.Column(sa.Integer)