#!/usr/bin/env bash
set -e

# VarPipe-Dx: Wrapper script to run VEP and ANNOVAR
# Usage: ./annotate_variants.sh <input.vcf> <output_prefix>

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input.vcf> <output_prefix>"
    exit 1
fi

INPUT_VCF=$1
OUTPUT_PREFIX=$2

echo "Running Ensembl VEP..."
vep -i $INPUT_VCF \
    -o ${OUTPUT_PREFIX}_vep.vcf \
    --vcf \
    --everything \
    --assembly GRCh38 \
    --offline \
    --fork 4

echo "Running ANNOVAR..."
table_annovar.py $INPUT_VCF humandb/ \
    -buildver hg38 \
    -out ${OUTPUT_PREFIX}_annovar \
    -remove -protocol refGene,clinvar_20221231,gnomad30_genome \
    -operation g,f,f \
    -nastring . \
    -vcfinput

echo "Annotation complete."
