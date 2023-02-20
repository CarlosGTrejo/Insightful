from fastapi import FastAPI, WebSocket
import uvicorn
# import io

app = FastAPI()
connected_clients = set()


async def send_back(websocket, file):
    # same_file = io.BytesIO()
    await websocket.send_bytes(file)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            file = await websocket.receive_bytes()
            await send_back(websocket, file)
    finally:
        connected_clients.remove(websocket)

uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
