import json
import typing
import strawberry

@strawberry.type
class Book:
    title: str
    author: str
    price: float
    qty: typing.Optional[int]