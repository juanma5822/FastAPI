#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, EmailStr, PaymentCardNumber
from pydantic.types import PaymentCardBrand
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body,Query,Path,File, Form, Header,Cookie, UploadFile

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

class PersonBase(BaseModel):
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

class Person(PersonBase):
    password: str = Field(
        ...,
        min_length=8,
        example="hfumkf669"
        )
    
class PersonOut(PersonBase):
    pass    

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

class LoginOut(BaseModel):
    username: str = Field(...,max_length=20)
    message: str = Field(default="Login Succesfully")    

@app.get(path="/",
    status_code=status.HTTP_200_OK,
    tags=["Home"]
    ) # path operation decorator
def home():
    return {"Hello": "World"}

# Request and Response Body

@app.post(path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"]
    )
def create_person(
    person: Person = Body(...,)
    ):
    return person

@app.post(path="/person/new",
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"]
    )
def create_person1(
    person: Person = Body(...,),
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

@app.get(path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
    )
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=25,
        title="Person Name",
        description="This is the person name. It's between 1 and 25 characters",
        example= "Juan"
        ),
    age: Optional[int] = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example=25
        )

):
    return {name: age}

#Validations: Path Parameters

persons = [1, 2, 3, 4, 5]

@app.get(path="/person/detail/{person_id}",
    tags=["Persons"]
    )
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        example=123
        )
): 
    if person_id not in persons: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This person doesn't exist!"
        )
    return {person_id: "It exists!"}

# Validations: Request Body

@app.put(path="/person/{person_id}",tags=["Persons"])
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

#Forms

@app.post(path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Login","Persons"]
)
def login(
    username:str = Form(...),
    password: str = Form(...)
):
    return LoginOut(username = username)

#Cookies and Headers Parameters

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Contact"]    
    )
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
        ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
        ),
    email: EmailStr = Form(...),
    message: str = Form(...,min_length=20),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

@app.post(path="/post-image",tags=["Image"])
def post_image(
    image:UploadFile = File(...)
):
    return {
        "Filename" : image.filename,
        "Format" : image.content_type,
        "Size(kb)" : round(len(image.file.read())/1024,ndigits=2)
    }