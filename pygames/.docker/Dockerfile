FROM python:3.11-buster as build_space_invaders

# install os system level packages
RUN apt-get -y update && apt install -y ffmpeg

USER 0
RUN mkdir /.cache && chmod 777 /.cache

# Copy source and install dependencies
RUN mkdir -p /opt/sandy_inspires/game/space_invaders/

# upgrade pip
RUN pip install --upgrade pip

COPY space_invaders/requirements.txt /opt/sandy_inspires/game/space_invaders

# Install the application dependencies
RUN pip install --trusted-host pypi.python.org --trusted-host pypi.org --no-cache-dir -r /opt/sandy_inspires/game/space_invaders/requirements.txt

# copy all the other file
COPY . /opt/sandy_inspires/game/space_invaders
WORKDIR /opt/sandy_inspires/game/space_invaders/

# build the application - might have to do some load test
RUN pygbag --build --ume_block 0 --title "Sandy Inspires - Space Invaders" --app_name "Sandy Inspires - Space Invaders" /opt/sandy_inspires/game/space_invaders


FROM nginx:alpine3.17 as prod

# create all game directories
RUN mkdir -p /usr/share/nginx/html/game/space_invaders
RUN mkdir -p /usr/share/nginx/html/game/flappy_bird
RUN mkdir -p /usr/share/nginx/html/game/classic_hunt

# copy the main html page
COPY index.html /usr/share/nginx/html

# copy the file built from the build env
COPY --from=build_space_invaders /opt/sandy_inspires/game/space_invaders/build/web/* /usr/share/nginx/html/game/space_invaders

# copy nginx config and entrypoint files
COPY .docker/files/nginx.conf /etc/nginx/nginx.conf
COPY .docker/files/entrypoint.sh  /usr/share/entrypoint.sh
COPY .docker/files/mime.types /etc/nginx/mime.types

# make the entrypoint script executable
RUN chmod +x /usr/share/entrypoint.sh

WORKDIR /usr/share/nginx/html

ENTRYPOINT ["/usr/share/entrypoint.sh"]

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]