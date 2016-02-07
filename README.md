# Dockerized Email Service
Email notification service on Python. The service listens for events from the Bus and sends emails.

* [Architecture](#architecture)
* [Technologies](#technologies)
* [Environment Variables](#environment-variables)
* [Events](#events)
* [License](#license)

# Architecture
The application is a long-running worker service listening for messages from the Bus.

# Technologies
* Python 2.7
* Official pynsq driver for NSQ messaging service

# Environment Variables
The service should be properly configured with environment variables.

Key | Value | Description
:-- | :-- | :-- 
LOOKUPD_ADDRESSES | nsqlookupd1:4161,nsqlookupd2:4161 | TCP addresses for nsqlookupd instances.
SENDGRID_USERNAME | sendgrid_username | Sendgrid account user name.
SENDGRID_PASSWORD | *** | Sendgrid account password.
REGISTRATION_TEMPLATE | {"subject": "Welcome to Clickberry", "html": "&lt;html&gt;&lt;body&gt;&lt;h1&gt;Welcome to Clickberry&lt;/h1&gt;&lt;/body&gt;&lt;/html&gt;"} | HTML template for registration email.
FEEDBACK_TEMPLATE | {"subject": "Feedback to Clickberry", "html": "&lt;html&gt;&lt;body&gt;&lt;h1&gt;Feedback from %name%&lt;/h1&gt;&lt;p&gt;Message: %comment%&lt;p&gt;&lt;/body&gt;&lt;/html&gt;"} | HTML template for feedback email.
SUPPORT_EMAIL | support@clickberry.com | Support mailbox.
FROM_EMAIL_DEFAULT | noreply@clickberry.com | Default noreply sender.
FEEDBACK_EMAIL_DEFAULT | feedback@clickberry.com | Default feedback sender.

# Events
The service listens for events from the Bus (messaging service).

## Receive events

Topic | Channel | Params | Description
:-- | :-- | :-- | :-- 
registrations | send-email | { email: *recipient_address* } | Sends registration emails.

# License
Source code is under GNU GPL v3 [license](LICENSE).
