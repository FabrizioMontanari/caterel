import boto3


class EmailClient:

    def __init__(self):
        self.client = boto3.client('ses')

        self.server_address = 'no-reply@imartinisisposano.it'
        self.admin_address = 'imartinisisposano@gmail.com'


    def send_booking_notification(self):
        return self.client.send_email(
            Source=self.server_address,
            Destination={'ToAddresses': [self.admin_address]},
            Message={
                'Subject': {'Data': 'Ping'},
                'Body': {'Text': {'Data': 'test da srv a martini'}},
            }
        )
        
c = EmailClient()