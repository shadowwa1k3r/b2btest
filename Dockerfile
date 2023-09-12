FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install python3-dev default-libmysqlclient-dev build-essential -y

COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN MYSQLCLIENT_CFLAGS="-I/usr/include/mysql" MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient" pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--config", "gunicorn-cfg.py", "b2broker.wsgi"]