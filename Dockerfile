FROM python:latest as todolist

COPY ./requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY . /app

WORKDIR /app
EXPOSE 8000

CMD ["gunicorn", "web_server:app", "-b", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]