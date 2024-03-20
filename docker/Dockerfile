FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim
WORKDIR /app
COPY ../requirements.txt .
RUN pip install python-multipart
RUN pip install -r requirements.txt
COPY ../src .
EXPOSE 5003
CMD python src/main.py
