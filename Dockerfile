FROM python:3.13-rc-alpine
LABEL maintainer="Sinan Erdinc <hello@sinanerdinc.com>"

WORKDIR /app

RUN pip install opet

ENTRYPOINT ["opet-cli"]
