FROM ubuntu:14.04

MAINTAINER buda

RUN apt-get update
RUN apt-get install -y nginx
# RUN apt-get install -y python3-pip python3-dev build-essential
# RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
# RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
# RUN pip install cython uwsgi

ADD nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /opt/deploy/www/infinity
ADD web /opt/deploy/www/infinity/
RUN chown -R www-data:www-data /opt/deploy/www/infinity

EXPOSE 80

ENV TERM dumb

CMD ["nginx", "-g", "daemon off;"]
