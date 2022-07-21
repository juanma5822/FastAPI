from enum import Enum
from pydantic import BaseModel
from pydantic import Field,EmailStr
from typing import Optional

class Hair_color(Enum):
    white= "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"
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