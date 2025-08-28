FROM python:3.12

WORKDIR /usr/src/app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /usr/src/app/

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]