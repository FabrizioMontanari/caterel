import boto3
import gspread
import json

from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials


class DBManager(object):
    def __init__(self):
        credentials = self._get_credentials()
        client = gspread.authorize(credentials)

        self.sheet_family = client.open(
            "MartiniWedding").worksheet("famiglie")
        self.sheet_confirmation = client.open(
            "MartiniWedding").worksheet("conferme")

    def _get_credentials(self):
        required_scopes = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive',
        ]
        s3 = boto3.resource('s3')
        obj = s3.Object('www.imartinisisposano.it', 'secret_key.json').get()
        keyfile_dict = json.loads(obj['Body'].read().decode('utf-8'))

        return ServiceAccountCredentials.from_json_keyfile_dict(
            keyfile_dict=keyfile_dict,
            scopes=required_scopes
        )

    def _is_guest_allowed(self, guest):
        try:
            return guest and self.sheet_family.find(guest)
        except (gspread.exceptions.CellNotFound, AttributeError) as e:
            return False

    def _get_family_data(self, guest):
        guest_cell = self.sheet_family.find(guest)
        guest_list = []
        for person in self.sheet_family.row_values(guest_cell.row):
            if person != guest:
                guest_list.append('' if 'p1' in person else person)
        return guest_list

    def get_family(self, guest):
        sanitised_guest = guest.lower()

        return ({'guestAllowed': True, 'guestFamily': self._get_family_data(sanitised_guest)}
                if self._is_guest_allowed(sanitised_guest)
                else {'guestAllowed': False})

    def set_confirmation(self, target, menu, notes, author, is_plusone_of):
        try:
            conf = self.sheet_confirmation.find(
                target) if is_plusone_of is None else self.sheet_confirmation.find("p1_" + is_plusone_of)
        except gspread.exceptions.CellNotFound as e:
            return False
        # se +1 salvo anche il nome
        if is_plusone_of is not None:
            self.sheet_confirmation.update_cell(conf.row, conf.col, self.clean_string(target))
            #TODO: aggiornare anche il foglio con le famiglie?????
            ref = self.sheet_family.find("p1_" + is_plusone_of)
            self.sheet_family.update_cell(ref.row, ref.col, self.clean_string(target))

        self.sheet_confirmation.update_cell(conf.row, conf.col+1, self.clean_string(menu))
        self.sheet_confirmation.update_cell(conf.row, conf.col+2, self.clean_string(notes))
        self.sheet_confirmation.update_cell(
            conf.row, conf.col+3, author+" made it")
        self.sheet_confirmation.update_cell(
            conf.row, conf.col+4, datetime.now().strftime("%Y-%m-%d %H:%M"))
        # se +1 salvo il riferimento di quello che ha dato il +1
        if is_plusone_of is not None:
            self.sheet_confirmation.update_cell(
                conf.row, conf.col+5, self.clean_string(is_plusone_of))
        return True

    def clean_string(self, s):
        if len(s)<=2:
            return s
        
        if s[0] == "=":
            return "haking?" + s[1:]
        
        return s
