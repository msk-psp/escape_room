FROM python:3.11-slim-buster

WORKDIR /app

COPY pyproject.toml uv.lock ./ 

RUN pip install uv && uv sync

COPY . .

ENV PATH="/app/.venv/bin:$PATH"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
