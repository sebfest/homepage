FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --group dev --no-install-project
COPY . /app/
