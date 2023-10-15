from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Annotated
import modules
from db_setup import engine, SessionLocal


# _____ DATABASE SECTION _____ #
modules.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# _____ PYDANTIC TYPE SECTION _____ #


# Type definitions for Car:
class CreateCar(BaseModel):
    model: str
    color: str
    has_damage: bool


# Type definitions for Car:
class CreateProperty(BaseModel):
    floor: int
    square: str


# Type definitions for Person:
class CreatePerson(BaseModel):
    name: str
    age: int
    married: bool
    car: CreateCar
    property: CreateProperty


# _____ END POINTS SECTION _____ #
app = FastAPI()


# creating tables api:
@app.post("/person_info")
async def create_person(info: CreatePerson, db: db_dependency):
    car = modules.Car(
        model=info.car.model, color=info.car.color, has_damage=info.car.has_damage
    )
    db.add(car)
    db.commit()
    property = modules.Property(floor=info.property.floor, square=info.property.square)
    db.add(property)
    db.commit()
    person = modules.Person(
        name=info.name,
        age=info.age,
        married=info.married,
        car_id=car.id,
        property_id=property.id,
    )
    db.add(person)
    db.commit()

    return "Success"


@app.get("/get_by_id/{name}")
async def get_person_by_id(name: str, db: db_dependency):
    person = db.query(modules.Person).filter(modules.Person.name == name).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person was not found")
    else:
        car = db.query(modules.Car).filter(modules.Car.id == person.car_id).first()
        property = (
            db.query(modules.Property)
            .filter(modules.Property.id == person.property_id)
            .first()
        )
        output = {
            "name": person.name,
            "age": person.age,
            "married": person.married,
            "car": car,
            "property": property,
        }
        return output
