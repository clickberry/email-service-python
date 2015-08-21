"""
Listens for incomming messages and sends emails.
"""

import nsq
import simplejson as json
import sendgrid
import os

TOPIC_NAME = 'registrations'
CHANNEL_NAME = 'send-email'

# get parameters from environment
LOOKUPD_ADDRESSES = os.getenv('LOOKUPD_ADDRESSES', '').split(',')
SENDGRID_USERNAME = os.getenv('SENDGRID_USERNAME', '')
SENDGRID_PASSWORD = os.getenv('SENDGRID_PASSWORD', '')

def handler(message):
    """
    Handles incoming message.
    """
    json_data = json.loads(message.body)

    if not 'email' in json_data:
        return False

    send_registration_email(json_data['email'])
    return True

def send_registration_email(address):
    """
    Sends registration email to specified address.
    """

    sendgrid_client = sendgrid.SendGridClient(SENDGRID_USERNAME, SENDGRID_PASSWORD)
    message = sendgrid.Mail(to=address, subject='Welcome to Clickberry', 
                            html='Welcome to Clickberry', text='Welcome to Clickberry', 
                            from_email='noreply@clickberry.com')
    sendgrid_client.send(message)

    print 'Registration email sent to address: %s' % address

# create reader
READER = nsq.Reader(message_handler=handler,
                    lookupd_http_addresses=LOOKUPD_ADDRESSES,
                    topic=TOPIC_NAME, channel=CHANNEL_NAME, lookupd_poll_interval=15)

if __name__ == '__main__':    

    # start listening
    print 'Listening for incoming messages...'
    nsq.run()
