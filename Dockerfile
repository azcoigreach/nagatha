FROM python:3.10.5

# adding trusted keys for dl-ssl.google.com
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# installing chrome
RUN apt-get update && apt-get install -y google-chrome-stable

# installing latest release of chromedriver
RUN LATEST=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    echo "Installing chromedriver ${LATEST}" && \
    wget -N https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -P ~/ && \
    unzip ~/chromedriver_linux64.zip -d ~/ && \
    rm ~/chromedriver_linux64.zip && \
    mv -f ~/chromedriver /usr/local/bin/chromedriver && \
    chown root:root /usr/local/bin/chromedriver && \
    chmod 0755 /usr/local/bin/chromedriver

WORKDIR /usr/src/app

# copy all the files and directories to the container
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# run the command python -m app.main
CMD [ "python", "-m", "app.main" ]