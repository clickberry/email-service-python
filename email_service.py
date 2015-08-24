"""
Listens for incomming messages and sends emails.
"""

import nsq
import simplejson as json
import sendgrid
import os

# constants
REGISTRATIONS_TOPIC_NAME = 'registrations'
REGISTRATIONS_CHANNEL_NAME = 'send-email'
FROM_EMAIL_DEFAULT = 'noreply@clickberry.com'

# env
LOOKUPD_ADDRESSES = os.getenv('LOOKUPD_ADDRESSES', '').split(',')
SENDGRID_USERNAME = os.getenv('SENDGRID_USERNAME')
SENDGRID_PASSWORD = os.getenv('SENDGRID_PASSWORD')
REGISTRATION_TEMPLATE = os.getenv('REGISTRATION_TEMPLATE')

def listen(lookupd_addresses=None):
    """
    Define listeners for incoming messages.
    """

    # get lookupd addresses
    if lookupd_addresses:
        lookupd_addresses = [lookupd_addresses]
    lookupd_addresses = lookupd_addresses or LOOKUPD_ADDRESSES

    # listen for registrations
    listen_registrations(lookupd_addresses)

    # listen for password restores
    listen_password_restores(lookupd_addresses)

    # start all listeners
    nsq.run()

def listen_registrations(lookupd_addresses):
    """
    Listens for registration messages.
    """
    nsq.Reader(message_handler=registrations_handler,
               lookupd_http_addresses=lookupd_addresses,
               topic=REGISTRATIONS_TOPIC_NAME, 
               channel=REGISTRATIONS_CHANNEL_NAME, 
               lookupd_poll_interval=15)

def registrations_handler(message):
    """
    Handles incoming registration message.
    """
    # get template
    if not REGISTRATION_TEMPLATE: 
        return False

    template = dict(REGISTRATION_TEMPLATE)
    subject = template.get('subject')
    html = template.get('html')

    # get address
    json_data = json.loads(message.body)
    if not 'email' in json_data:
        return False

    address = json_data['email']

    # create sendgrid client
    sendgrid_client = sendgrid.SendGridClient(SENDGRID_USERNAME, SENDGRID_PASSWORD)
    message = sendgrid.Mail(to=address, 
                            subject=subject, 
                            html=html, 
                            from_email=FROM_EMAIL_DEFAULT)

    # send email
    status, message = sendgrid_client.send(message)

    print 'Registration email sent to address %s: %s' % address, status
    return True

def listen_password_restores(lookupd_addresses):
    """
    Listens for password restore messages.
    """
    return lookupd_addresses

if __name__ == '__main__':
    print 'Listening for incoming messages...'
    listen()    
