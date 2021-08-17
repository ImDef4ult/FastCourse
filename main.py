from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn

App = FastAPI()


@App.get('/blog')
# Example of query: http://localhost:8000/blog?limit=5&published=True
def index(limit: int = 100, published: bool = True, sort: Optional[str] = None):
    if sort is not None:
        return {'data': f'Blog List of {limit} from the DB and published: {published} sorted'}
    else:
        return {'data': f'Blog List of {limit} from the DB and published: {published}'}


@App.get('/blog/unpublished')
def unpublished():
    return {'data': 'Unpublished'}


@App.get('/blog/{id_Blog}')
def about(id_Blog: int):
    return {'data': id_Blog}


@App.get('/blog/{id_blog}/comments')
def comments(id_blog: int):
    return {'data': {'comments': 'This is a comment', 'id': id_blog}}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@App.post('/blog')
def create_blog(blog_request: Blog):
    return {'data': f'Created blog with name {blog_request.title}, body: {blog_request.body} with published state: {blog_request.published}'}


# Just for Debugging
# if __name__ == '__main__':
#     uvicorn.run(App, host='127.0.0.1', port=8000)
