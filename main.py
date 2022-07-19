#Python

from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, EmailStr, PaymentCardNumber
from pydantic.types import PaymentCardBrand
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import Body,Query,Path

app = FastAPI()

#Models

class Hair_color(Enum):
    white= "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=30,
        example= "Bogota"
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=30,
        example= "Cundinamarca"
    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=30,
        example= "Colombia"
    )

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=25,
        example="Juan"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=25,
        example="Romero"
        )
    age: int = Field(
        ...,
        gt=17,
        le=70,
        example= 28
        )
    email: EmailStr = Field(
        ...,
        title="Email",
        description="here put your email",
        example= "juan@gmail.com"
    )    
    hair_color: Optional[Hair_color] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    

class Payment(BaseModel):
    card_number: PaymentCardNumber = Field(
        ...,
        title="Number Card",
        description="number card credit",
        example= '4915110267441320'
    )

    expiration_mont: int = Field(
        ...,
        gt=0,
        le=12,
        example=8
    )

    expiration_year: int = Field(...,example= 28)

    @property
    def brand_card(self) -> PaymentCardBrand:
        return self.card_number.brand



@app.get("/") # path operation decorator
def home():
    return {"Hello": "World"}

# Request and Response Body

@app.post("/person/new")
def create_person(
    person: Person = Body(...),
    location: Location = Body(...),
    payment: Payment = Body(...)
):
    return {
        "person" : person,
        "location" : location,
        "payment" : {
            "brand": payment.brand_card,
            "last4": payment.card_number.last4,
            "maskk": payment.card_number.masked,
        }
    }
        


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

# Validations: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id:int = Path(
        ...,
        title="Person ID",
        description="This is Person ID",
        gt=0,
        example=45485
    ),
    person: Person = Body(...),
    Location: Location = Body(...)
):
    
    result = person.dict()
    result.update(Location.dict())
    
    return {
        "person_id" : person_id,
        "result" : result
    }
        
    

