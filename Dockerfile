FROM ubuntu:14.04

MAINTAINER Alexey Melnikov <a.melnikov@clickberry.com>

# Install Python Setuptools
RUN apt-get update && apt-get install -y \
  python-setuptools

# Install pip
RUN easy_install pip

WORKDIR /src

# Add and install Python modules
ADD requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt

# Bundle app source
ADD . /src

# Expose
EXPOSE  5000

CMD []

# Prepare env vars and start app
RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]