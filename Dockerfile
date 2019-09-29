FROM python:3.7

COPY . /src

EXPOSE 80
RUN pip install uvloop
WORKDIR /src

CMD python3.7 ./src/main.py