from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

books = [
    {
        "id": 1,
        "title": "The Alchemist",
        "author": "Paulo Coelho"
    },
    {
        "id": 2,
        "title": "The God of Small Things",
        "author": "Aravind Adiga"
    }
]

class Book(BaseModel):
    id: int
    title: str
    author: str

class BookUpdate(BaseModel):
    title: str
    author: str

app = FastAPI()

@app.get('/book')
def get_book():
    return books

@app.get('/book/{book_id}')
def get_book(book_id: int):
    book = list(filter(lambda x: x["id"] == book_id, books))[0]
    if book:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.post('/book')
def create_book(book: Book):
    books.append(book.model_dump())

@app.put('/book/{book_id}')
def update_book(book_id: int, book_update: BookUpdate):
    book = list(filter(lambda x: x["id"] == book_id, books))[0]
    if book:
        book["title"] = book_update.title
        book["author"] = book_update.author

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.delete('/book/{book_id}')
def delete_book(book_id: int):
    book = list(filter(lambda x: x["id"] == book_id, books))[0]
    if book:
        books.remove(book)
        return {"message": "The book was deleted"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")