FROM python:3.10

WORKDIR /home/gencaster

COPY requirements.txt .

RUN pip3 install --no-cache -r requirements.txt

COPY . .

RUN chmod +x start_server.sh

CMD [ "/bin/sh", "/home/gencaster/start_server.sh" ]
