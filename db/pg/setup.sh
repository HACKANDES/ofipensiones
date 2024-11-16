#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER ofipensiones_web;
    ALTER USER ofipensiones_web PASSWORD 'webpasswd';
    
    CREATE DATABASE ofipensiones_andes;
    GRANT CONNECT ON DATABASE ofipensiones_andes TO ofipensiones_web;

    \c ofipensiones_andes

    GRANT USAGE ON SCHEMA public TO ofipensiones_web;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO ofipensiones_web;
EOSQL
