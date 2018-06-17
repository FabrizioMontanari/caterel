import boto3
import gspread

from oauth2client.service_account import ServiceAccountCredentials


class DBManager(object):
    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds',
                      'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            'src/secret_key.json', self.scope)
        self.client = gspread.authorize(self.creds)

        self.sheet_family = self.client.open("MartiniWedding").worksheet("famiglie")
        self.sheet_confirmation = self.client.open("MartiniWedding").worksheet("conferme")
    
    def _load_credentials():
        pass

    def get_family(self, target):
        try:
            selected = self.sheet_family.find(target)
        except gspread.exceptions.CellNotFound as e:
            print(target, " non trovato")
            return None

        selected_family = self.sheet_family.row_values(selected.row)
        cleaned_family = [x for x in selected_family if x != target]
        return cleaned_family

    def set_confirmation(self, target, menu, notes, author, is_plusone_of):
        try:
            conf = self.sheet_confirmation.find(
                target) if is_plusone_of is None else self.sheet_confirmation.find("p1_" + is_plusone_of)
        except gspread.exceptions.CellNotFound as e:
            print(target, " non trovato per la conferma")
            return False
        # se +1 salvo anche il nome
        if is_plusone_of is not None:
            self.sheet_confirmation.update_cell(conf.row, conf.col, target)
            #TODO: aggiornare anche il foglio con le famiglie?????
            ref = self.sheet_family.find("p1_" + is_plusone_of)
            self.sheet_family.update_cell(ref.row, ref.col, target)

        self.sheet_confirmation.update_cell(conf.row, conf.col+1, menu)
        self.sheet_confirmation.update_cell(conf.row, conf.col+2, notes)
        self.sheet_confirmation.update_cell(
            conf.row, conf.col+3, author+" made it")
        self.sheet_confirmation.update_cell(
            conf.row, conf.col+4, dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
        # se +1 salvo il riferimento di quello che ha dato il +1
        if is_plusone_of is not None:
            self.sheet_confirmation.update_cell(
                conf.row, conf.col+5, is_plusone_of)
        return True
