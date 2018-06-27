import boto3

from jinja2 import Template
from os import path

ROOT_FOLDER = path.join(path.dirname(__file__), '..')


class EmailClient:
    def __init__(self):
        self.client = boto3.client('ses')

        self.server_address = 'no-reply@imartinisisposano.it'
        self.admin_address = 'imartinisisposano@gmail.com'

    def _read_template(self, template_name):
        with open(f'{ROOT_FOLDER}/templates/emails/{template_name}') as file:
            return file.read()

    def _render_message(self, template_name, **kwargs):
        message = self._read_template(template_name)
        return Template(message).render(**kwargs)

    def _send_message(self, template_name, from_email, to_email, subject, template_dictionary={}):
        return self.client.send_email(
            Source=from_email,
            Destination={'ToAddresses': [to_email]},
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': self._render_message(
                            template_name=f'{template_name}.txt',
                            **template_dictionary
                        )
                    },
                    'Html': {
                        'Data': self._render_message(
                            template_name=f'{template_name}.html',
                            **template_dictionary
                        )
                    },
                },
            }
        )

    def _send_admin_notification(self, template_dictionary):
        main_guest = template_dictionary['name']

        return self._send_message(
            template_name='admin_notification',
            from_email=self.server_address,
            to_email=self.admin_address,
            subject=f'Nuova conferma RSVP da {main_guest}!',
            template_dictionary=template_dictionary
        )

    def _send_guest_notification(self, template_dictionary):
        main_guest = template_dictionary['name']

        return self._send_message(
            template_name='guest_notification',
            from_email=self.admin_address,
            to_email=template_dictionary['email'],
            subject=f'Grazie per la conferma {main_guest}!',
            template_dictionary=template_dictionary
        )

    def _build_template_dictionary(self, family_data):
        main_guest = family_data[0]

        return {
            'name': main_guest.get('nome'),
            'email': main_guest.get('email'),
            'note': main_guest.get('nota'),
            'family': [
                {
                    'name': guest.get('nome'),
                    'menu': guest.get('menu')
                }
                for guest
                in family_data
            ]
        }

    def send_rsvp_notifications(self, family_data):
        template_dictionary = self._build_template_dictionary(family_data)

        self._send_admin_notification(template_dictionary)
        if template_dictionary['email']:
            self._send_guest_notification(template_dictionary)
