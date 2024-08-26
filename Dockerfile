FROM node:alpine as frontend-build

WORKDIR /app
COPY ./registry/frontend/ /app
RUN npm install && npm run build

FROM python:3.12-slim

ENV PYTHONPATH /app
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY ./registry/ /app
COPY ./requirements.txt /app
COPY --from=frontend-build /app/dist /app/frontend/dist

RUN pip3 install --trusted-host pypi.python.org -r /app/requirements.txt &&\
    pip3 install --trusted-host pypi.python.org gunicorn

EXPOSE 5000

CMD ["gunicorn", "-b", ":5000", "-t", "60", "-w", "4", "app:app"]
