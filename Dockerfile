FROM python:3.11

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY /api ./api


CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
