"""
Email notification service v0.0.8
Listens for incomming messages and sends emails.
"""

import nsq
import simplejson as json
import sendgrid
import os

try:
    from html import escape  # python 3.x
except ImportError:
    from cgi import escape  # python 2.x

# constants
REGISTRATIONS_TOPIC_NAME = 'registrations'
FEEDBACKS_TOPIC_NAME = 'feedbacks'
ABUSES_TOPIC_NAME = 'abuses'

# env
LOOKUPD_ADDRESSES = os.getenv('LOOKUPD_ADDRESSES', '').split(',')

SENDGRID_USERNAME = os.getenv('SENDGRID_USERNAME')
SENDGRID_PASSWORD = os.getenv('SENDGRID_PASSWORD')

REGISTRATION_TEMPLATE = os.getenv('REGISTRATION_TEMPLATE')
FEEDBACK_TEMPLATE = os.getenv('FEEDBACK_TEMPLATE')
ABUSE_TEMPLATE = os.getenv('ABUSE_TEMPLATE')

SUPPORT_EMAIL = os.getenv('SUPPORT_EMAIL')
NOREPLY_EMAIL = os.getenv('NOREPLY_EMAIL')

def listen(lookupd_addresses=None):
    """
    Define listeners for incoming messages.
    """

    # get lookupd addresses
    if lookupd_addresses:
        lookupd_addresses = [lookupd_addresses]
    lookupd_addresses = lookupd_addresses or LOOKUPD_ADDRESSES

    # register listeners
    register_listeners(lookupd_addresses)

    # start all listeners
    nsq.run()

def register_listeners(lookupd_addresses):
    listen_registrations(lookupd_addresses)
    listen_feedbacks(lookupd_addresses)
    listen_abuses(lookupd_addresses)

def listen_registrations(lookupd_addresses):
    """
    Listens for registration messages.
    """
    nsq.Reader(message_handler=registrations_handler,
               lookupd_http_addresses=lookupd_addresses,
               topic=REGISTRATIONS_TOPIC_NAME, 
               channel='send-email',
               lookupd_poll_interval=15)

def listen_feedbacks(lookupd_addresses):
    """
    Listens for feedback messages.
    """
    nsq.Reader(message_handler=feedbacks_handler,
               lookupd_http_addresses=lookupd_addresses,
               topic=FEEDBACKS_TOPIC_NAME, 
               channel='send-email',
               lookupd_poll_interval=15)

def listen_abuses(lookupd_addresses):
    """
    Listens for abuse messages.
    """
    nsq.Reader(message_handler=abuses_handler,
               lookupd_http_addresses=lookupd_addresses,
               topic=ABUSES_TOPIC_NAME, 
               channel='send-email',
               lookupd_poll_interval=15)

def registrations_handler(message):
    """
    Handles incoming registration messages.
    """
    # get template
    if not REGISTRATION_TEMPLATE: 
        return False

    template = json.loads(REGISTRATION_TEMPLATE)
    subject = template['subject']
    html = template['html']

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
                            from_email=NOREPLY_EMAIL)

    # send email
    status, message = sendgrid_client.send(message)
    if status != 200:
        print 'Could not sent email to address %s: %s, %s' % (address, status, message)
        return False

    print 'Registration email sent to address %s' % address
    return True

def feedbacks_handler(message):
    """
    Handles incoming feedback messages.
    """
    # get template
    if not FEEDBACK_TEMPLATE: 
        return False

    template = json.loads(FEEDBACK_TEMPLATE)
    subject = template['subject']
    html = template['html']

    # parse feedback data
    json_data = json.loads(message.body)
    if not 'comment' in json_data:
        return False

    address = json_data.get('email', NOREPLY_EMAIL)
    name = escape(json_data.get('name', 'anonymous'))
    comment = escape(json_data.get('comment'))

    html = html.replace('%name%', name)
    html = html.replace('%comment%', comment)

    # create sendgrid client and message
    sendgrid_client = sendgrid.SendGridClient(SENDGRID_USERNAME, SENDGRID_PASSWORD)
    message = sendgrid.Mail(to=SUPPORT_EMAIL, 
                            subject=subject, 
                            html=html, 
                            from_email=address)

    # send email
    status, message = sendgrid_client.send(message)
    if status != 200:
        print 'Could not sent email to address %s: %s, %s' % (SUPPORT_EMAIL, status, message)
        return False

    print 'Feedback email sent from %s' % address
    return True

def abuses_handler(message):
    """
    Handles incoming abuse messages.
    """
    # get template
    if not ABUSE_TEMPLATE: 
        return False

    template = json.loads(ABUSE_TEMPLATE)
    subject = template['subject']
    html = template['html']

    # parse abuse data
    json_data = json.loads(message.body)
    if not 'url' in json_data:
        return False

    url = escape(json_data.get('url'))
    address = json_data.get('email', NOREPLY_EMAIL)
    name = escape(json_data.get('name', 'anonymous'))
    comment = escape(json_data.get('comment', ''))

    html = html.replace('%url%', url)
    html = html.replace('%name%', name)
    html = html.replace('%comment%', comment)

    # create sendgrid client and message
    sendgrid_client = sendgrid.SendGridClient(SENDGRID_USERNAME, SENDGRID_PASSWORD)
    message = sendgrid.Mail(to=SUPPORT_EMAIL, 
                            subject=subject, 
                            html=html, 
                            from_email=address)

    # send email
    status, message = sendgrid_client.send(message)
    if status != 200:
        print 'Could not sent email to address %s: %s, %s' % (SUPPORT_EMAIL, status, message)
        return False

    print 'Abuse email sent from %s' % address
    return True

if __name__ == '__main__':
    print 'Listening for incoming messages...'
    listen()    
