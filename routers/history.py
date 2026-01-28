from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/history",
    tags=["history"],
)
