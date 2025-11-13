# Deployment Guide: MongoDB Atlas + Render

This guide walks you through deploying your FastAPI services to Render using MongoDB Atlas as your database.

## Prerequisites

1. A GitHub account (or GitLab/Bitbucket)
2. A MongoDB Atlas account (free tier available)
3. A Render account (free tier available)

## Step 1: Set Up MongoDB Atlas

### 1.1 Create a MongoDB Atlas Account

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up for a free account
3. Complete the registration process

### 1.2 Create a Cluster

1. In the Atlas dashboard, click **"Build a Database"**
2. Choose the **FREE (M0) tier**
3. Select a cloud provider and region (choose one close to your Render region)
4. Give your cluster a name (e.g., `fastapi-cluster`)
5. Click **"Create Cluster"**

### 1.3 Configure Database Access

1. Go to **Database Access** in the left sidebar
2. Click **"Add New Database User"**
3. Choose **"Password"** authentication
4. Enter a username and password (save these securely!)
5. Set user privileges to **"Atlas Admin"** (or more restrictive if preferred)
6. Click **"Add User"**

### 1.4 Configure Network Access

1. Go to **Network Access** in the left sidebar
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (for development) or add Render's IP ranges
   - **For production**: Add specific IP ranges for better security
   - **For development**: Use `0.0.0.0/0` to allow all IPs
4. Click **"Confirm"**

### 1.5 Get Your Connection String

1. Go to **Database** in the left sidebar
2. Click **"Connect"** on your cluster
3. Choose **"Connect your application"**
4. Select **Python** and version **3.11 or later**
5. Copy the connection string (it looks like):
   ```
   mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
   ```
6. Replace `<username>` and `<password>` with your actual credentials
7. Add your database name at the end (replace `?` with `/<database-name>?` if not using default):
   ```
   mongodb+srv://username:password@cluster.mongodb.net/tags_db?retryWrites=true&w=majority
   ```

## Step 2: Deploy Services to Render

You'll need to deploy each service separately on Render. Here's how to deploy each one:

### 2.1 Deploy Tags Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your repository (GitHub/GitLab/Bitbucket)
4. Select your repository and branch
5. **IMPORTANT**: Configure the service:
   - **Name**: `tags-service` (or your preferred name)
   - **Region**: Choose a region close to your users
   - **Root Directory**: `tags-service` ⚠️ **This is critical!** Set this to the service directory name
   - **Environment**: `Docker` ⚠️ **Must be Docker, not Python**
   - **Build Command**: (leave empty, Docker handles this)
   - **Start Command**: (leave empty, Dockerfile CMD handles this)
   
   **Note**: If you don't set **Root Directory** to `tags-service`, Render will look for a Dockerfile in the root directory and fail with "no such file or directory" error.

6. **Add Environment Variables**:
   ```
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/tags_db?retryWrites=true&w=majority
   MONGODB_DATABASE=tags_db
   PORT=8000
   ```

7. Click **"Create Web Service"**
8. Render will build and deploy your service

### 2.2 Deploy Moderate Service

1. Repeat steps 1-4 from above
2. **IMPORTANT**: Configure the service:
   - **Name**: `moderate-service`
   - **Root Directory**: `moderate-service` ⚠️ **Must match the directory name**
   - **Environment**: `Docker` ⚠️ **Must be Docker**

3. **Add Environment Variables**:
   ```
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/tags_db?retryWrites=true&w=majority
   MONGODB_DATABASE=tags_db
   JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
   PORT=8002
   ```

4. Click **"Create Web Service"**

### 2.3 Deploy Videos Service

1. Repeat steps 1-4 from above
2. **IMPORTANT**: Configure the service:
   - **Name**: `videos-service`
   - **Root Directory**: `videos-service` ⚠️ **Must match the directory name**
   - **Environment**: `Docker` ⚠️ **Must be Docker**

3. **Add Environment Variables**:
   ```
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/tags_db?retryWrites=true&w=majority
   MONGODB_DATABASE=tags_db
   PORT=8000
   ```

4. Click **"Create Web Service"**

## Step 3: Environment Variables Reference

Each service requires these environment variables:

