# -*- coding: utf-8 -*-

dockerfile = '''
FROM python:2.7
MAINTAINER Jonnatas Matias <matiasjonnatas@gmail.com>

EXPOSE 8000

WORKDIR /home/codes/

RUN pip install unicodecsv

VOLUME /tmp/codes/:/home/codes/

CMD ["/bin/bash"]
'''

base_url = 'unix://var/run/docker.sock'

editor_initial_comment = '''
\'\'\'
Using your CSV/JSON data:

from lendcsv import read_file

data = read_file(
    file_type,
    delimiter,
    quotechar,
    mode
)

Arguments:
- file_type -> 'list', 'dict' or 'json' -> default: 'dict'
- delimiter -> ';', ',', '|' or '\\t'    -> default: ';'
- quotechar -> '\\"' or '\\''             -> default: '\\"'
- mode      -> 'rb', 'r' or 'rU'        -> default: 'rb'
\'\'\'
# Paste your code here.
'''

csv_parser = '''# -*- coding: utf-8 -*-

def read_file(file_type='dict', delimiter=';', quotechar='"', mode='rb'):
    import json
    import unicodecsv as csv

    with open('{datafile}', mode) as datafile:
        if file_type == 'dict':
            data = csv.DictReader(
                datafile,
                delimiter=delimiter,
                quotechar=quotechar
            )
        elif file_type == 'list':
            data = csv.reader(
                datafile,
                delimiter=delimiter,
                quotechar=quotechar
            )
        elif file_type == 'json':
            return json.load(datafile)
        else:
            data = []

        return [x for x in data]
'''
