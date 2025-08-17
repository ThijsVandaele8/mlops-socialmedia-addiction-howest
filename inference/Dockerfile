FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY ../dist ./dist
RUN pip install ./dist/socialmedia_mlops-0.1.2-py3-none-any.whl

COPY ./inference .
COPY ../models ./models

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]