FROM nginx:alpine3.17

# make the directory where we'll store the game files
RUN mkdir -p /usr/share/nginx/html/game/

# copy the main html page
COPY index.html /usr/share/nginx/html

# copy the game files
COPY game /usr/share/nginx/html/game

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