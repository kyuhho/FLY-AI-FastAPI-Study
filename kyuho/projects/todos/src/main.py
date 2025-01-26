from typing import List
from fastapi import FastAPI, Body, HTTPException, Depends
from schema.request import CreateToDoRequest
from sqlalchemy.orm import Session

from database.connection import get_db
from database.repository import create_todo, delete_todo, get_todo_by_todo_id, get_todos, update_todo
from database.orm import ToDo

from schema.response import ToDoSchema
from schema.response import ToDoListSchema

app = FastAPI()

@app.get("/")
def health_check_handler():
    return {"ping": "pong"}

@app.get("/todos", status_code=200)
def get_todos_handler(
    order: str | None = None,
    session: Session = Depends(get_db)
) -> ToDoListSchema:

    todos : List[ToDo] = get_todos(session=session)

    if(order == "DESC"):
        return ToDoListSchema(
            todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]]
       )
    
    return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos]
    )

@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(
    todo_id: int,
    session: Session = Depends(get_db)
):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    
    if todo:
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Todo not found")

# request body를 알아서 CreateToDoRequest 형식으로 처리해줌
# 새로 생성된 todo item return
@app.post("/todos", status_code=201)
def create_todo_handler(
    request: CreateToDoRequest,
    session: Session = Depends(get_db)
):
    todo: ToDo = ToDo.create(request=request) # id = None
    todo: ToDo = create_todo(session=session, todo=todo) # id = int
    return ToDoSchema.from_orm(todo)

@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
    todo_id: int,
    is_done: bool = Body(..., embed=True),
    session: Session = Depends(get_db)
):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    
    if todo:
        todo.done() if is_done else todo.undone()
        todo: ToDo = update_todo(session=session, todo=todo)
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(
    todo_id: int,
    session: Session = Depends(get_db)
):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    delete_todo(session=session)
    

