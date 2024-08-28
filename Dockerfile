FROM node:alpine as frontend-build

WORKDIR /app
COPY registry/frontend/ /app
RUN npm install && npm run build

FROM python:3.12-slim

ENV PYTHONPATH /app
ENV PYTHONUNBUFFERED 1

RUN pip3 install poetry

WORKDIR /app
COPY pyproject.toml /app

RUN poetry config virtualenvs.create false && \
    poetry install --with prod

COPY registry /app/registry
COPY --from=frontend-build /app/dist /app/registry/frontend/dist

EXPOSE 5000

CMD ["gunicorn", "-b", ":5000", "-t", "60", "-w", "4", "registry.app:app"]
