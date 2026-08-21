FROM python:3.12-slim

RUN pip install uv

WORKDIR /app

COPY backend/pyproject.toml backend/uv.lock ./

RUN uv sync

COPY ./backend .

CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0"]
