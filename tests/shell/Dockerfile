# uvツール用
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS uv

FROM python:3.13-slim
COPY --from=uv /usr/local/bin/uv /usr/local/bin/uvx /usr/local/bin/
