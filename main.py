from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Todo
from schemas import TodoCreate, TodoResponse
import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo API",
    description="FastAPI + SQLAlchemy CRUD API",
    version="1.0.0"
)

# Home Route
@app.get("/")
def home():
    return {"message": "Todo API is running successfully on Railway 🚀"}

# Health Check Route
@app.get("/health")
def health():
    return {"status": "ok"}

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE TODO
@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(
        title=todo.title,
        description=todo.description
    )

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo

# READ ALL TODOS
@app.get("/todos", response_model=list[TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

# READ SINGLE TODO
@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    return todo

# UPDATE TODO
@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    updated_todo: TodoCreate,
    db: Session = Depends(get_db)
):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    todo.title = updated_todo.title
    todo.description = updated_todo.description

    db.commit()
    db.refresh(todo)

    return todo

# DELETE TODO
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    db.delete(todo)
    db.commit()

    return {"message": "Todo deleted successfully"}