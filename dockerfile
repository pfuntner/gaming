FROM python:2.7
WORKDIR /root

COPY waiter.py /tmp
COPY history /tmp

RUN apt update && apt install -y vim less openssh-server sudo sshpass ansible
# RUN systemctl enable ssh
# RUN mkdir -p /run/sshd
RUN pip install requests

cmd ["python", "/tmp/waiter.py"]
