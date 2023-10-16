from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import pydantic_types as types
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


# _____ CRUD SECTION _____ #
app = FastAPI()


# _____ CREATE _____:
# creating person information including his/her car and property details:
@app.post("/create_person")
async def create_person(info: types.CreatePerson, db: db_dependency):
    car = modules.Car(
        model=info.car.model, color=info.car.color, has_damage=info.car.has_damage
    )
    db.add(car)
    db.commit()
    property = modules.Property(
        floor=info.property.floor, square=info.property.square)
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
    db.refresh(person)

    return "Success"

# creating car


@app.post("/create_car")
async def create_car(info: types.CreateCar, db: db_dependency):
    car = modules.Car(model=info.model, color=info.color,
                      has_damage=info.has_damage)
    db.add(car)
    db.commit()
    db.refresh(car)


# _____ READING _____:
@app.get("/get_person/{name}")
async def get_person(name: str, db: db_dependency):
    person = db.query(modules.Person).filter(
        modules.Person.name == name).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person was not found")
    else:
        car = db.query(modules.Car).filter(
            modules.Car.id == person.car_id).first()
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


# _____ DELETION _____:
@app.delete("/delete_person/{id}")
async def delete_by_id(id: int, db: db_dependency):
    one = db.query(modules.Person).filter(modules.Person.id == id).first()
    db.delete(one)
    db.commit()
    return "success"


# _____ UPDATE _____:
# updating car details:
@app.post("/update_car/{owner}")
async def update_car(
    owner: str, info: types.CreateCar, db: db_dependency
):
    person = db.query(modules.Person).filter(
        modules.Person.name == owner).first()
    if not person:
        raise HTTPException(
            status_code=404, detail="Such owner does not exist")
    else:
        car = db.query(modules.Car).filter(
            modules.Car.id == person.car_id).first()
        car.model = info.model
        car.color = info.color
        car.has_damage = info.has_damage
        db.commit()
        db.refresh(car)
        return "success"


# updating person details:
@app.post("/update_person/{id}")
async def update_person(id: int, info: types.CreatePerson, db: db_dependency):
    person = db.query(modules.Person).filter(
        modules.Person.id == id).first()
    if not person:
        raise HTTPException(
            status_code=404, detail="Person by such ID does not exist")
    else:
        person.name = info.name
        person.age = info.age
        person.married = info.married
        db.commit()
        db.refresh(person)
        return "Success"


# updating properties details based on their owners:
@app.post("/update_properties/{owner}")
async def update_property(info: types.CreateProperty, owner: str, db: db_dependency):
    person = db.query(modules.Person).filter(
        modules.Person.name == owner).first()
    if not person:
        raise HTTPException(
            status_code=404, detail="Such Owner does not exist")
    else:
        property = db.query(modules.Property).filter(
            modules.Property.id == person.property_id).first()
        property.floor = info.floor
        property.square = info.square
        db.commit()
        db.refresh(property)
        return "Success"
