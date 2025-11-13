# FastAPI Microservices - Tags, Videos & Moderation Service

A microservices architecture built with FastAPI, MongoDB Atlas, and Docker. This project demonstrates Clean Architecture principles with three independent services: **Tags Service**, **Videos Service**, and **Moderation Service**.

## 🏗️ Architecture Overview

This project consists of three microservices:

- **Tags Service** (Port 8001) - Manages timestamped tags on video clips
- **Videos Service** (Port 8003) - Manages video clips metadata
- **Moderation Service** (Port 8002) - Handles user authentication and tag moderation
- **NGINX** (Port 8080) - Optional load balancer for local development

All services share a MongoDB database (MongoDB Atlas in production, local MongoDB for development).

## 🚀 Quick Start

### Prerequisites

- **Docker** and **Docker Compose** installed ([Download Docker](https://www.docker.com/get-started))
- **MongoDB Atlas account** (for production deployment) - [Sign up for free](https://www.mongodb.com/cloud/atlas)
- **Git** for cloning the repository

### Local Development Setup

#### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd assignda
```

#### 2. Set Environment Variables

Create a `.env` file in the root directory (or set environment variables):

```bash
# For local MongoDB (default)
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=tags_db

# For MongoDB Atlas (production)
# MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/tags_db?retryWrites=true&w=majority

# JWT Secret (for moderate service)
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
```

**Note**: If you're using MongoDB Atlas locally, replace `MONGODB_URL` with your Atlas connection string.

#### 3. Build and Run with Docker Compose

```bash
# Build all services
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

#### 4. Verify Services are Running

Check health endpoints:

- **Tags Service**: http://localhost:8001/health
- **Moderation Service**: http://localhost:8002/health
- **Videos Service**: http://localhost:8003/health
- **NGINX Load Balancer**: http://localhost:8080

#### 5. Access API Documentation

Each service provides interactive API documentation:

- **Tags Service**: http://localhost:8001/docs
- **Moderation Service**: http://localhost:8002/docs
- **Videos Service**: http://localhost:8003/docs

## 📋 Services Details

### Tags Service (Port 8001)

Manages timestamped tags on video clips.

**API Endpoints:**
- `POST /tags` - Create a new tag
- `GET /tags/clip/{clip_id}` - Get all tags for a specific clip
- `GET /tags/{tag_id}` - Get a specific tag by ID
- `DELETE /tags/{tag_id}` - Delete a tag
- `GET /health` - Health check

**Environment Variables:**
- `MONGODB_URL` - MongoDB connection URL
- `MONGODB_DATABASE` - Database name (default: `tags_db`)

### Videos Service (Port 8003)

Manages video clips metadata.

**API Endpoints:**
- `POST /videos` - Create a new video
- `GET /videos/{clip_id}` - Get video by ID
- `GET /health` - Health check

**Environment Variables:**
- `MONGODB_URL` - MongoDB connection URL
- `MONGODB_DATABASE` - Database name (default: `tags_db`)

### Moderation Service (Port 8002)

Handles user authentication and tag moderation.

**API Endpoints:**

**Authentication:**
- `POST /auth/register` - Register a new user
- `POST /auth/token` - Login and get JWT token

**Moderation** (requires authentication):
- `GET /moderation/pending` - List pending tags for moderation
- `POST /moderation/{tag_id}` - Approve or reject a tag

**Environment Variables:**
- `MONGODB_URL` - MongoDB connection URL
- `MONGODB_DATABASE` - Database name (default: `tags_db`)
- `JWT_SECRET` - Secret key for JWT token signing (required)

**User Roles:**
- `USER` - Regular user
- `MODERATOR` - Can moderate tags

## 🔧 Configuration

### Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `MONGODB_URL` | MongoDB connection string | `mongodb://localhost:27017` | Yes |
| `MONGODB_DATABASE` | Database name | `tags_db` | No |
| `JWT_SECRET` | JWT signing secret (moderate service only) | - | Yes (moderate) |

### MongoDB Connection Strings

**Local MongoDB:**
```
mongodb://localhost:27017
```

**MongoDB Atlas:**
```
mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority
```

Replace:
- `username` - Your MongoDB Atlas username
- `password` - Your MongoDB Atlas password
- `cluster` - Your cluster name
- `database` - Database name

## ☁️ Production Deployment (Render)

### Prerequisites

- GitHub/GitLab/Bitbucket repository
- MongoDB Atlas cluster (see setup below)
- Render account ([Sign up for free](https://render.com))

### Step 1: Set Up MongoDB Atlas

1. **Create Account**: Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and sign up
2. **Create Cluster**: Click "Build a Database" → Choose FREE (M0) tier → Select region → Create
3. **Database Access**: Go to "Database Access" → Add user → Create username/password → Save credentials
4. **Network Access**: Go to "Network Access" → Add IP Address → Allow from anywhere (`0.0.0.0/0`) for development, or add Render IPs for production
5. **Get Connection String**: Go to "Database" → Connect → Connect your application → Copy connection string

   Format: `mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority`

### Step 2: Deploy to Render

Deploy each service separately on Render:

#### Deploy Tags Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your repository
4. Configure:
   - **Name**: `tags-service`
   - **Region**: Choose closest to users
   - **Root Directory**: `tags-service` ⚠️ **CRITICAL**
   - **Environment**: `Docker` ⚠️ **MUST be Docker**
   - **Build Command**: (leave empty)
   - **Start Command**: (leave empty)
5. **Environment Variables**:
   ```
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/tags_db?retryWrites=true&w=majority
   MONGODB_DATABASE=tags_db
   ```
6. Click **"Create Web Service"**

#### Deploy Moderate Service

1. Repeat steps 1-3 above
2. Configure:
   - **Name**: `moderate-service`
   - **Root Directory**: `moderate-service` ⚠️ **CRITICAL**
   - **Environment**: `Docker` ⚠️ **MUST be Docker**
3. **Environment Variables**:
   ```
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/tags_db?retryWrites=true&w=majority
   MONGODB_DATABASE=tags_db
   JWT_SECRET=your-strong-random-secret-here
   ```
   **Generate JWT Secret**: `openssl rand -hex 32`
4. Click **"Create Web Service"**

#### Deploy Videos Service

1. Repeat steps 1-3 above
2. Configure:
   - **Name**: `videos-service`
   - **Root Directory**: `videos-service` ⚠️ **CRITICAL**
   - **Environment**: `Docker` ⚠️ **MUST be Docker**
3. **Environment Variables**:
   ```
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/tags_db?retryWrites=true&w=majority
   MONGODB_DATABASE=tags_db
   ```
4. Click **"Create Web Service"**


## 🧪 Testing

### Test Health Endpoints

```bash
# Tags Service
curl http://localhost:8001/health

# Moderation Service
curl http://localhost:8002/health

# Videos Service
curl http://localhost:8003/health
```

### Test API Endpoints

**1. Register a user (Moderation Service):**
```bash
curl -X POST http://localhost:8002/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123",
    "role": "USER"
  }'
```

**2. Login (Moderation Service):**
```bash
curl -X POST http://localhost:8002/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"
```

**3. Create a video (Videos Service):**
```bash
curl -X POST http://localhost:8003/videos \
  -H "Content-Type: application/json" \
  -d '{
    "clip_id": "video123",
    "title": "Test Video",
    "description": "A test video"
  }'
```

**4. Create a tag (Tags Service):**
```bash
curl -X POST http://localhost:8001/tags \
  -H "Content-Type: application/json" \
  -d '{
    "clip_id": "video123",
    "timestamp": 120.5,
    "text": "Important moment"
  }'
```



## 📁 Project Structure

```
assignda/
├── docker-compose.yml          # Docker Compose configuration
├── README.md                   # This file
│
├── tags-service/               # Tags microservice
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── adapters/          # HTTP adapters, repositories
│       ├── domain/            # Business entities
│       ├── infrastructure/    # Database, security
│       └── usecase/           # Business logic
│
├── moderate-service/           # Moderation microservice
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/                   # Same structure as tags-service
│
├── videos-service/             # Videos microservice
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/                   # Same structure as tags-service
│
└── nginx/                      # NGINX load balancer (optional)
    ├── Dockerfile
    └── nginx.conf
```



## 📚 Technology Stack

- **FastAPI** - Modern Python web framework
- **MongoDB** - NoSQL database (Atlas in production)
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation
- **Python-JOSE** - JWT authentication
- **Uvicorn** - ASGI server
- **Docker** - Containerization
- **NGINX** - Load balancer (optional)



**Happy Coding! 🚀**

