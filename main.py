from fastapi import FastAPI,Request,Path
from pydantic import BaseModel, Field
from typing import Union

app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = "0.1.0"


class Movie(BaseModel):
    id: Union[int,None] = None
    title:str = Field(min_length=5, max_length=15)
    overview:str = Field(default="Descripcion de la pelicula", min_length=15, max_length=50)
    year:str
    rating:float = Field(ge=0,le=10)
    category:str

    class Config:
        schema_extra = {
            "example":{
                "id":1,
                "title":"Titulo Pelicula",
                "overview":"Descripcion de la pelicula",
                "year":2022,
                "rating":4.2,
                "category":"Acción"

            }
        }


movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    }, {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    } 
]


@app.get('/',tags=['home'])
def message():
    return "Hello, word"


@app.get('/movies', tags=['movies'])
async def get_movies():
    return movies


@app.get('/movies/{id}',tags=['movies'])
async def get_movie(id:int):
    movie = filter(lambda x:x['id'] == id,movies)
    try:
        return list(movie)[0]
    except:
        return {"error":"No se encontro la pelicula"}

@app.get('/movies/',tags=['movies'])
async def get_movies_by_category(category: str):
    movies_filter = filter(lambda mv:mv['category']==category,movies)
    return list(movies_filter)

@app.post('/movies',tags=['movies'])
async def create_movie(movie: Movie):
    if movie.id:
        mv= filter(lambda x: x['id']==movie.id,movies)
        if len(list(mv))>0:
            return {"error":"el ID de la pelicula ya existe"}
    
    movie.id = movies[-1]['id'] + 1 
    movies.append(movie.dict())
    return movie

@app.delete('/movies/{id}',tags=['movies'])
async def delete_movie(id:int):
    for index,movie in enumerate(movies):
        if movie['id'] == id:
            del movies[index]
            return movie
    return{"error":"la pelicula no existe"}


@app.put('/movies/{id}',tags=['movies'])
async def update_movie(id:int,movie:Request):
    movie_js= await movie.json()
    for index,movie_up in enumerate(movies):
        if movie_up['id'] == id:
            movies[index].update(movie_js)
            return movies[index]

    return {"error":"No se encuentra la pelicula"}        