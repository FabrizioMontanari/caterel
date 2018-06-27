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

    def _clean_string(self, s):
        return s.replace('=', '\'=')

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

    def _set_confirmation(self, guest, author=None):
        cell_mapping = {
            1: guest.get('nome', ''),
            2: guest.get('menu', ''),
            3: guest.get('email', ''),
            4: author or guest.get('nome'),
            5: datetime.now().strftime("%Y-%m-%d %H:%M"),
            6: guest.get('nota', '')
        }

        plus_one_ref = guest.get('is_plusone_of', '')
        booking_reference = f'P1 {plus_one_ref}' if plus_one_ref else guest.get('nome', '')
        booking_row = self.sheet_confirmation.find(booking_reference)

        cell_range = self.sheet_confirmation.range(
            booking_row.row,
            booking_row.col+1,
            booking_row.row,
            booking_row.col+7
        )

        for col_offset, value in cell_mapping.items():
            cell_range[col_offset].value = self._clean_string(value)

        self.sheet_confirmation.update_cells(cell_range)

    def get_family(self, guest):
        sanitised_guest = guest.lower()

        return ({'guestAllowed': True, 'guestFamily': self._get_family_data(sanitised_guest)}
                if self._is_guest_allowed(sanitised_guest)
                else {'guestAllowed': False})

    def update_rsvp(self, family_data):
        self._set_confirmation(family_data[0])  # main guest

        for guest in family_data[1:]:
            self._set_confirmation(guest, author=family_data[0].get('nome'))
