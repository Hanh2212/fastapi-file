from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()
file_path = 'data.json'


class Item(BaseModel):
    id: int
    name: str
    author: str
    description: str = None


def read_file():
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def write_file(data):
    with open(file_path, 'w') as file:
        json.dump(data, file)


@app.get("/books/", response_model=list[Item])
def get_books():
    data = read_file()
    print(data)
    return read_file()


@app.get('/books/{book_id}', response_model=Item)
def get_books_detail(book_id: int):
    data = read_file()
    for existing_books in data:
        if existing_books['id'] == book_id:
            return existing_books
    raise HTTPException(status_code=404, detail='Book not found')


@app.post('/books/', response_model=Item)
def add_book(book: Item):
    data = read_file()
    print(data)
    if any(existing_book['id'] == book.id for existing_book in data):
        raise HTTPException(status_code=400, detail='Item with this id aleady exist')
    data.append(book.dict())
    write_file(data)
    return book


@app.put('/books/{book_id}', response_model=Item)
def update_book(book_id: int, book: Item):
    data = read_file()
    for index, existing_book in enumerate(data):
        if existing_book['id'] == book_id:
            data[index] = book.dict()
            write_file(data)
            return book
    raise HTTPException(status_code=400, detail='Book not found')


@app.delete('/books/{book_id}', response_model=dict)
def delete_book(book_id: int):
    data = read_file()
    for index, existing_book in enumerate(data):
        if existing_book['id'] == book_id:
            deleted_book = data.pop(index)
            write_file(data)
            return {'message': 'Book deleted successfully', 'book': deleted_book}
    raise HTTPException(status_code=404, detail='Book not found')
