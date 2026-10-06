from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional

import models
from database import engine, get_db
from auth import hash_password, verify_password, create_access_token, get_current_user

# Recreate tables with new structure
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskFlow API with Authentication",
    description="Backend REST API with MS SQL Server and JWT Authentication.",
    version="3.0.0"
)

# Pydantic Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskResponse(TaskCreate):
    id: int
    completed: bool
    owner_id: int

    class Config:
        from_attributes = True

# --- AUTH ENDPOINTS ---
@app.post("/register", response_model=UserResponse, status_code=201, summary="Register a new user")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.UserModel).filter(models.UserModel.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = hash_password(user.password)
    new_user = models.UserModel(email=user.email, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token", response_model=Token, summary="Login and get JWT token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm uses 'username' field for email in Swagger
    user = db.query(models.UserModel).filter(models.UserModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- PROTECTED TASK ENDPOINTS ---
@app.get("/tasks", response_model=List[TaskResponse], summary="Get current user's tasks")
def get_user_tasks(db: Session = Depends(get_db), current_user: models.UserModel = Depends(get_current_user)):
    return current_user.tasks

@app.post("/tasks", response_model=TaskResponse, status_code=201, summary="Create task for current user")
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: models.UserModel = Depends(get_current_user)):
    new_task = models.TaskModel(
        title=task.title,
        description=task.description,
        completed=False,
        owner_id=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# --- UPDATE and DELETE task endpoints ---
@app.put("/tasks/{task_id}", response_model=TaskResponse, summary="Update user task")
def update_task(
    task_id: int, 
    task_update: TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.UserModel = Depends(get_current_user)
):
    # Search for task that belongs strictly to the current user
    task = db.query(models.TaskModel).filter(
        models.TaskModel.id == task_id,
        models.TaskModel.owner_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.title = task_update.title
    task.description = task_update.description
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=204, summary="Delete user task")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.UserModel = Depends(get_current_user)
):
    task = db.query(models.TaskModel).filter(
        models.TaskModel.id == task_id,
        models.taskModel.owner_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}