import boto3

from jinja2 import Template


class EmailClient:
    def __init__(self):
        self.client = boto3.client('ses')

        self.server_address = 'no-reply@imartinisisposano.it'
        self.admin_address = 'imartinisisposano@gmail.com'

    def _read_template(self, template_name):
        with open(f'../templates/emails/{template_name}') as file:
            return file.read()

    def _render_message(self, template_name, **kwargs):
        message = self._read_template(template_name)
        return Template(message).render(**kwargs)

    def _send_message(self, template_name, from_email, to_email, subject, template_dictionary={}):
        return  self.client.send_email(
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

    def _sanitise_dictionary(dictionary):
        allowed_keys = ['guest_name', 'guest_note', 'menu_choice']
        return {k:v for k,v in dictionary if k in allowed_keys}

    def send_admin_notification(self, template_dictionary):
        guest_name = template_dictionary.get('guest_name', None)

        return self._send_message(
            template_name='admin_notification',
            from_email=self.server_address,
            to_email=self.admin_address,
            subject=f'Nuova conferma RSVP da {guest_name}!',
            template_dictionary=self._sanitise_dictionary(template_dictionary)
        )

    def send_guest_notification(self, to_email, template_dictionary):
        guest_name = template_dictionary.get('guest_name', None)

        return self._send_message(
            template_name='guest_notification',
            from_email=self.admin_address,
            to_email=to_email,
            subject=f'Grazie per la conferma {guest_name}!',
            template_dictionary=self._sanitise_dictionary(template_dictionary)
        )
