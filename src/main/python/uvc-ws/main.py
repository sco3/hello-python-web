from fastapi import FastAPI, WebSocket
import uvicorn
import logging

logging.basicConfig(level=logging.CRITICAL)

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, world!\n")
    await websocket.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081, log_level="critical")