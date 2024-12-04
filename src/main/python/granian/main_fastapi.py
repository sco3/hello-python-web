



from fastapi import FastAPI

from granian.server import Granian
from granian.constants import HTTPModes, Interfaces, Loops, ThreadModes

app = FastAPI()


@app.get("/")
async def home():
    return f"Hello, World!\n"




if __name__ == "__main__":
    server = Granian(target="main_fastapi:app",interface=Interfaces.ASGI, address="0.0.0.0", port=8080, workers=1)
    server.serve()