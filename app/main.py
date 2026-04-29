from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from . import models, schemas, auth, database, websocket_manager

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Chat Application API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Chat Application API"}

@app.post("/auth/signup", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/auth/login", response_model=schemas.Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Role-Based Access Control Example
allow_admin_only = auth.RoleChecker([models.UserRole.admin])

@app.get("/admin-only", response_model=schemas.UserResponse)
def get_admin_data(current_user: models.User = Depends(allow_admin_only)):
    # This endpoint is only accessible to users with the 'admin' role
    return current_user

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    token: str = Query(...),
    db: Session = Depends(database.get_db)
):
    user = await auth.get_user_ws(token, db)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    await websocket_manager.manager.connect(websocket, room_id)
    try:
        await websocket_manager.manager.send_personal_message(f"Welcome to room {room_id}, {user.username}!", websocket)
        await websocket_manager.manager.broadcast(f"User {user.username} joined the chat", room_id)
        
        while True:
            data = await websocket.receive_text()
            message = f"{user.username}: {data}"
            await websocket_manager.manager.broadcast(message, room_id)
    except WebSocketDisconnect:
        websocket_manager.manager.disconnect(websocket, room_id)
        await websocket_manager.manager.broadcast(f"User {user.username} left the chat", room_id)
