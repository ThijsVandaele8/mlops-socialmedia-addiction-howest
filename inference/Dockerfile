FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

ARG SOCIALMEDIA_WHEEL_URL
RUN test -n "$SOCIALMEDIA_WHEEL_URL" || (echo "SOCIALMEDIA_WHEEL_URL is required" && exit 1) \
    && pip install --no-cache-dir "$SOCIALMEDIA_WHEEL_URL"

COPY ./inference .
COPY ../models ./models

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]