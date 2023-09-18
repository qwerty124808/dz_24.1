FROM python:3.11

WORKDIR /code

COPY . /code/

RUN pip install -r requirements.txt --root-user-action=ignore

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]