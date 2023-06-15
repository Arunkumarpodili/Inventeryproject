FROM nginx
RUN rm -rf /usr/share/nginx/html/index.html
ADD templates /usr/share/nginx/html/