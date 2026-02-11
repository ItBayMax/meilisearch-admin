# =============================================================================
# Meilisearch Admin - Multi-stage Dockerfile
# =============================================================================
# Stage 1: Build frontend with Node.js
# Stage 2: Production runtime with Python + Nginx
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Frontend Builder
# -----------------------------------------------------------------------------
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files first for better caching
COPY frontend/package*.json ./

# Install dependencies
RUN npm set registry=https://registry.npmmirror.com

# Copy frontend source and build
COPY frontend/ ./
RUN rm -rf node_modules && npm install && npm run build


# -----------------------------------------------------------------------------
# Stage 2: Production Runtime
# -----------------------------------------------------------------------------
FROM python:3.10-slim AS runtime

LABEL maintainer="Meilisearch Admin"
LABEL description="Web-based administration interface for Meilisearch"

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Shanghai \
    FLASK_ENV=production

WORKDIR /app

# Install system dependencies and nginx
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    supervisor \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy Python requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    -i https://pypi.tuna.tsinghua.edu.cn/simple

# Copy backend source
COPY backend/ ./backend/
COPY config/ ./config/

# Copy frontend build from builder stage
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist/

# Copy nginx and supervisor configuration
COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create directories for data and logs
RUN mkdir -p /app/data /app/logs \
    && chown -R www-data:www-data /app

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/api/health || exit 1

# Start supervisor (manages nginx + gunicorn)
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]


# =============================================================================
# Build Command:
#   docker build -t meilisearch-admin:latest .
#
# Run Command:
#   docker run -d -p 8080:80 \
#     -v $(pwd)/data:/app/data \
#     -v $(pwd)/logs:/app/logs \
#     --name meilisearch-admin \
#     meilisearch-admin:latest
# =============================================================================
