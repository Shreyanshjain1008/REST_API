# Basic CRUD API with FastAPI

This is a simple REST API built with Python and FastAPI that performs basic CRUD (Create, Read, Update, Delete) operations on a `users` resource. It uses an in-memory dictionary for data storage.

## ✨ Features

-   **Create, Read, Update, and Delete** users.
-   **Data Validation** using Pydantic (e.g., valid email, positive age).
-   **In-Memory Storage** (data resets on server restart).
-   **Automatic API Docs** via Swagger UI and ReDoc.

## 🚀 Setup and Run

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/Shreyanshjain1008/REST_API.git
    cd REST_API
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```sh
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Run the server:**
    ```sh
    uvicorn main:app --reload
    ```

5.  **Access the API:**
    -   The API will be running at `http://127.0.0.1:8000`.
    -   Access the interactive Swagger docs at **`http://127.0.0.1:8000/docs`**.

## ⚙️ API Endpoints

-   `POST /users` - Create a new user.
-   `GET /users` - Get a list of all users.
-   `GET /users/{user_id}` - Get a single user by their ID.
-   `PUT /users/{user_id}` - Update an existing user.
-   `DELETE /users/{user_id}` - Delete a user.
