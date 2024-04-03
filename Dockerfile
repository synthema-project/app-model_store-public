FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim
WORKDIR /app
COPY src/requirements.txt src/requirements.txt
RUN pip install -r src/requirements.txt
COPY src src
EXPOSE 80
