FROM nginx:1.19.2

RUN rm /etc/nginx/conf.d/default.conf

COPY deploy/nginx/nginx.conf ../etc/nginx/conf.d
COPY movies_admin/staticfiles /etc/nginx/staticfiles
