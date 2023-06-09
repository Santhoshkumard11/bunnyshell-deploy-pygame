FROM python:3.11-buster as pygame_build

# install os system level packages
RUN apt-get -y update && apt install -y ffmpeg

USER 0
RUN mkdir /.cache && chmod 777 /.cache

# make game directories
RUN mkdir -p /opt/sandy_inspires/game/space_invaders/ /opt/sandy_inspires/game/flappy_bird/ /opt/sandy_inspires/game/classic_hunt/ /opt/sandy_inspires/game/street_fighter/

# upgrade pip
RUN pip install --upgrade pip

COPY space_invaders/requirements.txt /opt/sandy_inspires/game/space_invaders/

# install the game dependencies
RUN pip install --trusted-host pypi.python.org --trusted-host pypi.org --no-cache-dir -r /opt/sandy_inspires/game/space_invaders/requirements.txt

# copy all the game folders
COPY space_invaders /opt/sandy_inspires/game/space_invaders
COPY flappy_bird /opt/sandy_inspires/game/flappy_bird
COPY classic_hunt /opt/sandy_inspires/game/classic_hunt
COPY street_fighter /opt/sandy_inspires/game/street_fighter

# build the games - might have to do some load test
RUN pygbag --build --ume_block 0 --title "Sandy Inspires - Space Invaders" --app_name "Sandy Inspires - Space Invaders" /opt/sandy_inspires/game/space_invaders/main.py
RUN pygbag --build --ume_block 0 --title "Sandy Inspires - Flappy Bird" --app_name "Sandy Inspires - Flappy Bird" /opt/sandy_inspires/game/flappy_bird/main.py
RUN pygbag --build --ume_block 0 --title "Sandy Inspires - Classic Hunt" --app_name "Sandy Inspires - Classic Hunt" /opt/sandy_inspires/game/classic_hunt/main.py
RUN pygbag --build --ume_block 0 --title "Sandy Inspires - Street Figher" --app_name "Sandy Inspires - Street Figher" /opt/sandy_inspires/game/street_fighter/main.py


FROM nginx:alpine3.17 as prod

# create all game directories
RUN mkdir -p /usr/share/nginx/html/game/space-invaders/ /usr/share/nginx/html/game/flappy-bird/ /usr/share/nginx/html/game/classic-hunt/ /usr/share/nginx/html/game/street-fighter/

# copy the main html page
COPY index.html /usr/share/nginx/html

# copy the file built from the build env
COPY --from=pygame_build /opt/sandy_inspires/game/space_invaders/build/web /usr/share/nginx/html/game/space-invaders
COPY --from=pygame_build /opt/sandy_inspires/game/flappy_bird/build/web /usr/share/nginx/html/game/flappy-bird
COPY --from=pygame_build /opt/sandy_inspires/game/classic_hunt/build/web /usr/share/nginx/html/game/classic-hunt
COPY --from=pygame_build /opt/sandy_inspires/game/street_fighter/build/web /usr/share/nginx/html/game/street-fighter

# copy nginx config and entrypoint files
COPY .docker/files/nginx.conf /etc/nginx/nginx.conf 
COPY .docker/files/mime.types /etc/nginx/mime.types
COPY .docker/files/entrypoint.sh  /usr/share/entrypoint.sh 

# make the entrypoint script executable
RUN chmod +x /usr/share/entrypoint.sh

WORKDIR /usr/share/nginx/html

ENTRYPOINT ["/usr/share/entrypoint.sh"]

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]