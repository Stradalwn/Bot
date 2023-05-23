FROM python:3.10.6-slim-buster

COPY . .

RUN apt-get update && \
    apt-get install -y python3-venv && \
    python3 -m venv env && \
    env/bin/pip install --upgrade pip && \
    env/bin/pip install -r requirements.txt

CMD ["env/bin/python3", "main.py"]
