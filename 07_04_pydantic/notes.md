# Pydantic Notes

## Why Do We Need Pydantic?

Python is a **dynamically typed language**.

That means a variable can point to values of different types during runtime.

```python
x = 10
x = "Hello"
x = [1, 2, 3]
```

Python allows this flexibility, but it also means **wrong data types can easily enter your application**, especially when data comes from:

- APIs
- User input
- JSON files
- Databases
- Environment variables

Imagine a user registration form.

```text
Name : Linto
Age  : 15
```

Everything works.

But what if someone sends:

```text
Name : Linto
Age  : fifteen
```

or

```text
Age : "twenty eight"
```

Without validation, this bad data can travel deep into your application and even reach the database.

This is why **type safety** and **data validation** become extremely important in production systems.



# What is TypeScript?

TypeScript is a **statically typed superset of JavaScript** that catches type-related errors during development before the code runs.

Pydantic brings a similar idea to Python by validating data at runtime.



# Plain Python Classes

A normal Python class does **not** validate data.

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


person = Person("Linto", "five")

print(person.age)
```

Output

```text
five
```

Python happily accepts the string.

No validation happens.



# Dataclass Doesn't Solve This Either

Dataclasses remove boilerplate code but still don't validate input types.

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int


person = Person(
    name="Linto",
    age="five"
)

print(person)
```

Output

```text
Person(name='Linto', age='five')
```

Even though `age` is declared as an integer, Python stores a string.

So dataclasses improve readability, **not validation**.



# Where Pydantic Comes Into the Picture

Pydantic creates **rigid data models** that validate incoming data before your program uses it.

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int


def create_user(new_user: User):
    print("Name:", new_user.name)
    print("Age :", new_user.age)


linto = User(
    name="Li",
    age=28
)

create_user(linto)
```

Output

```text
Name: Li
Age : 28
```



# How Pydantic Helps

- Creates rigid input and output models
- Performs automatic type validation
- Performs data validation
- Makes code much safer
- Reduces runtime bugs
- Greatly improves API reliability



# Type Validation

```python
from pydantic import BaseModel

class UserModel(BaseModel):
    name: str
    age: int
```

Valid

```python
UserModel(
    name="Linto",
    age=28
)
```

Invalid

```python
UserModel(
    name="Linto",
    age="twenty eight"
)
```

Output

```text
ValidationError
```



# Automatic Type Coercion

Pydantic performs **limited automatic type coercion**.

Example

```python
UserModel(
    name="Linto",
    age="28"
)
```

Output

```python
age = 28
```

The string `"28"` becomes an integer.

But

```python
UserModel(
    name="Linto",
    age="twenty eight"
)
```

Output

```text
ValidationError
```

Pydantic is helpful, but it is **not aggressively converting everything**.



# Default Values

```python
from pydantic import BaseModel

class UserModel(BaseModel):
    name: str
    age: int = 0
```

Since `age` has a default value, it becomes optional.

```python
UserModel(name="Linto")
```

Output

```python
name='Linto'
age=0
```



# Field Validation

Type validation alone is not enough.

Suppose your API accepts

```python
age = -10
```

It is an integer.

But it is still invalid.

This is where **Field()** comes in.

```python
from pydantic import BaseModel, Field

class UserModel(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100
    )

    age: int = Field(
        ge=0,
        le=100
    )
```

Here

- `ge` → greater than or equal
- `le` → less than or equal

Now

```python
UserModel(
    name="A",
    age=-5
)
```

returns a validation error.



# Annotated Version

The same validation can also be written using `Annotated`.

```python
from typing import Annotated
from pydantic import BaseModel, Field, EmailStr

class UserModel(BaseModel):
    name: Annotated[
        str,
        Field(min_length=2, max_length=100)
    ]

    age: Annotated[
        int,
        Field(ge=0, le=100)
    ]

    email: EmailStr
```

There is no major advantage here for simple models.

Personally, I prefer the previous `Field()` style because it is easier to read.



# Built-in Specialized Types

Pydantic provides many useful data types.

```python
EmailStr
SecretStr
HttpUrl
IPvAnyAddress
FilePath
DirectoryPath
UUID
```

Example

```python
email: EmailStr
```

You don't have to write a regex to validate email addresses.



# field_validator

Sometimes built-in validation isn't enough.

You may need custom validation logic.

```python
from pydantic import BaseModel, field_validator

class UserModel(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if value.lower() == "admin":
            raise ValueError("admin is not allowed")
        return value
```

Now

```python
UserModel(name="admin")
```

Output

```text
ValidationError
```



# Field vs field_validator

| Field() | field_validator |
|----------|----------------|
| Built-in validation | Custom validation |
| Length checks | Business logic |
| Range checks | Complex conditions |
| Regex | Any Python code |
| Faster | More flexible |

Use `Field()` whenever possible.

Use `field_validator()` when built-in validation isn't enough.



# model_validator

`field_validator` validates **one field at a time**.

For validations involving multiple fields, use `model_validator`.

Example:

```python
from pydantic import BaseModel, model_validator

class UserModel(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
```

Here we compare two different fields.

That is impossible using `field_validator`.



# computed_field

Sometimes you don't want users to provide a value.

Instead, you want to compute it automatically.

```python
from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    length: int
    width: int

    @computed_field
    @property
    def area(self) -> int:
        return self.length * self.width


r = Rectangle(length=5, width=10)

print(r.area)
```

Output

```text
50
```

The user never entered `area`.

Pydantic computed it automatically.



# Nested Models

Models can contain other models.

```python
from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin_code: str


class Applicant(BaseModel):
    name: str
    age: int
    address: Address
```

Usage

```python
Applicant(
    name="Linto",
    age=28,
    address={
        "city": "Bangalore",
        "state": "Karnataka",
        "pin_code": "560037"
    }
)
```

Pydantic automatically converts the dictionary into an `Address` object and validates it.



# Managing Environment Variables

Reading environment variables using `os.getenv()` has several problems:

- Everything is returned as a string
- No validation
- Missing variables can cause runtime failures
- No default validation
- Secrets can accidentally be printed

Instead, Pydantic provides **BaseSettings**.

```python
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env"
    )

    api_key: SecretStr

    max_connections: int = Field(
        default=100,
        ge=1,
        le=1000
    )

    debug: bool = False


settings = AppSettings()

print(
    settings.max_connections,
    type(settings.max_connections)
)

print(settings.api_key)

print(
    settings.api_key.get_secret_value()
)
```

Output

```text
200 <class 'int'>
**********
actual-secret-key
```

Benefits:

- Automatically reads from `.env`
- Converts types automatically
- Validates values
- Supports default values
- Keeps secrets masked
- Centralized application configuration

This is the preferred way to manage configuration in production applications.



# Summary

Pydantic provides:

- Runtime type validation
- Data validation
- Automatic (limited) type coercion
- Custom validators
- Cross-field validation
- Computed fields
- Nested models
- Environment variable management
- Stronger, safer, and production-ready Python applications