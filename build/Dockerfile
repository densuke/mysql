FROM mysql:8.4.5
COPY healthcheck.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/healthcheck.sh
# 実際の起動において現状では15〜30秒もあればおおむね起動完了しているのでこの値にしています
HEALTHCHECK --interval=5s --timeout=5s --start-period=15s --retries=5 \
    CMD [ "healthcheck.sh" ]
