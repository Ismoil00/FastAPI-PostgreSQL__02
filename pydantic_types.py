from pydantic import BaseModel


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