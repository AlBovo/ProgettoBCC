FROM python:3.11.8-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
WORKDIR /src
EXPOSE 5000

CMD ["python", "main.py"]