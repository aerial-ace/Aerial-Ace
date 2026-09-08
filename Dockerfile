FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

COPY . .

CMD [ "uv", "run", "main.py" ]
