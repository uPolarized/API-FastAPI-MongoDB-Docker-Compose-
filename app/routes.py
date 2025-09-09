# app/routes.py
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from bson import ObjectId 

import crud
from database import get_database
from schemas import UserCreate, UserUpdate, UserResponse, PaginatedUserResponse


router = APIRouter()

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user"
)
async def create_new_user(
    user: UserCreate = Body(...),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    created_user = await crud.create_user(db, user)
    if created_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    return created_user

@router.get(
    "/",
    response_model=PaginatedUserResponse,
    summary="List users with filters and pagination"
)
async def list_users(
    db: AsyncIOMotorDatabase = Depends(get_database),
    q: str = Query(None, description="Search text for user name"),
    min_age: int = Query(None, description="Minimum age filter"),
    max_age: int = Query(None, description="Maximum age filter"),
    is_active: bool = Query(None, description="Filter by active status"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
):
    users, total = await crud.get_users(db, q, min_age, max_age, is_active, page, limit)
    return PaginatedUserResponse(total=total, page=page, limit=limit, data=users)

@router.get(
    "/{id}",
    response_model=UserResponse,
    summary="Get a single user by ID"
)

async def get_single_user(
    id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid ObjectId format: {id}")

    user = await crud.get_user_by_id(db, id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user

@router.put(
    "/{id}",
    response_model=UserResponse,
    summary="Update an existing user"
)

async def update_existing_user(
    id: str,
    user_update: UserUpdate = Body(...),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid ObjectId format: {id}")
        
    result = await crud.update_user(db, id, user_update)
    if result["matched_count"] == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
    updated_user = await crud.get_user_by_id(db, id)
    return updated_user

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user"
)

async def delete_existing_user(
    id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid ObjectId format: {id}")
        
    deleted_count = await crud.delete_user(db, id)
    if deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return None