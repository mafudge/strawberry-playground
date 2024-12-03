import json
import typing
import strawberry
import pandas as pd


# this will get replaced via a dynamically generated one
@strawberry.type
class Book:
    title: str

def load_books():
    with open("./books.json") as file:
        data = json.load(file)
        return data

def generate_schema(data : list[dict]):
    '''
    schema generation 
    '''
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

def generate_model(schema: dict, classname : str):
    '''
    model generation
    '''
    model_code = f"@strawberry.type\nclass {classname}:"
    for key,val in schema.items():
        model_code += f"\n    {key}: {val}"
    return model_code


def write_model(model_code :str, filename : str):
    '''
    write model code to file
    '''
    data = "import json\nimport typing\nimport strawberry\n\n"
    data += model_code
    with open(filename,"w") as file:
        file.write(data)

def get_books():
    '''
    Resolver function to get books from json file
    '''
    data = load_books()
    df = pd.json_normalize(data)
    jsondata = json.loads(df.to_json(orient='records'))
    books = [Book(**book) for book in jsondata]
    return books


if __name__ == '__main__':
    data = load_books()
    schema = generate_schema(data)
    model = generate_model(schema, "Book")
    write_model(model, "models.py")

    