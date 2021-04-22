import sqlalchemy
from .db_session import SqlAlchemyBase


class Parks(SqlAlchemyBase):
    __tablename__ = 'parks'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    address = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
