from pydantic import BaseModel

class CreateToDoRequest(BaseModel):
        #일부러 id: int 없앴음
    contents: str
    is_done: bool
    
    