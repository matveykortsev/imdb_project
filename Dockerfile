FROM postgres:12
ADD scripts/01_create_table.sql /docker-entrypoint-initdb.d
ADD scripts/02_load_data.sql /docker-entrypoint-initdb.d
ADD scripts/03_create_views.sql /docker-entrypoint-initdb.d