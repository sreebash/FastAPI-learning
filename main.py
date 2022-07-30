from typing import Optional

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from blog import models
from blog.database import engine, SessionLocal
from blog.schemas import Blog

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


@app.post('/blog')
def create(request: Blog, db: Session = Depends(get_db)):
    return db
