FROM python:3.9.7-slim

EXPOSE 8000

ENV GUNICORN_CMD_ARGS --bind=0.0.0.0 --workers=2

VOLUME [ "/data" ]
ENV SQLITE_PATH=/data/meteosangue.sqlite3

RUN apt-get update && \
    apt-get install -y \
      gnupg2 \
      curl
RUN curl --silent 'https://deb.nodesource.com/gpgkey/nodesource.gpg.key' | apt-key add -
RUN echo 'deb http://deb.nodesource.com/node_12.x stretch main' >> /etc/apt/sources.list.d/node.list
RUN apt-get install -y \
      build-essential \
      locales \
      nodejs \
      npm && \
    npm install -g phantomjs-prebuilt && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Generate locales required by the application
RUN echo "it_IT.UTF-8 UTF-8\nen_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8

RUN chmod +x docker-startup.sh

ENV OPENSSL_CONF /dev/null
