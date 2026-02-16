from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

# ---------------------------------------
# 1. Create FastAPI App
# ---------------------------------------
app = FastAPI()


# ---------------------------------------
# 2. Store Active Connections
# ---------------------------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[websocket] = username

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            del self.active_connections[websocket]

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    def get_usernames(self):
        return list(self.active_connections.values())


manager = ConnectionManager()


# ---------------------------------------
# 3. Root API
# ---------------------------------------
@app.get("/")
async def root():
    return {"message": "Chatterbox Milestone 2 - Group Chat Server Running"}


# ---------------------------------------
# 4. WebSocket Endpoint
# ---------------------------------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    # Ask for username
    await websocket.accept()
    await websocket.send_text("Enter your username:")

    username = await websocket.receive_text()

    # Add user
    await manager.connect(websocket, username)

    # Notify all
    await manager.broadcast(f" {username} joined the chat")

    print(f"{username} connected")

    try:
        while True:

            message = await websocket.receive_text()

            # Special command: show users
            if message.lower() == "/users":
                users = ", ".join(manager.get_usernames())
                await websocket.send_text(f"Online users: {users}")
            else:
                # Broadcast normal message
                await manager.broadcast(f"{username}: {message}")

    except WebSocketDisconnect:

        manager.disconnect(websocket)

        # Notify all
        await manager.broadcast(f" {username} left the chat")

        print(f"{username} disconnected")


# ---------------------------------------
# 5. Run Server
# ---------------------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
