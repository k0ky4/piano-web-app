FROM python:3.11.2-alpine3.16

COPY requirements.txt /app/
COPY static /app/static
COPY templates /app/templates
COPY *.py /app/

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]