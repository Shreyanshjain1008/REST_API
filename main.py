import uuid
from typing import List, Dict
from pydantic import BaseModel, EmailStr, Field

from fastapi import FastAPI, HTTPException, status

app = FastAPI(
    title="Basic CRUD API",
    description="An API for managing users with basic CRUD operations.",
    version="1.0.0",
)

# Use forward reference for User in db type hint
db: Dict[uuid.UUID, "User"] = {}

class UserBase(BaseModel):
    name: str = Field(..., min_length=1, description="User's full name")
    email: EmailStr = Field(..., description="User's valid email address")
    age: int = Field(..., gt=0, description="User's age, must be positive")

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: uuid.UUID

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user_create: UserCreate):
    """
    Create a new user.
    - Ensures email is not already in use.
    - Generates a new UUID for the user.
    """
    for existing_user in db.values():
        if existing_user.email == user_create.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered."
            )

    user = User(
        id=uuid.uuid4(),
        **user_create.dict()
    )

    db[user.id] = user

    return user

@app.get("/users", response_model=List[User])
def get_all_users():
    """
    Retrieve a list of all users.
    """
    return list(db.values())

@app.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: uuid.UUID):
    """
    Retrieve a single user by their ID.
    - Handles the case where the user is not found.
    """
    user = db.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found."
        )
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: uuid.UUID, user_update: UserCreate):
    """
    Update an existing user's details.
    - Handles the case where the user is not found.
    - Ensures email is not already in use by another user.
    """
    user = db.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found."
        )

    # Check for email uniqueness (excluding current user)
    for uid, existing_user in db.items():
        if uid != user_id and existing_user.email == user_update.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered to another user."
            )

    updated_user = User(
        id=user_id,
        name=user_update.name,
        email=user_update.email,
        age=user_update.age
    )
    db[user_id] = updated_user

    return updated_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: uuid.UUID):
    """
    Delete a user by their ID.
    - Handles the case where the user is not found.
    """
    if user_id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found."
        )

    del db[user_id]
    # No content to return for 204 status
    