python is dynamically typed langauge
which can chagne the type of my variable or value during run time
it affects databases 

class person
    name
    age

if people giving age like 15, fifteen it will be an issue
python is not type safe

explain what is typescript in 1-2 sentence

where pydantic comes to picture

import pydantic
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

def create_user(newUser: User):
    print(name , newUser.name  )
    print(age,   newUser.age )

linto = User(
    name = "Li",
    age = 28
)

create_user(linto)

How pydantic helps;
* Helps us to create rigid data models for our input and output
* making our code more error safe
* we can enforce type and data validations

not only field type validation but also data validation is also important as you move towards production

age: int = "five"
here python is not checking anything. 
a plain class is not handling class
class person:
    def __init__:
        self. 
        self.

also dataclass also not solving this problem.
show the above class in dataclass implementation


from pydantic import BaseModel
class UserModel(BaseModel):
    name: str
    age: int = 0  # has a default -> optional

this pydantic acutally solving the problem
automatic type coerstion (only a little bit not aggressive) is a feature "28" will be considered as 28
but "twenty eight" will return an error



now we did type validation next is field validation
from pydantic import BaseModel, Field
class UserModel(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=0, le=100)

anotjher way to get the same output, no benefits, i will prefer second one
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated
class UserModel(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=100)]
    age: Annotated[int, Field(ge=0, le=100)]
    email: EmailStr  # we don't have to use regex, it will regex non-email
    # we can also use Httpstr and SecretStr. we can do this so many items like file or ip everything is we can use pydantic

give me one example eiwh field_validator decorator here and tell me what is the diff between this and field

field_valdiation is only for one field for cross field validation we use model_validator decorator. also give short note with example

computed_field decorator explain this with a short note and example code

# Nedted Models is the next topic
from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin_code: str

class Applicant(BaseModel):
    name: str
    age: int
    address: Address  # a whole model used as field type

this is for os.getenv() problems to solve also write a short note about it and give this code
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    api_key: SecretStr
    max_connections: int = Field(default=100, ge=1, le=1000)
    debug: bool = False

settings = AppSettings()   # reads from .env / environment automatically
print(settings.max_connections, type(settings.max_connections))   # 200 <class 'int'>
print(settings.api_key)                          # ********** (masked)
print(settings.api_key.get_secret_value())       # the real value, on purpose