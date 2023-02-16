from fastapi import FastAPI

app = FastAPI()


@app.get("/")

def root():
    return {
        "msg": "Hopefully, I'm gonna be pretty pretty API someday :)"
    }
        