import sqlalchemy
from .db_session import SqlAlchemyBase


class InterestingPlaces(SqlAlchemyBase):
    __tablename__ = 'interesting_places'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    address = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
