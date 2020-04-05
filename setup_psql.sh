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

# echo "Creating user..."
# if [ "$(psql -c "CREATE USER bayanihan_dev WITH PASSWORD 'dev_bayanihan';")" == "CREATE ROLE" ]; then
#     echo "User created."
# else
#     echo "User already exists."
# fi

# if [ "$(psql -c "GRANT ALL PRIVILEGES ON DATABASE unverified TO bayanihan_dev;")" == "GRANT" ]; then
#     echo "Permissions granted to user."
# else
#     echo "Failed to grant permissions."
# fi
