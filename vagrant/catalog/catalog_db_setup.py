import os
import sys
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# Database code begins here


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class OutdoorActivity(Base):
    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # Returns object data in JSON
        return{
            'name': self.name,
            'id': self.id,
        }


class Items(Base):
    __tablename__ = 'gear'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    price = Column(String(8))
    description = Column(String(250))
    activity_id = Column(Integer, ForeignKey('activity.id'))
    activity = relationship(OutdoorActivity)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # Returns object data in JSON
        return{
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'id': self.id,
        }

# Database code ends here
engine = create_engine('sqlite:///catalogwithusers.db')
Base.metadata.create_all(engine)
