from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}


@app.get('/blog')
def index(limit=10, published: bool = True, sort: Optional[str] = None):
    # return published
    if published:
        return {'data': f'{limit} published blogs from the database'}
    return {'data': f'{limit} blogs from the database'}


@app.get('/blog/{unpublished}')
def unpublished(unpublished: str):
    return {'data': unpublished}


@app.get('/blog/{blog_id}')
def show_blog(blog_id: int):
    return {'data': blog_id}


@app.get('/blog/{comments_id}/comments')
def comments(comments_id, limit: int = 10):
    return limit


class Blog(BaseModel):
    title: str
    body: str
    published_at: Optional[bool]


@app.post('/blog')
def create_blog(request: Blog):
    return {'data': 'Blog is created'}
