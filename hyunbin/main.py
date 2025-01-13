from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def health_check_handler() :
    return {"ping" : "pong"}


todo_data = {
    1 : {
        "id" : 1,
        "contents" : "몰라"
    }
}