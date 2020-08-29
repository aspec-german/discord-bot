FROM python:3
# alpine has problems with yarl :(
WORKDIR /opt
COPY requirements.txt .
COPY .env .
RUN pip3 install -r requirements.txt
CMD ["python", "bot.py"]
