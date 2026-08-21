process JOINT_GENOTYPING {
    tag "cohort"
    publishDir "${params.outdir}/gatk/joint", mode: 'copy'

    input:
    path gvcfs        // all per-sample .g.vcf.gz files
    path gvcf_indices // matching .tbi files
    path genome_fasta
    path genome_fai
    path genome_dict

    output:
    path "cohort.vcf.gz", emit: vcf
    path "cohort.vcf.gz.tbi", emit: tbi

    script:
    // CombineGVCFs is simpler than GenomicsDBImport for small cohorts (< ~50 samples),
    // which fits a portfolio-scale project. Switch to GenomicsDBImport + an interval
    // list if the cohort grows.
    def variant_args = gvcfs.collect { "-V ${it}" }.join(' ')
    """
    gatk CombineGVCFs \\
        -R ${genome_fasta} \\
        ${variant_args} \\
        -O combined.g.vcf.gz

    gatk GenotypeGVCFs \\
        -R ${genome_fasta} \\
        -V combined.g.vcf.gz \\
        -O cohort.vcf.gz
    """
}
