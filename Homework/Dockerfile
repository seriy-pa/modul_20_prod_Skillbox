FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app_my_first_django

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY my_first_django .

CMD ["python", "manage.py", "runserver"]
