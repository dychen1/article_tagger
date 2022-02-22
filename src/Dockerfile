FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN mkdir /src
WORKDIR /src
COPY . /src
COPY ./requirements.txt /src/requirements.txt

RUN python3 -m pip install --no-cache-dir -r /src/requirements.txt
ENV FLASK_APP=/src/article_tagger.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000
ENTRYPOINT ["python3", "-m", "flask", "run"]
