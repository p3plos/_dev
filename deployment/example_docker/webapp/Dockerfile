
FROM python:3.10-alpine

RUN pip3 install pipenv

WORKDIR /app

COPY /Pipfile      /app/Pipfile
COPY /Pipfile.lock /app/Pipfile.lock

RUN pipenv install --system --deploy --ignore-pipfile

COPY . /app

ENTRYPOINT ["python"]
CMD ["app.py"]
