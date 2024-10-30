FROM python:3.11

RUN apt update \
    && apt upgrade -y \
    && apt install -y curl \
        locales \
    && rm -rf /var/lib/apt/lists/* \
    && sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen

RUN pip3 install --no-cache-dir --upgrade pip \
    && pip install poetry
RUN pip install python-dotenv
RUN pip install uvicorn
RUN pip install greenlet
RUN apt-get update
RUN apt-get install -y ffmpeg libsm6 libxext6

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY backend/pyproject.toml .

RUN poetry install --no-dev || poetry install

COPY backend/. /app/backend/.
COPY .env /app/backend/.
WORKDIR /app/backend

VOLUME /app/backend/research_data


EXPOSE 8080

CMD ["python", "run.py"]