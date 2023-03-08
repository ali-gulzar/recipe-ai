from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()


@app.get("/")
def fastapi_barebones():
    return "FastAPI barebone application!"


handler = Mangum(app)
