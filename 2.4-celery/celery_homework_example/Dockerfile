FROM python:3.10
COPY ./app /app

WORKDIR /app
COPY requirements.txt /app
RUN apt update && apt install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir -r /app/requirements.txt
ENV PYTHONUNBUFFERED=TRUE

ENTRYPOINT gunicorn app:app --bind 0.0.0.0:5000 --capture-output