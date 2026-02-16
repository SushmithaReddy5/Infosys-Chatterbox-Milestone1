from fastapi import FastAPI, WebSocket
import uvicorn

# ----------------------------------------------------
# 1. Create FastAPI App
# ----------------------------------------------------
app = FastAPI()


# ----------------------------------------------------
# 2. Simple GET API to check the server
# ----------------------------------------------------
@app.get("/")
async def read_root():
    return {"message": "Chatterbox Milestone 1 - WebSocket Server Running"}


# ----------------------------------------------------
# 3. WebSocket Endpoint
# ----------------------------------------------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    # Step 1: Accept the WebSocket connection
    await websocket.accept()
    print("Client connected!")

    # Step 2: Listen for messages continuously
    while True:
        try:
            # Receive message from client
            message = await websocket.receive_text()
            print(f"Received: {message}")

            # Step 3: Send reply back (echo)
            await websocket.send_text(f"Server: You said -> {message}")

        except Exception as e:
            print("Client disconnected!", e)
            break


# ----------------------------------------------------
# 4. Start the WebSocket Server
# ----------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)