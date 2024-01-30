from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from .schemas import Blog
from . import schemas
from . import models
from .hashing import Hash
from .database import engine, SessionLocal
from . import models
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app  = FastAPI()

app.mount("/static", StaticFiles(directory="D:\FastAPI\static"), name="static")


models.Base.metadata.create_all(engine)

origins = [
    "http://localhost:8000",  # Adjust this to the domain where your frontend is served
    "http://localhost:3000",  # Common for React development
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close() 

@app.post("/blog", status_code= status.HTTP_201_CREATED, tags=['blogs'])
def create_blog(request: Blog, db: Session = Depends(get_db)):

    new_blog = models.BlogsTable(title= request.title, body= request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

@app.put("/blog/{id}", status_code= status.HTTP_202_ACCEPTED, tags=['blogs'])
def update_particular_blog(id, request: Blog,  db: Session= Depends(get_db)):
    blog = db.query(models.BlogsTable).filter(models.BlogsTable.id == id)
    if not blog.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Blog with id: {id} not found in the database...")
    else:
        blog.update(
            {
                "title": request.title,
                "body": request.body
            }
        )
        db.commit()

        return {"detail": f"updated the details for {id} successfully....."}


@app.get("/blog", response_model=List[schemas.ShowBlog], tags=['blogs'])
def get_all_blogs(db: Session = Depends(get_db)):
    all_blogs = db.query(models.BlogsTable).all()    

    return all_blogs

@app.get("/blog/{id}", status_code=200, response_model= schemas.ShowBlog, tags=['blogs'])
def get_particular_blog_details(id, response: Response, db: Session= Depends(get_db)):
    blog = db.query(models.BlogsTable).filter(models.BlogsTable.id == id).first()
    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail={"detail": f"blog with {id} is not available ..."} )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"blog with {id} is not available ..."}
    return blog

@app.delete("/blog/{id}", status_code= status.HTTP_204_NO_CONTENT, tags=['blogs'])
def delete_particular_blog(id, db: Session= Depends(get_db)):

    blog = db.query(models.BlogsTable).filter(models.BlogsTable.id == id)
    if not blog.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"blog with id: {id} not found")
    
    blog.delete(synchronize_session=False)                         
    db.commit()

    return {"detail": f"Deleted {id} successfully..."}



@app.post("/user",response_model=schemas.ShowUser, tags=['users'])
def create_user(request:schemas.User, db: Session= Depends(get_db)):
    hashed_pwd = Hash.bcrypt(request.password)
    new_user = models.UserTable(name=request.username, email=request.email, password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/user/{id}", response_model=schemas.ShowUser, tags=['users'])
def get_user(id, db: Session= Depends(get_db)):
    user = db.query(models.UserTable).filter(models.UserTable.id == id).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    return user
