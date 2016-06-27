# -*- coding: utf-8 -*-

dockerfile = '''
FROM python:2.7

EXPOSE 8000

WORKDIR /home/codes/

CMD ["/bin/bash"]

'''

base_url = 'unix://var/run/docker.sock'

csv_parser = '''# -*- coding: utf-8 -*-

def read_file(csv_type, delimiter=';', quotechar='"', mode='rb'):
    import json
    import unicodecsv as csv

    with open('{csvfile}', mode) as csvfile:
        if csv_type == 'dict':
            csvdata = csv.DictReader(
                csvfile,
                delimiter=delimiter,
                quotechar=quotechar
            )
        elif csv_type == 'tuple':
            csvdata = csv.reader(
                csvfile,
                delimiter=delimiter,
                quotechar=quotechar
            )
        elif csv_type == 'json':
            csvdata = json.load(csvfile)

        return [x for x in csvdata]
'''
