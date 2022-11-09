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

    login = sa.Column(sa.String, primary_key=True)
    password = sa.Column(sa.String)

class Budget(Base):
    __tablename__ = 'budgets'

    id = sa.Column(sa.Integer, primary_key=True)
    amount = sa.Column(sa.Numeric(10, 2))
    f1 = sa.Column(sa.Integer)
    f2 = sa.Column(sa.Integer)