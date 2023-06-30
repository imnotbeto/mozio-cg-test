FROM python:3.10-slim as base

ENV PIPENV_VENV_IN_PROJECT=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --dev --system --deploy

COPY . ./

CMD ["python3", "main.py"]
