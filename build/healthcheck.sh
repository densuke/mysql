#!/bin/bash


# Wait for the database to be ready
mysqladmin ping --silent -h db \
    -u "${MYSQL_USER}" --password="${MYSQL_PASSWORD}" \
    --wait=1
