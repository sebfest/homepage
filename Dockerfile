FROM python:3.10
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements/requirements.txt ./requirements.txt
RUN pip install --upgrade --quiet pip setuptools && pip install --no-cache-dir --quiet -r requirements.txt
COPY . /app/