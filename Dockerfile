FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /project

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /project/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./project /project/

EXPOSE 8000

# Copy the script file into the container
COPY scripts/run.sh /project/scripts/run.sh
RUN chmod +x /project/scripts/run.sh


CMD ["/project/scripts/run.sh"]
