FROM python:3.9

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN pip install --no-cache-dir pipenv
RUN pipenv install

ENTRYPOINT ["pipenv", "run", "python", "src/bot.py"]
