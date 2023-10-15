from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from db_setup import Base

# Person Table of PostgreSQL:
class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    age = Column(Integer, nullable=False)
    married = Column(Boolean, default=False)
    car_id = Column(Integer, ForeignKey("car.id"), nullable=True)
    property_id = Column(Integer, ForeignKey("property.id"), nullable=True)


# Car Table of PostgreSQL:
class Car(Base):
    __tablename__ = 'car'

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String(200), nullable=False)
    color = Column(String(200))
    has_damage = Column(Boolean, default=False)

# Property Table of PostgreSQL:
class Property(Base):
    __tablename__ = 'property'

    id = Column(Integer, primary_key=True, index=True)
    floor = Column(Integer, nullable=False)
    square = Column(String, nullable=False)


""" 
{
    "person": {
        "name": "John",
        "age": 22,
        "married": true,
        "car_id": 1,
        "property_id": 1
    },
    "car": {
        "model": "BMW",
        "color": "black",
        "has_damage": true
    },
    "property": {
        "floor": 2,
        "square": "100m2"
    }
} 
"""