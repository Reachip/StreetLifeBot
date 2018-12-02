FROM python:3.6
WORKDIR /street-life-bot
COPY . .
RUN pip install -r requirements.txt
CMD python bot 