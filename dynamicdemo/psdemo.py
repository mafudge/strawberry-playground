import json
import typing
import strawberry


@strawberry.type
class Book:
    title: str
    author: str
    price: float
    qty: typing.Optional[int]


if __name__ == '__main__':
    data = {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "price": 10.0,
        "qty": None
    }
    book = Book(**data)
    print(book)
    #schema.execute_sync(get_books)