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

def listen(lookupd_addresses=None):
    """
    Define listeners for incoming messages.
    """

    # get lookupd addresses
    if lookupd_addresses:
        lookupd_addresses = [lookupd_addresses]
    lookupd_addresses = lookupd_addresses or os.getenv('LOOKUPD_ADDRESSES', '').split(',')

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
    json_data = json.loads(message.body)

    if not 'email' in json_data:
        return False

    return send_registration_email(json_data['email'])

def send_registration_email(address):
    """
    Sends registration email to specified address.
    """

    registration_template = os.getenv('REGISTRATION_TEMPLATE')
    if not registration_template: 
        return False

    # get template
    template = dict(registration_template)
    subject = template.get('subject')
    html = template.get('html')
    from_email = template.get('from', FROM_EMAIL_DEFAULT)

    # create sendgrid client
    username = os.getenv('SENDGRID_USERNAME', '')
    password = os.getenv('SENDGRID_PASSWORD', '')
    sendgrid_client = sendgrid.SendGridClient(username, password)
    message = sendgrid.Mail(to=address, 
                            subject=subject, 
                            html=html, 
                            from_email=from_email)
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
