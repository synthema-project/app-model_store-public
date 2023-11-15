FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-2021-10-02
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD uvicorn main:app --host 0.0.0.0 --port 8000 --reload --root-path /api
