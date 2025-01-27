from fastapi import FastAPI, Body, HTTPException, Depends
from pydantic import BaseModel
from database.connection import get_db
from database.repository import get_todos
from schema.response import ToDoSchema
from schema.response import ToDoListSchema
from typing import List
from database.orm import ToDo
from schema.request import CreateToDoRequest 
from sqlalchemy.orm import Session
from database.repository import get_todo_by_todo_id
from database.repository import create_todo
from database.repository import update_todo
from database.repository import delete_todo
app = FastAPI()
@app.get("/")
def health_check_handler():
    return  {"ping":"pong"}


todo_data={
    1:{
       "id":   1,
       "contents": "실전! FastAPI 섹션 0 수강",
       "is_done" : True, 
    },
    2:{
       "id":   2,
       "contents": "실전! FastAPI 섹션 1 수강",
       "is_done" : False, 
    },
    3:{
       "id":   3,
       "contents": "실전! FastAPI 섹션 2 수강",
       "is_done" : False, 
    },
    
}

@app.get("/example")
def get_todos_handler(
    order:str | None = None,
    session : Session = Depends(get_db),
)->ToDoListSchema:
    todos: List[ToDo] = get_todos(session = session)
    
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
    session : Session = Depends(get_db),
)->ToDoSchema:
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        return ToDoSchema.from_orm(todo)
    
    raise HTTPException(status_code = 404, detail = "ToDo Not Found")







    
@app.post("/example", status_code = 201)
def create_todo_handler(request: CreateToDoRequest,
                        session:Session=Depends(get_db),
    )->ToDoSchema:
    todo: ToDo = ToDo.create(request=request) #id=None
    todo: ToDo=create_todo(session=session, todo=todo) #id할당
    
    return ToDoSchema.from_orm(todo)

@app.patch("/example/{todo_id}", status_code = 200)
def update_todo_handler(todo_id: int,
                        is_done: bool = Body(..., embed = True),
                        session:Session=Depends(get_db),
                        
):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        if is_done is True:
            todo.done()
        else:
            todo.undone()
        todo: ToDo = update_todo(session=session, todo=todo)
        return ToDoSchema.from_orm(todo)
    
    raise HTTPException(status_code = 404, detail = "ToDo Not Found")

@app.delete("/example/{todo_id}", status_code = 204)
def delete_todo_handler(todo_id: int,
                        session:Session = Depends(get_db),
):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if not todo:
        
        raise HTTPException(status_code = 404, detail = "ToDo Not Found")
    
    delete_todo(session=session,todo_id=todo_id)
    
    


    


