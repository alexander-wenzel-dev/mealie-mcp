# syntax=docker/dockerfile:1

FROM python:3.14-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

RUN pip install --no-cache-dir uv

WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev --no-editable


FROM python:3.14-slim AS runtime

RUN groupadd --system app && useradd --system --gid app --home-dir /app app

WORKDIR /app
COPY --from=builder --chown=app:app /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH" \
    MEALIE_MCP_TRANSPORT=http \
    MEALIE_MCP_HTTP_HOST=0.0.0.0 \
    MEALIE_MCP_HTTP_PORT=8000

USER app
EXPOSE 8000

# Liveness only: hits /health over the loopback, so MEALIE_MCP_HTTP_ALLOWED_HOSTS
# must keep 127.0.0.1 (the default does).
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import os,sys,urllib.request; p=os.environ.get('MEALIE_MCP_HTTP_PORT','8000'); sys.exit(0 if urllib.request.urlopen(f'http://127.0.0.1:{p}/health').status==200 else 1)"]

CMD ["mealie-mcp"]
