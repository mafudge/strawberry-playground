import json
import typing
import strawberry
import pandas as pd

from models import Book

def load_books():
    with open("./books.json") as file:
        data = json.load(file)
        return data

def get_books():
    '''
    Resolver function to get books from json file
    '''
    data = load_books()
    df = pd.json_normalize(data)
    jsondata = json.loads(df.to_json(orient='records'))
    books = [Book(**book) for book in jsondata]
    return books


@strawberry.type
class Query:
    books: typing.List[Book] = strawberry.field(resolver=get_books)


# Creating schema
schema = strawberry.Schema(query=Query)


