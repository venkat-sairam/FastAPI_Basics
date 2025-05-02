FROM python:3.11-slim

# Install curl, bash, and netcat — MUST go BEFORE anything that might fail silently
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates bash netcat-openbsd && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


# Install uv
RUN curl -Ls https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Set workdir
WORKDIR /app

# Add wait-for-it.sh
COPY ./scripts/wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Install deps
COPY pyproject.toml ./
RUN uv pip install --system -r pyproject.toml

# Copy app
COPY ./src /app
