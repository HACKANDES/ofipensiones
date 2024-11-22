#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE USER auth;
  CREATE USER auth_service;
  ALTER USER auth PASSWORD 'passwd';
  ALTER USER auth_service PASSWORD 'passwd';

  CREATE DATABASE ofipensiones_auth;
  GRANT CONNECT ON DATABASE ofipensiones_auth TO auth;
  GRANT CONNECT ON DATABASE ofipensiones_auth TO auth_service;

  \c ofipensiones_auth

  GRANT USAGE, CREATE ON SCHEMA public TO auth;

  GRANT USAGE ON SCHEMA public TO auth_service;
  ALTER DEFAULT PRIVILEGES FOR USER auth IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO auth_service;
  ALTER DEFAULT PRIVILEGES FOR USER auth IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES to auth_service;
EOSQL
