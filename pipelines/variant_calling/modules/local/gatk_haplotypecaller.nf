process GATK_HAPLOTYPECALLER {
    tag "$sample_id"
    publishDir "${params.outdir}/gatk/gvcf", mode: 'copy'

    input:
    tuple val(sample_id), path(bam), path(bai)
    path genome_fasta
    path genome_fai
    path genome_dict

    output:
    tuple val(sample_id), path("${sample_id}.g.vcf.gz"), path("${sample_id}.g.vcf.gz.tbi"), emit: gvcf

    script:
    """
    gatk HaplotypeCaller \\
        -I ${bam} \\
        -R ${genome_fasta} \\
        -ERC GVCF \\
        -O ${sample_id}.g.vcf.gz
    """
}
