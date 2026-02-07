"""
Chat management API endpoints.

This module provides endpoints for creating, retrieving, updating, and deleting
chats for the authenticated user.
"""

from fastapi import APIRouter, Depends, HTTPException, Path, Body
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.schemas.chat import ChatResponse, CreateChatResponse, UpdateChatTitleRequest, UpdateChatStatusRequest
from app.services.chat_service import chat_service
from app.repositories.chat_repo import chat_repo

router = APIRouter()


@router.post("", response_model=CreateChatResponse)
def create_chat(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Create a new chat for the authenticated user.

    Args:
        db (Session): The database session.
        user (User): The authenticated user.

    Returns:
        CreateChatResponse: The ID of the newly created chat.
    """
    chat = chat_service.create_chat(db, user.id_usuario)
    return CreateChatResponse(id_chat=chat.id_chat)


@router.get("", response_model=list[ChatResponse])
def list_chats(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Retrieve all chats for the authenticated user.

    Args:
        db (Session): The database session.
        user (User): The authenticated user.

    Returns:
        list[ChatResponse]: A list of chats belonging to the user.
    """
    return chat_service.list_chats(db, user.id_usuario)


@router.get("/{chat_id}", response_model=ChatResponse)
def get_chat(
    chat_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Retrieve a specific chat (validates ownership).

    Args:
        chat_id (int): The ID of the chat to retrieve.
        db (Session): The database session.
        user (User): The authenticated user.

    Returns:
        ChatResponse: The chat details.

    Raises:
        HTTPException: If the chat is not found or does not belong to the user.
    """
    chat = chat_repo.get_for_user(db, chat_id, user.id_usuario)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.put("/{chat_id}/title", response_model=ChatResponse)
def update_chat_title(
    chat_id: int = Path(..., ge=1),
    request_body: UpdateChatTitleRequest = Body(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Update the title of a chat (validates ownership).

    Args:
        chat_id (int): The ID of the chat to update.
        request_body (UpdateChatTitleRequest): The new title.
        db (Session): The database session.
        user (User): The authenticated user.

    Returns:
        ChatResponse: The updated chat details.

    Raises:
        HTTPException: If the title is empty or the chat is not found.
    """
    if not request_body.title or not request_body.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    chat = chat_service.update_chat_title(db, chat_id, user.id_usuario, request_body.title.strip())
    return chat


@router.put("/{chat_id}/status", response_model=ChatResponse)
def update_chat_status(
    chat_id: int = Path(..., ge=1),
    request_body: UpdateChatStatusRequest = Body(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Update the status of a chat manually (for testing purposes).

    Args:
        chat_id (int): The ID of the chat to update.
        request_body (UpdateChatStatusRequest): The new status.
        db (Session): The database session.
        user (User): The authenticated user.

    Returns:
        ChatResponse: The updated chat details.

    Raises:
        HTTPException: If the chat is not found.
    """
    chat = chat_repo.get_for_user(db, chat_id, user.id_usuario)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    chat.status = request_body.status
    if request_body.status == "completed" and not chat.completed_at:
        from datetime import datetime
        chat.completed_at = datetime.now()
    elif request_body.status == "active":
        chat.completed_at = None
    
    db.commit()
    db.refresh(chat)
    return chat


@router.delete("/{chat_id}")
def delete_chat(
    chat_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Delete a chat (validates ownership).

    Args:
        chat_id (int): The ID of the chat to delete.
        db (Session): The database session.
        user (User): The authenticated user.

    Returns:
        dict: A success message.

    Raises:
        HTTPException: If the chat is not found.
    """
    chat = chat_repo.get_for_user(db, chat_id, user.id_usuario)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    chat_repo.delete(db, chat_id)
    return {"message": "Chat deleted successfully"}
