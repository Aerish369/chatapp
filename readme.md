# Chat Application API

This is a real-time chat application API built with FastAPI, WebSockets, and SQLite. It features JWT-based authentication, role-based access control (RBAC), and real-time messaging through WebSockets.

## Features
- **FastAPI**: High-performance asynchronous API.
- **SQLite & SQLAlchemy**: Database integration and ORM.
- **JWT Authentication**: Secure user login and authorization.
- **Role-Based Access Control**: Different permissions for `admin` and `user` roles.
- **WebSockets**: Real-time broadcast messaging in chat rooms.

## Prerequisites
- Python 3.8+
- [Git](https://git-scm.com/) (optional, for cloning)

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd "Chat Application"
   ```

2. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`.



## API Endpoints Guide

### 1. Root Endpoint
Check if the API is running.
- **URL**: `/`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "message": "Welcome to the Chat Application API"
  }
  ```

### 2. User Signup
Register a new user.
- **URL**: `/auth/signup`
- **Method**: `POST`
- **Request Body (JSON)**:
  ```json
  {
    "username": "johndoe",
    "password": "secretpassword",
    "role": "user" 
  }
  ```
  *(Note: `role` can be `"user"` or `"admin"`. It defaults to `"user"` if not provided.)*
- **Response (201 Created)**:
  ```json
  {
    "id": 1,
    "username": "johndoe",
    "role": "user"
  }
  ```

### 3. User Login (Get JWT Token)
Authenticate and receive an access token.
- **URL**: `/auth/login`
- **Method**: `POST`
- **Content-Type**: `application/x-www-form-urlencoded`
- **Request Body**:
  - `username`: your_username
  - `password`: your_password
- **Response (200 OK)**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1...",
    "token_type": "bearer"
  }
  ```

### 4. Admin Only Endpoint (RBAC Example)
Requires the `admin` role and a valid Bearer token.
- **URL**: `/admin-only`
- **Method**: `GET`
- **Headers**:
  - `Authorization: Bearer <your_access_token>`
- **Response (200 OK)**:
  ```json
  {
    "id": 2,
    "username": "adminuser",
    "role": "admin"
  }
  ```
- **Error Response (403 Forbidden)** if a regular user tries to access it.

### 5. WebSocket Chat Room
Connect to a real-time chat room. You must provide the JWT token as a query parameter for authentication.
- **URL**: `ws://127.0.0.1:8000/ws/{room_id}?token=<your_access_token>`
- **Method**: `WebSocket`
- **Usage**:
  Connect to the WebSocket using JavaScript or any WebSocket client. Once connected, any text message sent will be broadcasted to all users in the `{room_id}`.
- **This feature is yet to be implemented**




