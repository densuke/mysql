#!/bin/bash


# Wait for the database to be ready
mysqladmin ping --silent -h db \
    -u "${MYSQL_USER}" --password="${MYSQL_PASSWORD}" \
    --connect-timeout=1 ||
mysqladmin ping -h localhost --silent \
    -u "${MYSQL_USER}" --password="${MYSQL_PASSWORD}" \
    --connect-timeout=1
