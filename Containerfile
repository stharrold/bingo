# Containerfile for bingo
# Python 3.11 + uv environment for development and CI/CD
#
# Build:  podman build -t bingo .
# Run:    podman run --rm -v .:/app bingo <command>
# Shell:  podman run --rm -it -v .:/app bingo bash

FROM python:3.11-slim

LABEL maintainer="stharrold"
LABEL description="Bingo card generator development environment with uv + Python 3.11"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
ENV UV_VERSION=0.5.5
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy dependency files first (for layer caching)
COPY pyproject.toml uv.lock* ./

# Create stub for editable install (source not yet copied)
RUN mkdir -p src/bingo && touch src/bingo/__init__.py README.md

# Install dependencies (--no-install-project to skip editable install)
RUN uv sync --frozen --no-install-project 2>/dev/null || uv sync --no-install-project

# Copy project files
COPY . .

# Install project in editable mode
RUN uv sync

# Set default command
CMD ["bash"]
