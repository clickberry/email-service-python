"""
Listens for incomming messages and sends emails.
"""

import nsq
import simplejson as json
import os

# get lookupd addresses from environment
LOOKUPD_ADDRESSES = os.getenv('LOOKUPD_ADDRESSES', '').split(',')

def handler(message):
    """
    Handles incoming message.
    """
    #json_data = json.loads(message)
    print message.body
    return True

# create reader
READER = nsq.Reader(message_handler=handler,
                    lookupd_http_addresses=LOOKUPD_ADDRESSES,
                    topic='registrations', channel='email', lookupd_poll_interval=15)

if __name__ == '__main__':    

    # start listening
    print 'Listening for incoming messages...'
    nsq.run()
