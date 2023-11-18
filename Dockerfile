FROM python:3.9

#
WORKDIR /code

#
COPY requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY app /code/app

EXPOSE 8011

WORKDIR /code/app/src

CMD ["python3", "initialize.py"]

WORKDIR /code/app/

CMD ["python3", "main.py"]
