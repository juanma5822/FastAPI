#Python

from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI, Query
from fastapi import Body,Path

app = FastAPI()

#Models

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None



@app.get("/") # path operation decorator
def home():
    return {"Hello": "World"}

# Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person 


# Validations: Query Parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=25,
        title="Person Name",
        description="This is the person name. It's between 1 and 25 characters"
        ),
    age: Optional[int] = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required"
        )

):
    return {name: age}

#Validations: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This is Person ID. It's required"
        )
):
	return {person_id: "It exist!"}
