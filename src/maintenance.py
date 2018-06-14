import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import datetime as dt

class DBMaintenance(object):
    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('/home/fabrizio/Martini/caterel/src/secret_key.json', self.scope)
        self.client  = gspread.authorize(self.creds)

        self.sheet_family = self.client.open("MartiniWedding").worksheet("famiglie")
        self.sheet_confirmation = self.client.open("MartiniWedding").worksheet("conferme")

    def dbLowercase(self, famiglie, conferme):
        import time

        # FAMIGLIE
        if famiglie:
            print('working on famiglie sheet')
            nrow = self.sheet_family.row_count
            print("total_families: " + str(nrow))
            for i in range(1,nrow+1):
                row = self.sheet_family.row_values(i)
                for j in range(1,len(row)+1):
                    cell = self.sheet_family.cell(i,j)
                    val = cell.value
                    text = val.split()
                    print(val)
                    lowered=[t.lower() for t in text]
                    new_text = ' '.join(lowered)
                    if new_text != val:
                        self.sheet_family.update_cell(i, j, new_text)
                    else:
                        print('skipping...')
                time.sleep(5)  # per evitare di eccedere il numero massimo di richieste per 100s
        
        # CONFERME
        if conferme:
            print('working on conferme sheet')
            nrow = self.sheet_confirmation.row_count
            print("total_people: " + str(nrow))
            for i in range(2,nrow+1):
                cell = self.sheet_confirmation.cell(i,1)
                val = cell.value
                text = val.split()
                print(val)
                lowered=[t.lower() for t in text]
                new_text = ' '.join(lowered)
                if new_text != val:
                    self.sheet_confirmation.update_cell(i, 1, new_text)
                else:
                    print('skipping...')
                time.sleep(1)  # per evitare di eccedere il numero massimo di richieste per 100s
    
    def dbCapitalizeNames(self, famiglie, conferme):
        import time

        # FAMIGLIE
        if famiglie:
            print('working on famiglie sheet')
            nrow = self.sheet_family.row_count
            print("total_families: " + str(nrow))
            for i in range(1,nrow+1):
                row = self.sheet_family.row_values(i)
                for j in range(1,len(row)+1):
                    cell = self.sheet_family.cell(i,j)
                    val = cell.value
                    text = val.split()
                    print(val)
                    uppered = [t[0].upper()+t[1:] if not t.startswith("p1_") else "p1_"+t[3].upper()+t[4:] for t in text ]
                    new_text = ' '.join(uppered)
                    if new_text != val:
                        self.sheet_family.update_cell(i, j, new_text)
                    else:
                        print('skipping...')
                time.sleep(5)  # per evitare di eccedere il numero massimo di richieste per 100s

        # CONFERME
        if conferme:
            print('working on conferme sheet')
            nrow = self.sheet_confirmation.row_count
            print("total_people: " + str(nrow))
            for i in range(2,nrow+1):
                cell = self.sheet_confirmation.cell(i,1)
                val = cell.value
                text = val.split()
                print(val)
                uppered = [t[0].upper()+t[1:] if not t.startswith("p1_") else "p1_"+t[3].upper()+t[4:] for t in text ]
                new_text = ' '.join(uppered)
                if new_text != val:
                    self.sheet_confirmation.update_cell(i, 1, new_text)
                else:
                    print('skipping...')
                time.sleep(1)  # per evitare di eccedere il numero massimo di richieste per 100s
'''
from maintenance import DBMaintenance as DBM
dbm=DBM()

dbm.dbLowercase(True, True)

dbm.dbCapitalizeNames(True, True)
'''