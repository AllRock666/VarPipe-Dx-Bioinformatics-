process DEEPVARIANT {
    tag "$sample_id"
    publishDir "${params.outdir}/deepvariant", mode: 'copy'

    input:
    tuple val(sample_id), path(bam), path(bai)
    path genome_fasta
    path genome_fai

    output:
    tuple val(sample_id), path("${sample_id}.deepvariant.vcf.gz"), emit: vcf
    tuple val(sample_id), path("${sample_id}.deepvariant.g.vcf.gz"), emit: gvcf

    script:
    """
    /opt/deepvariant/bin/run_deepvariant \\
        --model_type=WES \\
        --ref=${genome_fasta} \\
        --reads=${bam} \\
        --output_vcf=${sample_id}.deepvariant.vcf.gz \\
        --output_gvcf=${sample_id}.deepvariant.g.vcf.gz \\
        --num_shards=${task.cpus}
    """
}
