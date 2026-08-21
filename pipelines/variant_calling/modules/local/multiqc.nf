process MULTIQC {
    tag "multiqc"
    publishDir "${params.outdir}/multiqc", mode: 'copy'

    input:
    path '*'  // all QC/log files collected from upstream processes

    output:
    path "multiqc_report.html"
    path "multiqc_data"

    script:
    """
    multiqc . --filename multiqc_report.html
    """
}
