FROM python:3.13.3
WORKDIR /
ENV PYTHONUNBUFFERED=1
COPY .env .env
COPY start.sh start.sh
RUN apt-get update && apt-get install -y git

ENTRYPOINT [ "/start.sh" ]