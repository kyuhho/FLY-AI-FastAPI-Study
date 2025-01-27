from typing import List
from sqlalchemy import select,delete
from sqlalchemy.orm import Session

from database.orm import ToDo 
def get_todos(session:Session) -> List[ToDo]:
    return list(session.scalars(select(ToDo)))
    
    
def get_todo_by_todo_id(session:Session, todo_id:int)->ToDo|None:
    return session.scalar(select(ToDo).where(ToDo.id==todo_id))

def create_todo(session:Session, todo:ToDo) -> ToDo:
    session.add(instance=todo) #orm 객체를 session object에 추가, session에 쌓임
    
    session.commit() #database에 data 저장
    session.refresh(instance=todo) #db를 읽어오고 todo_id 값이 결정이 되고 todo에 이것이 반영
    return todo

def update_todo(session:Session, todo:ToDo)->ToDo:
    session.add(instance=todo) #orm 객체를 session object에 추가, session에 쌓임
    
    session.commit() #database에 data 저장
    session.refresh(instance=todo) #db를 읽어오고 todo_id 값이 결정이 되고 todo에 이것이 반영
    return todo

def delete_todo(session:Session, todo_id:int)->None:
    session.execute(delete(ToDo).where(ToDo.id==todo_id))
    session.commit()
    