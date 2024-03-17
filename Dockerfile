# Django
FROM python:3.9-buster
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt-get update && apt-get install -y vim
WORKDIR /etc/uwsgi/room_402_django

RUN python3 -m pip install uwsgi uwsgi-tools -i https://pypi.tuna.tsinghua.edu.cn/simple/

ADD requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

ADD uwsgi.ini uwsgi.ini
ADD . /etc/uwsgi/room_402_django

EXPOSE 8086
CMD uwsgi --ini /etc/uwsgi/room_402_django/uwsgi.ini
