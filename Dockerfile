FROM python:3.10.5

WORKDIR /usr/src/app

# copy all the files and directories to the container
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# run the command python -m app.main
CMD [ "python", "-m", "app.main" ]