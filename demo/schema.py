import json
import typing
import strawberry
from pydantic import BaseModel


@strawberry.type
class Book(BaseModel):
    title: str
    author: str
    price: float


def get_books():
    '''
    Resolver function to get books from json file
    '''
    with open("./books.json") as file:
        data = json.load(file)
    books = [Book.model_validate(book) for book in data]
    return books


@strawberry.type
class Query:
    books: typing.List[Book] = strawberry.field(resolver=get_books)


# Creating schema
schema = strawberry.Schema(query=Query)


if __name__ == '__main__':
    pass
    #schema.execute_sync(get_books)