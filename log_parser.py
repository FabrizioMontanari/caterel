"""
Script molto alla vecchia per estrarre e collare i log da cloudwatch. 
Si possono esportare cloudwatch -> s3 -> download, ma hanno una struttura del tipo /logs/<uuid_a>/<uuid_b>/000000.gz
Puoi copiare da S3 a local con la aws cli: `$ aws s3 sync s3://<bucket-name>/path/to/log/root/ log/`

Lo script legge tutti i file di questo nome sotto una cartella /logs e li processa (per ora una semplice estrazione di tutti i dump delle chiamate Zappa)
"""

import os
import gzip
import csv

from ast import literal_eval
from base64 import b64decode


def read_log(path):
    with gzip.open(f'logs/{path}/000000.gz') as file:
        return file.readlines()


def process_log(event):
    event_data = event.split('\t')
    event_details = literal_eval(event_data[3].replace('Zappa Event: ', ''))

    return {
        'time': event_data[1],
        'uuid': event_data[2],
        'path': event_details['path'],
        'body': b64decode(event_details['body']) if event_details['isBase64Encoded'] else event_details['body'],
        'full_event': event_details,
    }


def dump_to_file(log_list, file_name='dump.txt'):
    with open(file_name, 'w') as output:
        for log in log_list:
            output.write(str(log)+'\n')


def dump_to_csv(log_list, file_name='dump.csv'):
    with open(file_name, 'w') as output:
        writer = csv.writer(output,  delimiter=';')
        
        writer.writerow(['time', 'uuid', 'path', 'body', 'full_event'])
        for log in log_list:
            writer.writerow(log.values())



# read and flatten
log_list = []
for log in (read_log(directory) for directory in os.listdir('logs')):
    log_list += log

# convert and filter
zappa_logs = [log.decode('utf-8')
              for log in log_list if 'Zappa Event' in log.decode('utf-8')]

# process and dump
processed_logs = [process_log(log) for log in zappa_logs]

confirmation_logs = [log for log in processed_logs]
dump_to_csv(confirmation_logs)
