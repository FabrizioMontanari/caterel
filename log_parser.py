"""
Script molto alla vecchia per estrarre e collare i log da cloudwatch. 
Si possono esportare cloudwatch -> s3 -> download, ma hanno una struttura del tipo /logs/<uuid_a>/<uuid_b>/000000.gz
Puoi copiare da S3 a local con la aws cli: `$ aws s3 sync s3://<bucket-name>/path/to/log/root/ log/`

Lo script legge tutti i file di questo nome sotto una cartella /logs e li processa (per ora una semplice estrazione di tutti i dump delle chiamate Zappa)
"""

import os
import gzip


def read_log(path):
    with gzip.open(f'logs/{path}/000000.gz') as file:
        return file.readlines()


def process_line(log):  # TODO
    from ast import literal_eval

    event = log.split(b'Zappa Event: ')[1].replace(b'\n', b'')
    print(type(event))
    str_event = str(event)
    print(type(literal_eval(str_event)))
    return literal_eval(str_event)


def dump_to_file(log_list):
    with open('dump.txt', 'w') as output:
        for log in log_list:
            output.write(str(log))


log_list = []
for log in (read_log(directory) for directory in os.listdir('logs')):
    log_list += log

zappa_events = [log for log in log_list if 'Zappa Event' in str(log)]
dump_to_file(zappa_events)
