from typing import List
from sqlalchemy import select,delete
from sqlalchemy.orm import Session
from fastapi import Depends
from database.connection import get_db
from database.orm import ToDo


class ToDoRepository:
    def __init__(self, session:Session = Depends(get_db)):
        self.session= session
         
    def get_todos(self) -> List[ToDo]:
        return list(self.session.scalars(select(ToDo)))
        
        
    def get_todo_by_todo_id(self, todo_id:int)->ToDo|None:
        return self.session.scalar(select(ToDo).where(ToDo.id==todo_id))

    def create_todo(self, todo:ToDo) -> ToDo:
        self.session.add(instance=todo) #orm 객체를 session object에 추가, session에 쌓임
        
        self.session.commit() #database에 data 저장
        self.session.refresh(instance=todo) #db를 읽어오고 todo_id 값이 결정이 되고 todo에 이것이 반영
        return todo

    def update_todo(self, todo:ToDo)->ToDo:
        self.session.add(instance=todo) #orm 객체를 session object에 추가, session에 쌓임
        
        self.session.commit() #database에 data 저장
        self.session.refresh(instance=todo) #db를 읽어오고 todo_id 값이 결정이 되고 todo에 이것이 반영
        return todo

    def delete_todo(self, todo_id:int)->None:
        self.session.execute(delete(ToDo).where(ToDo.id==todo_id))
        self.session.commit()
        