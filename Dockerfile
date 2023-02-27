FROM nginx:1.23.3-alpine

COPY index.html /usr/share/nginx/html
COPY README.html /usr/share/nginx/html
COPY img/ /usr/share/nginx/html/img
