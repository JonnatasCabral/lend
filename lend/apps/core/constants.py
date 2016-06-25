dockerfile = '''
FROM python:2.7

EXPOSE 8000

WORKDIR /home/codes/

CMD ["/bin/bash"]

'''

base_url = 'unix://var/run/docker.sock'
