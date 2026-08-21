process MARK_DUPLICATES {
    tag "$sample_id"
    publishDir "${params.outdir}/dedup", mode: 'copy'

    input:
    tuple val(sample_id), path(bam), path(bai)

    output:
    tuple val(sample_id), path("${sample_id}.dedup.bam"), path("${sample_id}.dedup.bam.bai"), emit: bam
    path "${sample_id}.dedup.metrics.txt", emit: metrics

    script:
    """
    gatk MarkDuplicates \\
        -I ${bam} \\
        -O ${sample_id}.dedup.bam \\
        -M ${sample_id}.dedup.metrics.txt

    samtools index ${sample_id}.dedup.bam
    """
}
