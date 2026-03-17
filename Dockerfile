# Base Image
FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Workdir
WORKDIR /app

# Copy dependencies first (cache)
COPY pyproject.toml uv.lock ./

# Install dependencies without installing the project
RUN uv sync --frozen --no-install-project

# Copy the rest of the code
COPY . .

# Install the project
RUN uv sync --frozen

# Run the project
CMD ["uv", "run", "python", "main.py"]