FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install python-multipart
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD python main.py
