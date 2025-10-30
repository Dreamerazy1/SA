# Tags Service

A microservice for managing timestamped tags on video clips.

## Features

- Create tags with timestamps for specific video clips
- Retrieve all tags for a specific clip
- Get a specific tag by ID
- Delete tags

## API Endpoints

- `POST /tags` - Create a new tag
- `GET /tags/clip/{clip_id}` - Get all tags for a specific clip
- `GET /tags/{tag_id}` - Get a specific tag by ID
- `DELETE /tags/{tag_id}` - Delete a tag

## Running the Service

The service is part of the main docker-compose setup. To run it:

```bash
docker-compose up -d
```

The service will be available at: http://localhost:8001

## Environment Variables

- `MONGODB_URL` - MongoDB connection URL
- `MONGODB_DATABASE` - MongoDB database name