# OLake Domain Terminology & Aliases

This file tracks canonical names, connector aliases, and components within the OLake ecosystem.

## Components & Roles
- **OLake**: High-performance open-source data replication engine syncing relational and NoSQL databases to Lakehouse storage.
- **OLake UI**: Web-based interface for managing pipelines, connectors, and sync runs (deployed via Docker Compose).
- **OLake Go**: The core ingestion execution engine written in Go.
- **Fusion**: OLake's table compaction, maintenance, and optimization subsystem.

## Supported Sources vs. Destinations
- **Sources**: PostgreSQL, MongoDB, MySQL, Oracle, Kafka, DB2 LUW, MSSQL, S3.
  - *Note*: Kafka is supported as a **SOURCE**, not a destination.
- **Destinations**: Apache Iceberg (via REST, AWS Glue, JDBC, Hive catalogs) and Parquet format.
  - *Note*: Snowflake, BigQuery, and Redshift direct native ingestion are not direct writer connectors; Iceberg tables produced by OLake can be queried through Snowflake/BigQuery Iceberg catalogs.

## Connector CDC Technologies
- **Postgres**: Logical decoding via `wal2json` or `pgoutput`.
- **MySQL**: Binary logging (`binlog`) with row-based format.
- **Oracle**: LogMiner Change Data Capture (`archivelog` mode required).
- **MongoDB**: Change Streams on replica sets or sharded clusters (`oplog`).
