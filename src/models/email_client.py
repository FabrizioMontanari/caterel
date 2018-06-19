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

    def send_admin_notification(self):
        template = 'admin_notification'
        return self.client.send_email(
            Source=self.server_address,
            Destination={'ToAddresses': [self.admin_address]},
            Message={
                'Subject': {
                    'Data': 'Ping'
                },
                'Body': {
                    'Text': {
                        'Data': self._render_message(
                            template_name=f'{template}.txt',
                            guest_name='tizio caio'
                        )
                    },
                    'Html': {
                        'Data': self._render_message(
                            template_name=f'{template}.html',
                            guest_name='tizio caio'
                        )
                    },
                },
            }
        )

    def send_guest_notification(self, guest_email=None):
        template = 'guest_notification'

        return self.client.send_email(
            Source=self.admin_address,
            Destination={'ToAddresses': [guest_email]},
            Message={
                'Subject': {
                    'Data': 'Ping'
                },
                'Body': {
                    'Text': {
                        'Data': self._render_message(
                            template_name=f'{template}.txt',
                            guest_name='tizio caio'
                        )
                    },
                    'Html': {
                        'Data': self._render_message(
                            template_name=f'{template}.html',
                            guest_name='tizio caio'
                        )
                    },
                },
            }
        )


# debug
client = EmailClient()
res = client.send_guest_notification('imartinisisposano@gmail.com')
print(res)
