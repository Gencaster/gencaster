FROM python:3.8

WORKDIR /home/gencaster

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY gencaster/ .

RUN chmod +x start_server.sh

CMD [ "/bin/sh", "/gencaster/start_server.sh" ]
