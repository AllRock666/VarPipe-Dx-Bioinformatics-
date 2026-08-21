# VarPipe-Dx: Cloud Deployment & Compliance Architecture

## Target Architecture (AWS)

1. **Compute (Pipelines)**: 
   - **AWS Batch** executor mapped in Nextflow (`-profile awsbatch`). 
   - Each process spins up an EC2 spot/on-demand instance based on resource requirements (CPU/Memory) defined in `nextflow.config`.
2. **Storage (Data Lakes)**:
   - **Amazon S3**: Stores raw FASTQs, reference genomes, intermediate BAMs, and final VCFs. Nextflow natively interacts with S3 paths.
3. **Data Layer (API)**:
   - **Amazon RDS (PostgreSQL)**: Managed relational database for structured sample and variant tables.
   - **Amazon DocumentDB (MongoDB compatibility)**: For storing the deeply nested, schema-less VEP/ANNOVAR annotation JSON blobs.
4. **Compute (API & Dashboard)**:
   - **Amazon ECS / Fargate**: Runs the Dockerized FastAPI service and Streamlit dashboard.

## Compliance & Security (HIPAA Awareness)

Given the clinical nature of this pipeline, the following security constraints are applied to the cloud architecture:

1. **Encryption at Rest**:
   - All S3 buckets (raw data, results) enforce AES-256 (SSE-S3) or KMS-based (SSE-KMS) encryption.
   - RDS and DocumentDB volumes are encrypted at rest.
2. **Encryption in Transit**:
   - TLS 1.2+ is enforced for all API traffic (HTTPS via AWS ALB).
   - Database connections (RDS, DocumentDB) are strictly over TLS/SSL.
3. **Identity & Access Management (IAM) Least Privilege**:
   - AWS Batch execution roles only have access to specific S3 bucket prefixes (`arn:aws:s3:::varpipe-dx-bucket/project1/*`).
   - ECS task execution roles for the API only have read access to specific databases; they cannot modify pipeline runs.
4. **Audit Logging**:
   - AWS CloudTrail tracks all infrastructure API calls.
   - Nextflow execution logs (tower) and application logs (CloudWatch) are retained securely.
