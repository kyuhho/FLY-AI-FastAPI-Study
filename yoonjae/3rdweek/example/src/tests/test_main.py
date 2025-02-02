from fastapi.testclient import TestClient
from database.orm import ToDo
from main import app
from database.repository import ToDoRepository

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping":"pong"}

def test_get_todos(client, mocker):
    #order = ASC
    mocker.patch.object(ToDoRepository,"get_todos", return_value = [
        ToDo(id=1, contents="FastAPI Section 0", is_done=True),
        ToDo(id=2, contents="FastAPI Section 1", is_done=False),
    ])
    response = client.get("/example")
    assert response.status_code == 200
    assert response.json() == {"todos":[
            {"id":1, "contents":"FastAPI Section 0", "is_done":True},
            {"id":2, "contents":"FastAPI Section 1", "is_done":False},
            
        ]
    }
    #order = DESC
    response = client.get("/example?order=DESC")
    assert response.status_code == 200
    assert response.json() == {"todos":[
            
            {"id":2, "contents":"FastAPI Section 1", "is_done":False},
            {"id":1, "contents":"FastAPI Section 0", "is_done":True},
            
            
        ]
    }
    
    
def test_get_todo(client, mocker):
    #200
    mocker.patch.object(ToDoRepository,
        "get_todo_by_todo_id",
        return_value = ToDo(id=1, contents="todo",is_done=True),
        )
    response = client.get("/example/1")
    assert response.status_code == 200
    assert response.json() == {"id":1,"contents":"todo","is_done":True
    }
    #404
    mocker.patch.object(ToDoRepository,
        "get_todo_by_todo_id",
        return_value = None
        )
    response = client.get("/example/1")
    assert response.status_code == 404
    assert response.json() == {"detail":"ToDo Not Found"
    }
    
def test_create_todo(client, mocker):
    create_spy = mocker.spy(ToDo, "create") #main.py app.post의 ToDo.create
    mocker.patch.object(ToDoRepository,
        "get_todo_by_todo_id",
        return_value = ToDo(id=1, contents="todo",is_done=True),
        )
    body= {
        "contents":"test",
        "is_done":False,
    }
    #mocking을 활용하면 test code의 모든 부분을 검증하는게 아닐 수 있음->spy사용
    response = client.post("/example", json=body)
    assert create_spy.spy_return.id is None
    assert create_spy.spy_return.contents == "test"
    assert create_spy.spy_return.is_done is False
    
    assert response.status_code == 201
    assert response.json() == {"id":1,"contents":"todo","is_done":True
    }
    
def test_update_todo(client, mocker):
    mocker.patch.object(ToDoRepository,
        "get_todo_by_todo_id",
        return_value = ToDo(id=1, contents="todo",is_done=True),
        )
    undone = mocker.patch.object(ToDo, "undone")
    mocker.patch.object(ToDoRepository,
        "update_todo",
        return_value = ToDo(id=1, contents="todo",is_done=False),
        )
    response = client.patch("/example/1", json={"is_done":False})
    #is_done이 True면 undone 호출 X
    undone.assert_called_once_with()
    assert response.status_code == 200
    assert response.json() == {"id":1,"contents":"todo","is_done":False
    }
    mocker.patch.object(ToDoRepository,
        "get_todo_by_todo_id",
        return_value = None
        )
    response = client.get("/example/1")
    assert response.status_code == 404
    assert response.json() == {"detail":"ToDo Not Found"
    }
    
def test_delete_todo(client, mocker):
    #204
    mocker.patch.object(ToDoRepository,
        "get_todo_by_todo_id",
        return_value = ToDo(id=1, contents="todo",is_done=True),
        )
    
    mocker.patch.object(ToDoRepository,"delete_todo",return_value=None)
    
    response = client.delete("/example/1")
    assert response.status_code == 204
    
    #404
    mocker.patch.object(ToDoRepository,
        "get_todo_by_todo_id",
        return_value = None
        )
    response = client.delete("/example/1")
    assert response.status_code == 404
    assert response.json() == {"detail":"ToDo Not Found"
    }