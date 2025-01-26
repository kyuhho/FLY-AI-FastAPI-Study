from schema.request import CreateToDoRequest
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base

# Python console
# from database.connection import SessionFactory

# session = SessionFactory()

# from sqlalchemy import select
# from database.orm import ToDo

# # ToDo table에 있는 모든 Record를 출력
# todos = list(session.scalars(select(ToDo)))

# for todo in todos:
#     print(todo)

Base = declarative_base()

class ToDo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String(256), nullable=False)
    is_done = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"ToDo(id={self.id}, contents={self.contents}, is_done={self.is_done})"
    
    @classmethod
    def create(cls, request: CreateToDoRequest) -> "ToDo":
        return cls(
            contents = request.contents,
            is_done = request.is_done
        )
    
    def done(self) -> "ToDo":
        self.is_done = True
        return self

    def undone(self) -> "ToDo":
        self.is_done = False
        return self