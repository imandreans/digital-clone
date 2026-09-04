#Installing UV in Docker

FROM python:3.12-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:0.11.26 /uv /uvx /bin/

WORKDIR /app

COPY *.py pyproject.toml uv.lock /app/

ADD cv.txt /app/

# Installing needed dependencies
RUN uv sync --locked 

EXPOSE 7860

CMD ["uv", "run", "python", "main.py"]