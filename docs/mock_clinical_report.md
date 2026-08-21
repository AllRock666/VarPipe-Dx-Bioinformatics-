# Clinical Variant Report

**Patient ID**: PT-98273-A  
**Sample ID**: HG002-WES  
**Test Type**: Whole Exome Sequencing (WES) & RNA-seq Multi-Omics Panel  
**Date**: October 26, 2026  

---

## 1. Primary Findings (Pathogenic / Likely Pathogenic)

### Variant 1: `BRCA1` c.5266dupC (p.Gln1756Profs*74)
- **Genotype**: Heterozygous
- **Classification**: **PATHOGENIC**
- **ACMG/AMP Evidence Triggers**: 
  - `PVS1` (Very Strong): Frameshift variant in a gene where LOF is a known mechanism of disease.
  - `PM2` (Moderate): Absent from gnomAD controls.
- **Transcriptomic Impact (Multi-Omics)**:
  - **Significant Differential Expression detected.**
  - `log2FoldChange`: -2.1 (Downregulated)
  - `padj`: 1.2e-4
  - *Interpretation*: The variant appears to trigger nonsense-mediated decay (NMD) leading to a significant loss of transcript abundance compared to wild-type controls.

---

## 2. Variants of Uncertain Significance (VUS)

### Variant 2: `TP53` c.133T>A (p.Phe45Leu)
- **Genotype**: Heterozygous
- **Classification**: **VUS** (Variant of Uncertain Significance)
- **ACMG/AMP Evidence Triggers**: 
  - `PM2` (Moderate): Extremely low frequency in gnomAD.
  - `PP3` (Supporting): Multiple in silico predictors (REVEL, CADD) suggest deleterious effect.
- **Transcriptomic Impact (Multi-Omics)**:
  - No significant differential expression detected (`padj` > 0.05).
  - *Interpretation*: Transcript levels remain normal. Functional protein assays may be required to determine if the amino acid substitution impacts p53 function.

---

## 3. Methodology

*   **Variant Calling**: Performed using Nextflow, BWA-MEM, and GATK HaplotypeCaller + DeepVariant.
*   **Annotation**: Ensembl VEP (v110) and ANNOVAR (GRCh38).
*   **Transcriptomics**: Salmon pseudoalignment and DESeq2 differential expression analysis.
*   **Classification**: Proprietary automated ACMG/AMP rules engine (VarPipe-Dx v1.0).

*This report is mock-generated for demonstration purposes.*