### Common Variables (All Services)
- `MONGODB_URL`: Your MongoDB Atlas connection string
- `MONGODB_DATABASE`: Database name (e.g., `tags_db`)

### Service-Specific Variables

**Tags Service:**
- `PORT`: Port number (default: 8000, Render sets this automatically)

**Moderate Service:**
- `PORT`: Port number (default: 8002, Render sets this automatically)
- `JWT_SECRET`: Secret key for JWT tokens (use a strong random string)

**Videos Service:**
- `PORT`: Port number (default: 8000, Render sets this automatically)

## Step 4: Verify Deployment

After deployment, test each service:

1. **Tags Service**: `https://tags-service.onrender.com/health`
2. **Moderate Service**: `https://moderate-service.onrender.com/health`
3. **Videos Service**: `https://videos-service.onrender.com/health`

Each should return: `{"status": "ok"}`

## Step 5: Local Development Setup

For local development with MongoDB Atlas:

1. Create a `.env` file in each service directory (or root directory):
   ```bash
   # .env
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/tags_db?retryWrites=true&w=majority
   MONGODB_DATABASE=tags_db
   JWT_SECRET=your-local-jwt-secret
   ```

2. Run services using docker-compose:
   ```bash
   # Set environment variables
   export MONGODB_URL="mongodb+srv://username:password@cluster.mongodb.net/tags_db?retryWrites=true&w=majority"
   export MONGODB_DATABASE="tags_db"
   export JWT_SECRET="your-local-jwt-secret"
   
   # Start services
   docker-compose up --build
   ```

   Or run individually:
   ```bash
   cd tags-service
   docker build -t tags-service .
   docker run -p 8001:8000 -e MONGODB_URL="your-atlas-url" -e MONGODB_DATABASE="tags_db" tags-service
   ```

## Important Notes

### Security Best Practices

1. **Never commit `.env` files** to Git - add them to `.gitignore`
2. **Use strong JWT secrets** in production (generate with: `openssl rand -hex 32`)
3. **Restrict MongoDB Atlas network access** to Render IPs in production
4. **Use MongoDB Atlas database users** with minimal required privileges
5. **Enable MongoDB Atlas encryption** at rest (available on paid tiers)

### Render Considerations

1. **Free Tier Limitations**:
   - Services spin down after 15 minutes of inactivity
   - First request after spin-down may take 30-60 seconds
   - Upgrade to paid tier for always-on services

2. **Custom Domains**: You can add custom domains in Render dashboard for each service

3. **Auto-Deploy**: Render automatically deploys on git push (can be disabled)

4. **Health Checks**: Configure health check endpoints in Render dashboard (e.g., `/health`)

### MongoDB Atlas Considerations

1. **Free Tier Limits**:
   - 512 MB storage
   - Shared CPU and RAM
   - Perfect for development and small projects

2. **Connection Pooling**: Your connection string supports connection pooling by default

3. **Monitoring**: Use Atlas dashboard to monitor database performance

4. **Backups**: Free tier includes automated daily backups (keep for 2 days)

## Troubleshooting

### Connection Issues

- **"Authentication failed"**: Check username/password in connection string
- **"Connection timeout"**: Verify network access includes Render IPs
- **"DNS resolution failed"**: Ensure you're using the `mongodb+srv://` protocol

### Render Deployment Issues

- **"failed to read dockerfile: open Dockerfile: no such file or directory"**:
  - ✅ **Solution**: Make sure **Root Directory** is set correctly (e.g., `tags-service`, not empty or root)
  - ✅ Check that **Environment** is set to `Docker` (not `Python` or `Node`)
  - The Root Directory tells Render where to find the Dockerfile
  
- **Build fails**: 
  - Check Dockerfile syntax and requirements.txt
  - Verify the Root Directory path is correct
  - Check that all files referenced in Dockerfile exist in that directory
  
- **Service crashes**: Check logs in Render dashboard

- **Port issues**: Render sets `PORT` automatically, ensure your Dockerfile uses it

### Database Issues

- **Collection not found**: MongoDB creates collections automatically on first write
- **Connection pool exhausted**: Reduce connection pool size in your MongoDB driver settings

## Support Resources

- [Render Documentation](https://render.com/docs)
- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

