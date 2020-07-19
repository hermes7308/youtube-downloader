# Run Frontend
FROM nginx
ARG ENV
COPY ./nginx-$ENV.conf /etc/nginx/conf.d/default.conf
RUN chmod +x /etc/nginx/conf.d/default.conf

# SSL certification
COPY ./ssl /etc/ssl
RUN chmod +r /etc/ssl/ca_bundle.crt
RUN chmod +r /etc/ssl/certificate.crt
RUN chmod +r /etc/ssl/cprivate.key

EXPOSE 443