FROM python:3.11.8-alpine

COPY requirements.txt .
RUN apk update
RUN apk add pkgconfig
RUN apk add --no-cache gcc musl-dev mariadb-connector-c-dev
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
WORKDIR /src
EXPOSE 5000

CMD ["python", "main.py"]