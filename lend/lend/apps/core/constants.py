dockerfile = '''
FROM python:2.7

MAINTAINER Jonnatas Matias <matiasjonnatas@gmail.com>

EXPOSE 8000

VOLUME /data

CMD ["/bin/sh"]

'''

base_url='unix://var/run/docker.sock'