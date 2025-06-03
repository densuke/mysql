FROM mysql:8.4.5
COPY healthcheck.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/healthcheck.sh
HEALTHCHECK --interval=5s --timeout=3s --start-period=15s --retries=5 \
    CMD [ "healthcheck.sh" ]