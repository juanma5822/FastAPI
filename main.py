from fastapi import FastAPI


app = FastAPI()

@app.get("/") # path operation decorator
def home():
    return {"Hello": "World"}


