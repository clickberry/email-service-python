# Dockerized Email Service
Email notification service on Python. The service listens for events from the Bus and sends emails.

## Environment Variables
The service should be properly configured with environment variables.

Key | Value | Description
:-- | :-- | :-- 
LOOKUPD_ADDRESSES | nsqlookupd1:4161,nsqlookupd2:4161 | TCP addresses for nsqlookupd instances.
SENDGRID_USERNAME | sendgrid_username | Sendgrid account user name.
SENDGRID_PASSWORD | *** | Sendgrid account password.
REGISTRATION_TEMPLATE | {"subject": "Welcome to Clickberry", "html": "&lt;html&gt;&lt;body&gt;&lt;h1&gt;Welcome to Clickberry&lt;/h1&gt;&lt;/body&gt;&lt;/html&gt;"} | HTML template for registration email.

## Events
The service listens for events from the Bus (messaging service).

### Receive events

Topic | Channel | Description
:-- | :-- | :-- 
registrations | send-email | Sends registration emails.
