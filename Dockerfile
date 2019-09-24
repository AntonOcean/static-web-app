FROM python:3.7

COPY . /src

EXPOSE 80

WORKDIR /src

CMD python3.7 ./src/main.py