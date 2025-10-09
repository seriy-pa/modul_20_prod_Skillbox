FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app_my_first_django

RUN pip install --upgrade pip "poetry==2.2.1"

RUN poetry config virtualenvs.create false --local

COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY my_first_django .

CMD ["gunicorn", "my_first_django.wsgi:application", "--bind", "0.0.0.0:8000"]
