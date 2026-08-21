process BWA_MEM {
    tag "$sample_id"
    publishDir "${params.outdir}/aligned", mode: 'copy'

    input:
    tuple val(sample_id), path(reads)
    path genome_fasta
    path bwa_index // .amb .ann .bwt .pac .sa, built once upstream via BWA_INDEX

    output:
    tuple val(sample_id), path("${sample_id}.sorted.bam"), path("${sample_id}.sorted.bam.bai"), emit: bam

    script:
    """
    bwa mem -t ${task.cpus} \\
        -R '@RG\\tID:${sample_id}\\tSM:${sample_id}\\tPL:ILLUMINA\\tLB:${sample_id}' \\
        ${genome_fasta} ${reads[0]} ${reads[1]} \\
        | samtools sort -@ ${task.cpus} -o ${sample_id}.sorted.bam -
    samtools index ${sample_id}.sorted.bam
    """
}

process BWA_INDEX {
    tag "index"

    input:
    path genome_fasta

    output:
    path "${genome_fasta}.{amb,ann,bwt,pac,sa}", emit: index

    script:
    """
    bwa index ${genome_fasta}
    """
}
