from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query

from app.adapters.http.schemas import VideoCreate, VideoResponse
from app.usecase.videos import VideoService
from app.di import get_video_service


router = APIRouter(prefix="/videos")


@router.post("", response_model=VideoResponse)
async def create_video(
    video_create: VideoCreate,
    service: VideoService = Depends(get_video_service)
):
    video = await service.create_video(
        url=video_create.url,
        title=video_create.title,
        created_by=video_create.created_by,
    )
    return VideoResponse(**video.model_dump())


@router.get("/{clip_id}", response_model=VideoResponse)
async def get_video(
    clip_id: str,
    service: VideoService = Depends(get_video_service)
):
    video = await service.get_by_clip_id(clip_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return VideoResponse(**video.model_dump())


@router.get("", response_model=List[VideoResponse])
async def list_videos(
    limit: int = Query(default=100, ge=1, le=1000),
    service: VideoService = Depends(get_video_service)
):
    videos = await service.list_videos(limit=limit)
    return [VideoResponse(**v.model_dump()) for v in videos]


