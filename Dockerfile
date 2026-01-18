FROM ghcr.io/astral-sh/uv:python3.11-trixie-slim AS builder

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv export > requirements.txt

FROM my-sam-base:latest

USER root
COPY --from=builder /app/requirements.txt .
# Install only the additional dependencies, excluding solace-agent-mesh since it's already in the base image
RUN grep -v "solace-agent-mesh" requirements.txt > requirements-filtered.txt && \
    python3.11 -m pip install --no-cache-dir -r requirements-filtered.txt

USER solaceai
COPY --chown=solaceai:solaceai configs/ /app/configs/
COPY --chown=solaceai:solaceai src/ /app/src/

WORKDIR /app

CMD ["run", "/app/configs"]
