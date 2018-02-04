FROM python:3.6.3
WORKDIR /app
ADD . /app
RUN apt-get update \
    && apt-get -y install tesseract-ocr
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 8080
CMD hupper -m server
