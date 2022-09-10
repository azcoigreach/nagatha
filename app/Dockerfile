FROM python:3.10.5

WORKDIR /usr/src/app

# copy all the files and directories to the container
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", " app.main:app", "--host", "0.0.0.0", "--port", "8000"]