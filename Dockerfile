FROM python:3.10.4

WORKDIR /home/app/bot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get -y install postgresql gcc python3-dev musl-dev redis-server

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT [ "/bin/bash", "-c", "`cat entrypoint.sh`"]
