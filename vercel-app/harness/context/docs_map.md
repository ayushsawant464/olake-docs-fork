# OLake Documentation Structural Map

This map outlines the documentation hierarchy and canonical paths across `docs/` for navigation routing.

## 1. Getting Started & Concepts
- `docs/intro.mdx` — High-level overview of OLake (open table format replication, 500x faster).
- `docs/getting-started/quickstart.mdx` — Quickstart guide.
- `docs/getting-started/creating-first-pipeline.mdx` — Pipeline configuration walkthrough.
- `docs/getting-started/playground.mdx` — Interactive playground instructions.

## 2. Installation & Deployment
- `docs/install/olake-ui/index.mdx` — Docker Compose setup for OLake UI.
- `docs/install/olake-ui/offline-environments-aws.mdx` — Airgapped / offline deployment on AWS.
- `docs/install/olake-ui/offline-environments-generic.mdx` — Generic offline / private network deployment.
- `docs/install/docker-cli.mdx` — Running OLake via Docker CLI without the UI.
- `docs/install/kubernetes.mdx` — Kubernetes & Helm chart deployment.

## 3. Source Connectors (`docs/connectors/`)
- `docs/connectors/postgres/index.mdx` — PostgreSQL connector (logical decoding, wal2json, pgoutput).
- `docs/connectors/mongodb/index.mdx` — MongoDB connector (change streams, oplog, replica sets).
- `docs/connectors/mysql/index.mdx` — MySQL connector (binlog replication).
- `docs/connectors/oracle/index.mdx` — Oracle connector (LogMiner CDC setup, archivelog).
- `docs/connectors/kafka/index.mdx` — Kafka connector (source topics, offsets).
- `docs/connectors/db2/index.mdx` — IBM DB2 LUW connector.
- `docs/connectors/mssql/index.mdx` — Microsoft SQL Server connector.
- `docs/connectors/s3/index.mdx` — Amazon S3 source connector.

## 4. Destination Writers (`docs/writers/`)
- **Apache Iceberg (`docs/writers/iceberg/`)**:
  - `docs/writers/iceberg/catalog/glue.mdx` — AWS Glue Catalog configuration.
  - `docs/writers/iceberg/catalog/rest.mdx` — REST Catalog configuration.
  - `docs/writers/iceberg/catalog/jdbc.mdx` — JDBC Catalog configuration.
  - `docs/writers/iceberg/catalog/hive.mdx` — Hive Metastore Catalog configuration.
  - `docs/writers/iceberg/partitioning.mdx` — Iceberg table data partitioning.
  - `docs/writers/iceberg/azure.mdx` — Storing Iceberg tables on Azure ADLS Gen2.
  - `docs/writers/iceberg/gcp.mdx` — Storing Iceberg tables on Google Cloud Storage.
  - `docs/writers/iceberg/troubleshooting-local.mdx` — Local Iceberg debugging and testing.
- **Parquet Writer (`docs/writers/parquet/`)**:
  - `docs/writers/parquet/config.mdx` — Parquet writer configuration.
  - `docs/writers/parquet/permission.mdx` — IAM permissions for Parquet writer.

## 5. Core Engine & Configuration
- `docs/core/configs/source.mdx` — General `source.json` structure.
- `docs/core/configs/destination.mdx` — General `destination.json` structure.
- `docs/core/configs/stream.mdx` — Stream and table selection config.

## 6. Monitoring & Maintenance
- `docs/monitoring-and-observability/` — Prometheus metrics, health checks, log outputs.
- `docs/fusion/` — OLake Fusion maintenance, compaction, and release notes.
