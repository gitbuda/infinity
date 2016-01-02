FROM ubuntu:14.04

MAINTAINER buda

RUN apt-get update
RUN apt-get install -y nginx

ADD nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /opt/deploy/www/infinity
ADD web /opt/deploy/www/infinity/
RUN chown -R www-data:www-data /opt/deploy/www/infinity

ENV TERM dumb

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
