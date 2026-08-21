process GATK_BQSR {
    tag "$sample_id"
    publishDir "${params.outdir}/bqsr", mode: 'copy'

    input:
    tuple val(sample_id), path(bam), path(bai)
    path genome_fasta
    path genome_fai
    path genome_dict
    path known_sites
    path known_sites_idx

    output:
    tuple val(sample_id), path("${sample_id}.recal.bam"), path("${sample_id}.recal.bam.bai"), emit: bam
    path "${sample_id}.recal.table", emit: table

    script:
    """
    gatk BaseRecalibrator \\
        -I ${bam} \\
        -R ${genome_fasta} \\
        --known-sites ${known_sites} \\
        -O ${sample_id}.recal.table

    gatk ApplyBQSR \\
        -I ${bam} \\
        -R ${genome_fasta} \\
        --bqsr-recal-file ${sample_id}.recal.table \\
        -O ${sample_id}.recal.bam

    samtools index ${sample_id}.recal.bam
    """
}
