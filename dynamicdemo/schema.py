import json
import typing
import strawberry
import pandas as pd


# this will get replaced via a dynamically generated one
@strawberry.type
class Book:
    title: str

def load_books():
    '''
    load some json data
    '''
    with open("./books.json") as file:
        data = json.load(file)
        return data

def generate_schema():
    '''
    abstract schema generation 
    '''
    data = load_books()

    schema = {}
    # build schema
    for item in data:
        for key,val in item.items():
            if isinstance(val,int):
                schema[key] = "int"
            elif isinstance(val,float):
                schema[key] = "float"
            else:
                schema[key] = "str"
    # check for optional fields
    for item in data:
        for key, val in schema.items():
            if key not in item:
                schema[key] = f"typing.Optional[{val}]"

    return schema 

def generate_model(schema):
    '''
    strawberry model generation
    '''
    model_code = "@strawberry.type\nclass Book:"
    for key,val in schema.items():
        model_code += f"\n    {key}: {val}"
    return model_code


def get_books():
    '''
    Resolver function to get books from json file
    '''
    data = load_books()
    df = pd.json_normalize(data)
    jsondata = json.loads(df.to_json(orient='records'))
    books = [Book(**book) for book in jsondata]
    return books


schema = generate_schema()
exec(generate_model(schema))

# resolver
@strawberry.type
class Query:
    books: typing.List[Book] = strawberry.field(resolver=get_books)


# Creating schema
schema = strawberry.Schema(query=Query)


if __name__ == '__main__':
    print(generate_schema())
    data = load_books()
    df = pd.json_normalize(data)
    jsondata = json.loads(df.to_json(orient='records'))
    print(jsondata)     
    #schema.execute_sync(get_books)