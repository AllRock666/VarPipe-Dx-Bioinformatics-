#!/usr/bin/env nextflow

/*
 * VarPipe-Dx :: Phase 3 — RNA-seq Differential Expression Pipeline
 */

process FASTQC {
    tag "$sample"
    publishDir "${params.outdir}/fastqc", mode: 'copy'

    input:
    tuple val(sample), path(reads)

    output:
    path "*_fastqc.{zip,html}", emit: qc

    script:
    """
    fastqc -q ${reads}
    """
}

process SALMON_INDEX {
    tag "salmon_index"

    input:
    path transcriptome

    output:
    path "salmon_index", emit: index

    script:
    """
    salmon index -t ${transcriptome} -i salmon_index
    """
}

process SALMON_QUANT {
    tag "$sample"
    publishDir "${params.outdir}/salmon", mode: 'copy'

    input:
    tuple val(sample), val(condition), path(reads)
    path index

    output:
    tuple val(sample), val(condition), path("${sample}_quant"), emit: quant

    script:
    """
    salmon quant -i ${index} -l A \\
        -1 ${reads[0]} -2 ${reads[1]} \\
        --validateMappings -o ${sample}_quant
    """
}

process DESEQ2 {
    publishDir "${params.outdir}/deseq2", mode: 'copy'

    input:
    path quant_dirs

    output:
    path "differential_expression_results.csv", emit: results
    path "volcano_plot.pdf", emit: plot, optional: true

    script:
    """
    # In a real pipeline, this would execute an R script passing the quant dirs
    # and a design matrix. For scaffolding, we create a placeholder.
    echo "gene,baseMean,log2FoldChange,lfcSE,stat,pvalue,padj" > differential_expression_results.csv
    echo "GENE1,100,2.5,0.1,25,1e-5,1e-4" >> differential_expression_results.csv
    echo "GENE2,50,-1.5,0.2,-7.5,0.01,0.05" >> differential_expression_results.csv
    
    echo "Running DESeq2 placeholder script..."
    """
}

workflow {
    if (!params.input) error "Please provide --input samplesheet_rnaseq.csv"
    if (!params.transcriptome) error "Please provide --transcriptome reference.fasta"

    transcriptome = file(params.transcriptome)

    // Build Index
    SALMON_INDEX(transcriptome)

    // Parse samplesheet
    // format: sample,condition,fastq_1,fastq_2
    reads_ch = Channel
        .fromPath(params.input)
        .splitCsv(header: true)
        .map { row -> 
            tuple(row.sample, row.condition, [file(row.fastq_1), file(row.fastq_2)]) 
        }

    // FastQC expects just sample name and reads
    qc_ch = reads_ch.map { sample, condition, reads -> tuple(sample, reads) }
    FASTQC(qc_ch)

    // Salmon Quant
    SALMON_QUANT(reads_ch, SALMON_INDEX.out.index)

    // Collect all quant dirs for DESeq2
    quant_dirs_ch = SALMON_QUANT.out.quant.map { sample, condition, path -> path }.collect()
    
    DESEQ2(quant_dirs_ch)
}
