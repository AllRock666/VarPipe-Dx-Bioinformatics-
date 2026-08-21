process HARD_FILTER {
    tag "cohort"
    publishDir "${params.outdir}/gatk/filtered", mode: 'copy'

    input:
    path cohort_vcf
    path cohort_vcf_tbi
    path genome_fasta
    path genome_fai
    path genome_dict

    output:
    path "cohort.filtered.vcf.gz", emit: vcf
    path "cohort.filtered.vcf.gz.tbi", emit: tbi

    script:
    // GATK-recommended hard-filter thresholds. VQSR needs a much larger cohort
    // (typically 30+ WGS samples) than a portfolio project will have, so hard
    // filtering is the appropriate choice here — worth calling out explicitly
    // in the write-up since a reviewer may ask why VQSR wasn't used.
    """
    gatk VariantFiltration \\
        -R ${genome_fasta} \\
        -V ${cohort_vcf} \\
        --filter-expression "QD < 2.0"              --filter-name "QD2" \\
        --filter-expression "FS > 60.0"              --filter-name "FS60" \\
        --filter-expression "MQ < 40.0"              --filter-name "MQ40" \\
        --filter-expression "MQRankSum < -12.5"      --filter-name "MQRankSum-12.5" \\
        --filter-expression "ReadPosRankSum < -8.0"  --filter-name "ReadPosRankSum-8" \\
        --filter-expression "SOR > 3.0"              --filter-name "SOR3" \\
        -O cohort.filtered.vcf.gz
    """
}
