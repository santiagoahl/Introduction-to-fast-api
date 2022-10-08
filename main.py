# Comando para inicializar la api  uvicorn main:app --reload
# --reload es un comando que nos permite visualizar los cambios en la api de forma automatica, sin la necesidad de recargar
#Python
from doctest import Example
from typing import Optional#Ver curso profesional de python, optional general path queries opcionales
from enum import Enum #Crear enumeraciones de strings

#from pydantic import BaseModel
from pydantic import BaseModel, EmailStr, HttpUrl, PaymentCardNumber

#FastAPI
from fastapi import FastAPI
from fastapi import Body #Permite decir que un parametro en el Op function es body
app = FastAPI()

#Models validation
from pydantic import Field

#Models

class HairColor(str, Enum):
    white = "white"
    black = "black"
    brown = "brown"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Dortmund"
        )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Renania del Norte-Westfalia"
        )
    country: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Alemania"
        )

class Person(BaseModel): #Herencia de base models
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Santiago"
        ) #Sintaxis de tipado en python
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Ahumada"
        )
    age: int = Field(
        ...,
        ge=1,
        le=115,
        example=21
        )
    hair_color: Optional[HairColor] = Field(default=None,example="black") #Valor por defecto, mismo Null
    is_married: Optional[bool] = Field(default_factory=None, example=False)
    email: EmailStr = Field(
        ...,
        )
    card_number: PaymentCardNumber = Field(
        ...,
        )
    twitter_profile_link: HttpUrl = Field(
        ...,
        )
    #class Config:
     #   schema_extra = {
     #       "example": {
      #          "first_name": "Santiago",
       #         "last_name": "Ahumada Lozano",
        #        "age": 21,
         #       "hair_color": "black",
          #      "is_married": False
           # }
       # }
    #Swagger pide que haya un example llamado "example"


@app.get('/') 
def home():
    return {"Hello":"World"}


#Request and Response Body

@app.post("/person/new")

def create_person(person: Person = Body(...)): #... significa que un parametro o atributo es obligatorio, : es tipado estatico
    return person

#Validaciones: Query Parameters

from fastapi import Query

path = "/person/detail"
@app.get(path) 

    #Agregamos nuestro primer QP

def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name, it's between 1 and 50 characters",
        example="Natalia"
        ), #pues es QP
    age: Optional[str] = Query(
        ...,
        title="Person Age",
        description="This is the person age, it's required",
        example="21"
        ) #Este QP es obligatorio, pero normalmente deberia ser PP
):
    return {name:age}

#Validaciones: Path Parameters

from fastapi import Path

@app.get(path+"/{person_id}") #Si hay 2 endpoints iguales, siempre es tomado el ultimo

def show_person(
    person_id: int = Path(
        ...,
        ge=1,
        title="Person ID",
        description="This is the person id, it's required",
        example=123
        ) #Podemos obligar a pasar ids >1
):
    return {person_id: "It exists!"}

#Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123
    ),
    person: Person = Body(...),#Asociado a la clase que ya definimos
    location: Location = Body(...) #Combinamos 2 JSON, hay que especificar como hacerlo:
):
    results = person.dict()
    results.update(location) #Unir diccionarios
    return results
    #return Person
