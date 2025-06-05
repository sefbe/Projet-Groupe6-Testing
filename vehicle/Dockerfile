# Dockerfile

FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# pour installer netcat
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean


# Copie du script d'entrée
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]

