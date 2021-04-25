FROM python:3

COPY assets/ /opt/resource/
RUN chmod +x /opt/resource/*

COPY requirements.txt /
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
