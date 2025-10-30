from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query

from app.adapters.http.schemas import TagResponse, ModerationRequest
from app.di import get_moderation_service
from app.usecase.moderation import ModerationService
from app.adapters.http.auth_router import get_current_moderator
from app.domain.entities import User


router = APIRouter(prefix="")


@router.get("/pending", response_model=List[TagResponse])
async def list_pending_tags(
    limit: int = Query(default=100, ge=1, le=1000),
    moderation_service: ModerationService = Depends(get_moderation_service),
    _: User = Depends(get_current_moderator),
):
    tags = await moderation_service.list_pending(limit=limit)
    return [TagResponse(**t.model_dump()) for t in tags]


@router.post("/moderate/{tag_id}", response_model=TagResponse)
async def moderate_tag(
    tag_id: str,
    req: ModerationRequest,
    moderation_service: ModerationService = Depends(get_moderation_service),
    moderator: User = Depends(get_current_moderator),
):
    updated = await moderation_service.moderate_tag(
        tag_id=tag_id,
        status=req.status,
        moderator_username=moderator.username,
        note=req.note,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Tag not found")
    return TagResponse(**updated.model_dump())


