# Run Frontend
FROM nginx
ARG ENV
COPY ./nginx-$ENV.conf /etc/nginx/conf.d/default.conf
RUN chmod +x /etc/nginx/conf.d/default.conf

EXPOSE 80