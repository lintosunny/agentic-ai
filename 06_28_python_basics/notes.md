# 1. Array vs List

| List | Array |
|------|------|
| Built into Python | Requires `array` module or NumPy |
| Can store mixed data types | Stores only one data type |
| More flexible | More memory efficient |

```python
# List
numbers = [1, 2, 3, "hello"]

# Array
from array import array
numbers = array('i', [1, 2, 3])
```


# 2. JSON

JSON (JavaScript Object Notation) is a **text format** for storing and exchanging data.

Python represents JSON objects as **dictionaries (`dict`)**.

```python
weather_reading = {
    "city": "Bangalore"
}
```

### Access values

```python
print(weather_reading["city"])
```

or safely

```python
print(weather_reading.get("city"))
```

### Add a new key

```python
weather_reading["temp"] = 28
```

### Read temperature

```python
print(weather_reading["temp"])

# safer
print(weather_reading.get("temp"))
```

## JSON vs Dictionary

Although they look similar, **JSON and Python dictionaries are not the same.**

| JSON | Python `dict` |
|------|---------------|
| Text format for data exchange | Python data structure |
| Keys must be strings | Keys can be any immutable type (strings, integers, tuples, etc.) |
| Uses `true`, `false`, `null` | Uses `True`, `False`, `None` |
| Double quotes are required for strings | Single or double quotes can be used |
| Stored/transmitted as a string | Stored as an object in memory |

### JSON

```json
{
    "name": "Alice",
    "age": 25,
    "is_student": false
}
```

### Python Dictionary

```python
person = {
    "name": "Alice",
    "age": 25,
    "is_student": False
}
```

### Convert between JSON and Dictionary

```python
import json

# Dictionary → JSON
person = {"name": "Alice", "age": 25}
json_data = json.dumps(person)

print(json_data)
```

```python
import json

# JSON → Dictionary
json_data = '{"name":"Alice","age":25}'
person = json.loads(json_data)

print(person)
```

> **Remember:** JSON is a **string (text format)** used to exchange data, while a Python **dictionary (`dict`)** is an in-memory data structure used within Python programs.

# 3. OOP (Object-Oriented Programming)

OOP organizes code using **objects** and **classes**.

A class is a blueprint.
An object is an instance of that class.

## Example: Bank Account

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount

account = BankAccount("John", 1000)
account.deposit(500)

print(account.balance)
```


# 4. Dataclass

A **dataclass** automatically creates methods like:

- `__init__()`
- `__repr__()`
- `__eq__()`

Less boilerplate code.

```python
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    age: int

s = Student("Alice", 20)

print(s)
```

Instead of writing a long `__init__`, Python generates it automatically.


# 5. try-except

Used for **handling errors** without crashing the program.

```python
try:
    num = int(input("Enter number: "))
    print(10 / num)

except ValueError:
    print("Please enter a valid number.")

except ZeroDivisionError:
    print("Cannot divide by zero.")
```


# 6. Decorators

A decorator **adds extra behavior to a function without modifying it.**

```python
def logger(func):
    def wrapper():
        print("Function started")
        func()
        print("Function ended")
    return wrapper

@logger
def greet():
    print("Hello!")

greet()
```

Output

```
Function started
Hello!
Function ended
```

Common decorators:
- `@staticmethod`
- `@classmethod`
- `@property`


# 7. Calling a Real API

API = A way for applications to communicate.

Example using a free API:

```python
import requests

url = "https://api.github.com/users/octocat"

response = requests.get(url)
data = response.json()

print(data["login"])
print(data["public_repos"])
```

Another example:

```python
import requests

response = requests.get("https://api.agify.io?name=alice")
print(response.json())
```

Output

```python
{
    "name": "alice",
    "age": 27,
    "count": 12345
}
```