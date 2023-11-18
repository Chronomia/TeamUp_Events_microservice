FROM python:3.9-slim

#
WORKDIR /code

#
COPY requirements.txt requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app app

WORKDIR /code/app

EXPOSE 8011

RUN chmod +x start.sh
CMD ["bash", "./start.sh"]
