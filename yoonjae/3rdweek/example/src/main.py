from fastapi import FastAPI, Body, HTTPException, Depends
from pydantic import BaseModel
from database.connection import get_db
from schema.response import ToDoSchema
from schema.response import ToDoListSchema
from typing import List
from database.orm import ToDo
from schema.request import CreateToDoRequest 
from sqlalchemy.orm import Session
from database.repository import ToDoRepository
app = FastAPI()
@app.get("/")
def health_check_handler():
    return  {"ping":"pong"}




@app.get("/example")
def get_todos_handler(
    order:str | None = None,
    todo_repo:ToDoRepository = Depends(ToDoRepository),
)->ToDoListSchema:
    todos: List[ToDo] = todo_repo.get_todos()
    
    if order and order == "DESC":
        return ToDoListSchema(
        todos =[
            ToDoSchema.from_orm(todo)
            for todo in todos[::-1]
        ]
    )
        
    return ToDoListSchema(
        todos =[
            ToDoSchema.from_orm(todo)
            for todo in todos
        ]
    )
@app.get("/example/{todo_id}", status_code = 200)
def get_todo_handler(
    todo_id:int,
    todo_repo:ToDoRepository = Depends(ToDoRepository),
)->ToDoSchema:
    todo: ToDo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)
    if todo:
        return ToDoSchema.from_orm(todo)
    
    raise HTTPException(status_code = 404, detail = "ToDo Not Found")







    
@app.post("/example", status_code = 201)
def create_todo_handler(request: CreateToDoRequest,
                       todo_repo:ToDoRepository = Depends(ToDoRepository),
    )->ToDoSchema:
    todo: ToDo = ToDo.create(request=request) #id=None
    todo: ToDo=todo_repo.create_todo(todo=todo) #id할당
    
    return ToDoSchema.from_orm(todo)

@app.patch("/example/{todo_id}", status_code = 200)
def update_todo_handler(todo_id: int,
                        is_done: bool = Body(..., embed = True),
                        todo_repo:ToDoRepository = Depends(ToDoRepository),
                        
):
    todo: ToDo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)
    if todo:
        if is_done is True:
            todo.done()
        else:
            todo.undone()
        todo: ToDo = todo_repo.update_todo(todo=todo)
        return ToDoSchema.from_orm(todo)
    
    raise HTTPException(status_code = 404, detail = "ToDo Not Found")

@app.delete("/example/{todo_id}", status_code = 204)
def delete_todo_handler(todo_id: int,
                        todo_repo:ToDoRepository = Depends(ToDoRepository),
):
    todo: ToDo | None = todo_repo.get_todo_by_todo_id( todo_id=todo_id)
    if not todo:
        
        raise HTTPException(status_code = 404, detail = "ToDo Not Found")
    
    todo_repo.delete_todo(todo_id=todo_id)
    
    


    


