FROM python:3.8-buster

# install os system level packages
RUN apt-get -y update && apt install -y ffmpeg


USER 0
RUN mkdir /.cache && chmod 777 /.cache

# Copy source and install dependencies
RUN mkdir -p /opt/sandy_inspires/space_invaders/

# upgrade pip
RUN pip install --upgrade pip

COPY requirements.txt /opt/sandy_inspires/space_invaders/

# Install the application dependencies
RUN pip install --trusted-host pypi.python.org --trusted-host pypi.org --no-cache-dir -r /opt/sandy_inspires/space_invaders/requirements.txt

# copy all the other file
COPY . /opt/sandy_inspires/space_invaders/
WORKDIR /opt/sandy_inspires/space_invaders/

# Expose the application port
EXPOSE 8000

# Start the application - might have to do some load test
CMD pygbag --title "Sandy Inspires - Space Invaders" --app_name "Sandy Inspires - Space Invaders" /opt/sandy_inspires/space_invaders
