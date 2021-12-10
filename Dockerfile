FROM python:3.9-slim-bullseye

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

COPY . ./

ENV PORT=5000

CMD ["gunicorn", "predict:app"]