#!/usr/bin/env sh

pg_status=$(pg_isready 2>&1)

if [ "$pg_status" == "/tmp:5432 - accepting connections" ]; then
    echo "PostgreSQL Server running.";

elif [ "$pg_status" == "/tmp:5432 - no response" ]; then
    echo "PostgreSQL server not running. Please start the database server.";
    exit 1;
else
    echo "$pg_status: PostgreSQL Server not found! Please make sure it is installed correctly.";
    exit 1;
fi

echo "Checking if database with name \"unverified\" exists..."

if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='unverified'" )" != '1' ]; then
    echo "Database not found. Creating..."
    createdb "unverified";
else
    echo "Database already exists."
fi 