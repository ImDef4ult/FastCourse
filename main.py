from fastapi import FastAPI

App = FastAPI()


@App.get('/')
def index():
    return {'data': {'name': 'ImDef4ult'}}


@App.get('/about')
def about():
    return {'data': {'name': 'About Page'}}