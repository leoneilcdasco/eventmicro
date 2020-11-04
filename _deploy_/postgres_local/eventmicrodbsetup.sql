CREATE DATABASE eventmicrodb;
CREATE USER eventmicrodbuser WITH PASSWORD 'Buildtech2020';
ALTER ROLE eventmicrodbuser SET client_encoding TO 'utf8';
ALTER ROLE eventmicrodbuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE eventmicrodbuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE eventmicrodb TO eventmicrodbuser;
