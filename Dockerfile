FROM python:3.12


RUN pip3 install --no-cache-dir --upgrade pip \
    && pip install poetry
RUN pip install uvicorn
RUN apt-get update

# Отключение создания виртуальной среды Poetry
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt install make

WORKDIR /app
COPY backend/pyproject.toml .

RUN poetry install --no-dev || poetry install

COPY backend/. /app/backend/.
COPY .env /app/backend/.
WORKDIR /app/backend

VOLUME /app/backend/research_data

EXPOSE 8080

CMD ["python", "run.py"]