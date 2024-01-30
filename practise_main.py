from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# PATH -> ('/', '/about')
# Operation -> GET/POST
# Path operation decorator: Complete function along with the decorator.

@app.get('/')
def index():
    return "Hello, world!"

@app.get('/about')
def about():
    return {
        "Name": "Venkat",
        "University": "CU Boulder",
        "address": {
            "Apt":7,
            "City": "Boulder",
            "State": "Colorado",
            "pincode":80304,
            "Country": "USA"

        }
    }

## Here, if we don't have path parameters, then 
## FASTAPI will assume that the variable is by default Query parameter.
## So, limit, sort, and other variables are Query parameters.

@app.get('/blog')
def blog(limit = 10, sort: bool = True, other: Optional[str] = None):
    if sort:
        return {"data": f"Sort Value is {sort} and other value is: {other}"}
    else:
        return {"data": f"Sort Value is {sort} and other value is: {other}"}
    

# Here id is called Path `parameter`.
# Also, the id should be INTEGER Type.
# Otherwise, FASTAPI will return an error with the error message.

@app.get("/blog/{id}")
def show(id: int):
    print(f"Received {id} from the user")

    return {"data": {"id": id}}

## This won't be executed as the /blog/{id} defined in the previous step 
## Conflicts with the given parameters.


@app.get("/blog/data")
def showString(data):
    return {"data": data}

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]



@app.post("/blog")
def create_blog(request: Blog):

    return {"data": f"Blog is created with {request.title} and {request.body}"}
