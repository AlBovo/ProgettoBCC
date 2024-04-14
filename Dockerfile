FROM python:3.11.8-alpine

COPY requirements.txt .
RUN apk update
RUN apk add pkgconfig
RUN apk add --no-cache gcc musl-dev mariadb-connector-c-dev npm
RUN pip install --no-cache-dir -r requirements.txt

RUN npm install -D tailwindcss
RUN npx tailwindcss init
RUN npx tailwindcss -i ./src/static/input.css -o ./src/static/style.css

COPY src /src
WORKDIR /src

CMD ["python", "__init__.py"]