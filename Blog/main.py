from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from .hashing import Hash

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as Ex:
        print(f'Error: {Ex}')
    finally:
        db.close()


# Create a new Blog (INSERT)
@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['Blog'])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# Get all blogs(SELECT)
@app.get('/blog', response_model=List[schemas.ShowBlog], tags=['Blog'])  # List because the response is a list of elements
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


# Look for a specific blog using the id (SELECT WHERE)
@app.get('/blog/{blog_id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['Blog'])
def get_blog_byId(blog_id: int, response: Response, db: Session = Depends(get_db)):
    blog_result = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id: {blog_id} doesn\'t exist')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return f'Blog with id: {blog_id} doesn\'t exist'
    else:
        return blog_result


# Delete a blog (DELETE WHERE)
@app.delete('/blog/{blog_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blog'])
def delete_Blog(blog_id, db: Session = Depends(get_db)):
    blog_result = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog_result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id: {blog_id} doesn\'t exist')
    blog_result.delete(synchronize_session=False)
    db.commit()
    return f'Blog with id: {blog_id} was successfully deleted'


# Update a blog (UPDATE WHERE)
@app.put('/blog/{blog_id}', status_code=status.HTTP_202_ACCEPTED, tags=['Blog'])
def update_Blog(blog_id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog_result = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog_result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id: {blog_id} doesn\'t exist')
    blog_result.update({
        'title': request.title,
        'body': request.body
    })
    # blog_result.update(request)
    db.commit()
    return f'The blog with id: {blog_id} has been updated!'


# Create an user (INSERT)
@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=['User'])
def create_User(request: schemas.User, db: Session = Depends(get_db)):
    hashed_pwd = Hash.crypt(request.password)
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Look for a specific blog using the id (SELECT WHERE)
@app.get('/user/{user_id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=['User'])
def get_user_byId(user_id: int, db: Session = Depends(get_db)):
    user_result = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {user_id} doesn\'t exist')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return f'Blog with id: {blog_id} doesn\'t exist'
    else:
        return user_result

