# VarPipe-Dx: End-to-End Clinical Variant Interpretation & Multi-Omics Pipeline

VarPipe-Dx is a production-grade bioinformatics pipeline designed to ingest raw WES (Whole Exome Sequencing) and RNA-seq data, call and classify variants according to ACMG/AMP guidelines, and cross-reference variant-affected genes against expression data. The results are served through a queryable database and a clinical-style report.

This project is built to demonstrate proficiency in:
*   Variant calling & WES/WGS workflows
*   RNA-seq & differential expression analysis
*   ACMG/AMP variant classification
*   Workflow orchestration (Nextflow)
*   Bioinformatics tools: GATK, DeepVariant, VEP, ANNOVAR, MultiQC, FastQC, STAR/Salmon, DESeq2
*   Software Engineering: Python, FastAPI, PostgreSQL, MongoDB, Docker, GitHub Actions
*   Cloud Deployment & HPC awareness

## Project Structure

*   `pipelines/`: Nextflow workflows for variant calling and RNA-seq analysis.
*   `scripts/`: Python scripts for data processing, ACMG classification, and database loading.
*   `docs/`: Architecture diagrams, usage guides, and API documentation.
*   `tests/`: Unit and integration tests for the Python modules and pipelines.
*   `notebooks/`: Jupyter notebooks for exploratory data analysis and prototyping.
*   `.github/workflows/`: CI/CD pipelines.

## Phases

*   **Phase 0: Setup & Data**: Project skeleton, CI/CD, and data acquisition (GIAB HG002, public RNA-seq).
*   **Phase 1: Variant Calling Pipeline**: Nextflow pipeline for WES (FastQC -> BWA-MEM -> GATK/DeepVariant).
*   **Phase 2: Annotation & Classification**: VEP/ANNOVAR annotation and ACMG/AMP classification Python module.
*   **Phase 3: RNA-seq Differential Expression**: Nextflow pipeline for RNA-seq (STAR/Salmon -> DESeq2) and multi-omics integration.
*   **Phase 4: Data Layer & API**: PostgreSQL (relational data), MongoDB (annotations), and FastAPI query service.
*   **Phase 5: Cloud Deployment**: Dockerization, AWS Batch/GCP Life Sciences, S3/GCS, RDS.
*   **Phase 6: Documentation**: Architecture diagram, API Swagger docs, and mock clinical variant report.
*   **Phase 7 (Stretch): Dashboard**: Streamlit/React dashboard for QC and results.

## Quickstart

*(Instructions for setting up the environment, running the pipelines, and spinning up the API will be added here as the project evolves.)*
