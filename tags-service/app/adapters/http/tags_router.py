from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.adapters.http.schemas import TagCreate, TagResponse, TagUpdate
from app.di import get_tag_service
from app.usecase.tags import TagService

router = APIRouter(prefix="/tags")

@router.post("", response_model=TagResponse)
async def create_tag(
    tag_create: TagCreate,
    tag_service: TagService = Depends(get_tag_service)
):
    tag = await tag_service.create_tag(
        clip_id=tag_create.clip_id,
        tag_text=tag_create.tag_text,
        timestamp=tag_create.timestamp,
        created_by=tag_create.created_by
    )
    return TagResponse(**tag.model_dump())

@router.post("", response_model=TagResponse)
async def create_tag(
    tag_create: TagCreate,
    tag_service: TagService = Depends(get_tag_service)
):
    tag = await tag_service.create_tag(
        clip_id=tag_create.clip_id,
        tag_text=tag_create.tag_text,
        timestamp=tag_create.timestamp,
        created_by=tag_create.created_by
    )
    return TagResponse(**tag.model_dump())


@router.get("/clip/{clip_id}", response_model=List[TagResponse])
async def get_tags_by_clip_id(
    clip_id: str,
    tag_service: TagService = Depends(get_tag_service)
):
    tags = await tag_service.get_tags_by_clip_id(clip_id)
    return [TagResponse(**tag.model_dump()) for tag in tags]


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag_by_id(
    tag_id: str,
    tag_service: TagService = Depends(get_tag_service)
):
    tag = await tag_service.get_tag_by_id(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return TagResponse(**tag.model_dump())


@router.delete("/{tag_id}")
async def delete_tag(
    tag_id: str,
    tag_service: TagService = Depends(get_tag_service)
):
    deleted = await tag_service.delete_tag(tag_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tag deleted successfully"}


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: str,
    tag_update: TagUpdate,
    tag_service: TagService = Depends(get_tag_service)
):
    updated_tag = await tag_service.update_tag(
        tag_id=tag_id,
        tag_text=tag_update.tag_text,
        timestamp=tag_update.timestamp
    )
    if not updated_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return TagResponse(**updated_tag.model_dump())