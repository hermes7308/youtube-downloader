FROM python:3.7.7-stretch
RUN useradd -rm -d /home/irteam -s /bin/bash -g root -G sudo -u 1000 irteam

ARG ENV
RUN export FLASK_ENV=$ENV
RUN echo $ENV
RUN export FLASK_APP=run.py

RUN mkdir /app
WORKDIR /app
ADD . /app
RUN pip3 install -r requirements.txt

CMD ["nohup", "python3", "run.py", ">", "/home/irteam/logs/youtube-downloader.output.log", "&"]