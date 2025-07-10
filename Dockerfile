FROM python:3.13.5-slim

RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/root/.cache/pip \
    apt-get update && \
    apt-get install -y \
        git && \
    pip install gunicorn && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install /app

# EXPOSE 5000

CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsctables:app"]