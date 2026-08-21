#!/usr/bin/env nextflow

/*
 * VarPipe-Dx :: Phase 1 — WES Variant Calling Pipeline
 *
 * Usage:
 *   nextflow run main.nf -profile test,standard          # quick dev run, small data
 *   nextflow run main.nf -profile standard \
 *       --input samplesheet.csv --genome_fasta ref.fa --known_sites dbsnp.vcf.gz
 *   nextflow run main.nf -profile awsbatch ...            # cloud run, Phase 5
 */

include { FASTQC                } from './modules/local/fastqc.nf'
include { FASTP                 } from './modules/local/fastp.nf'
include { BWA_INDEX; BWA_MEM    } from './modules/local/bwa_mem.nf'
include { MARK_DUPLICATES       } from './modules/local/mark_duplicates.nf'
include { GATK_BQSR             } from './modules/local/gatk_bqsr.nf'
include { GATK_HAPLOTYPECALLER  } from './modules/local/gatk_haplotypecaller.nf'
include { DEEPVARIANT           } from './modules/local/deepvariant.nf'
include { JOINT_GENOTYPING      } from './modules/local/joint_genotyping.nf'
include { HARD_FILTER           } from './modules/local/hard_filter.nf'
include { MULTIQC               } from './modules/local/multiqc.nf'

workflow {

    if (!params.input)        error "Please provide --input samplesheet.csv"
    if (!params.genome_fasta) error "Please provide --genome_fasta reference.fa"

    // ---- Reference prep ----------------------------------------------------
    genome_fasta = file(params.genome_fasta)
    genome_fai   = file("${params.genome_fasta}.fai")
    genome_dict  = file(params.genome_fasta.replaceAll(/\.fa(sta)?$/, '.dict'))
    known_sites     = file(params.known_sites)
    known_sites_idx = file("${params.known_sites}.tbi")

    BWA_INDEX(genome_fasta)

    // ---- Samplesheet --------------------------------------------------------
    reads_ch = Channel
        .fromPath(params.input)
        .splitCsv(header: true)
        .map { row -> tuple(row.sample, [file(row.fastq_1), file(row.fastq_2)]) }

    // ---- QC + trimming --------------------------------------------------------
    FASTQC(reads_ch)
    FASTP(reads_ch)

    // ---- Alignment --------------------------------------------------------
    BWA_MEM(FASTP.out.trimmed_reads, genome_fasta, BWA_INDEX.out.index)
    MARK_DUPLICATES(BWA_MEM.out.bam)
    GATK_BQSR(
        MARK_DUPLICATES.out.bam,
        genome_fasta, genome_fai, genome_dict,
        known_sites, known_sites_idx
    )

    // ---- Variant calling: run both callers for benchmarking -----------------
    if (params.run_gatk) {
        GATK_HAPLOTYPECALLER(GATK_BQSR.out.bam, genome_fasta, genome_fai, genome_dict)

        gvcfs     = GATK_HAPLOTYPECALLER.out.gvcf.map { it[1] }.collect()
        gvcf_tbis = GATK_HAPLOTYPECALLER.out.gvcf.map { it[2] }.collect()

        JOINT_GENOTYPING(gvcfs, gvcf_tbis, genome_fasta, genome_fai, genome_dict)
        HARD_FILTER(
            JOINT_GENOTYPING.out.vcf, JOINT_GENOTYPING.out.tbi,
            genome_fasta, genome_fai, genome_dict
        )
    }

    if (params.run_deepvariant) {
        DEEPVARIANT(GATK_BQSR.out.bam, genome_fasta, genome_fai)
    }
    // NOTE: benchmarking each caller's output against the GIAB truth set with
    // hap.py is a separate, deliberately non-Nextflow step (see docs/benchmarking.md)
    // since hap.py is typically run once per pipeline version, not per sample.

    // ---- Aggregate QC --------------------------------------------------------
    qc_files = FASTQC.out.qc.map { it[1] }
        .mix(FASTP.out.json)
        .mix(MARK_DUPLICATES.out.metrics)
        .mix(GATK_BQSR.out.table)
        .collect()

    MULTIQC(qc_files)
}
