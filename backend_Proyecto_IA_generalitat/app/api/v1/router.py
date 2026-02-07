"""
API V1 Router configuration.

This module aggregates all the routers for version 1 of the API,
including authentication, chats, messages, and AI-related endpoints.
"""

from fastapi import APIRouter
from app.api.v1 import auth, chats, messages, ai

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(chats.router, prefix="/chats", tags=["chats"])
router.include_router(messages.router, prefix="/messages", tags=["messages"])
router.include_router(ai.router, prefix="/ai", tags=["ai"])
