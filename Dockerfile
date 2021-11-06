FROM python:3.9.7-slim-buster as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PATH=/home/ncuser/.local/bin:$PATH
ENV FT_APP_ENV="docker"

# Prepare environment
RUN mkdir /nagatha \
  && apt-get update \
  && apt-get -y install sudo curl \
  && apt-get clean \
  && useradd -u 1000 -G sudo -U -m -s /bin/bash ncuser \
  && chown ncuser:ncuser /nagatha \
  # Allow sudoers
  && echo "ncuser ALL=(ALL) NOPASSWD: /bin/chown" >> /etc/sudoers

WORKDIR /nagatha

# Install dependencies
FROM base as python-deps
RUN  apt-get update \
  && apt-get -y install build-essential git \
  && apt-get clean \
  && pip install --upgrade pip

USER ncuser
# Install and execute
COPY --chown=ncuser:ncuser . /nagatha/
RUN pip install --editable .

ENTRYPOINT ["nagatha"]
# Default Command
CMD [ "nagatha" ]
