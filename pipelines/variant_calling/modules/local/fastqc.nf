process FASTQC {
    tag "$sample_id"
    publishDir "${params.outdir}/fastqc", mode: 'copy'

    input:
    tuple val(sample_id), path(reads)

    output:
    tuple val(sample_id), path("*_fastqc.{zip,html}"), emit: qc

    script:
    """
    fastqc -q --threads ${task.cpus} ${reads}
    """
}
