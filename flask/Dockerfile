FROM python:3.7.7-stretch
RUN useradd -rm -d /home/irteam -s /bin/bash -g root -G sudo -u 1000 irteam

RUN mkdir /app
WORKDIR /app
ADD . /app
RUN pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org
RUN pip3 install -r requirements.txt

ARG ENV
ENV FLASK_ENV $ENV
ENV FLASK_APP /app/run.py

CMD ["nohup", "python3", "run.py", ">", "/home/irteam/logs/output.log", "&"]