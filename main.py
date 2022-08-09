from typing import Optional, List

from fastapi import FastAPI, Depends, Response, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from blog import models, schemas
from blog.database import engine, SessionLocal
from blog.hashing import Hash, pwd_cxt
from blog.schemas import Blog
from passlib.context import CryptContext

app = FastAPI()

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}

#
# @app.get('/blog')
# def index(limit=10, published: bool = True, sort: Optional[str] = None):
#     # return published
#     if published:
#         return {'data': f'{limit} published blogs from the database'}
#     return {'data': f'{limit} blogs from the database'}
#
#
# @app.get('/blog/{unpublished}')
# def unpublished(unpublished: str):
#     return {'data': unpublished}
#
#
# @app.get('/blog/{blog_id}')
# def show_blog(blog_id: int):
#     return {'data': blog_id}
#
#
# @app.get('/blog/{comments_id}/comments')
# def comments(comments_id, limit: int = 10):
#     return limit
#
#
# class Blog(BaseModel):
#     title: str
#     body: str
#     published_at: Optional[bool]
#

# @app.post('/blog')
# def create_blog(blog: Blog):
#     return {'data': f'Blog is created with {blog.title}'}


models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', response_model=List[schemas.ShowBlog], tags=['blogs'])
def get_blog_list(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['blogs'])
def get_single_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} is not exist!')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with the id {id} is not available'}
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def delete_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} is not exist!')

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} is deleted!')

    return 'deleted done'


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update_blog(id, request: Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).update({'title': request.title, 'body': request.body})
    db.commit()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} is not exist!')

    return f'Blog with the id {id} is updated'


@app.post('/user', response_model=schemas.ShowUser, tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['users'])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} is not available')

    return user
