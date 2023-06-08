FROM python:3.11-buster as build

# install os system level packages
RUN apt-get -y update && apt install -y ffmpeg


USER 0
RUN mkdir /.cache && chmod 777 /.cache

# Copy source and install dependencies
RUN mkdir -p /opt/sandy_inspires/space_invaders/

# upgrade pip
RUN pip install --upgrade pip

COPY requirements.txt /opt/sandy_inspires/space_invaders

# Install the application dependencies
RUN pip install --trusted-host pypi.python.org --trusted-host pypi.org --no-cache-dir -r /opt/sandy_inspires/space_invaders/requirements.txt

# copy all the other file
COPY . /opt/sandy_inspires/space_invaders
WORKDIR /opt/sandy_inspires/space_invaders/

# build the application - might have to do some load test
RUN pygbag --build --ume_block 0 --title "Sandy Inspires - Space Invaders" --app_name "Sandy Inspires - Space Invaders" /opt/sandy_inspires/space_invaders

FROM nginx:1.21.3-alpine as prod

RUN mkdir -p /usr/share/nginx/html

COPY --from=build -r /opt/sandy_inspires/space_invaders/build/web/* /usr/share/nginx/html/

COPY .docker/files/nginx.conf /etc/nginx/nginx.conf
COPY .docker/files/entrypoint.sh  /usr/share/entrypoint.sh
RUN chmod +x /usr/share/entrypoint.sh

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]