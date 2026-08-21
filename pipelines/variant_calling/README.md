# VarPipe-Dx — Phase 1: WES Variant Calling Pipeline

`FastQC → fastp → BWA-MEM → MarkDuplicates → BQSR → {GATK HaplotypeCaller, DeepVariant} → Joint Genotyping → Hard Filter → MultiQC`

## Quick start

```bash
# Fast dev iteration on a small chr21 subset
nextflow run main.nf -profile test,standard

# Full run
nextflow run main.nf -profile standard \
    --input samplesheet.csv \
    --genome_fasta /path/to/GRCh38.fa \
    --known_sites /path/to/dbsnp.vcf.gz

# Cloud (Phase 5) — fill in queue/bucket in conf/awsbatch.config first
nextflow run main.nf -profile awsbatch --input samplesheet.csv ...
```

`samplesheet.csv` format:

```csv
sample,fastq_1,fastq_2
sample01,/path/to/sample01_R1.fastq.gz,/path/to/sample01_R2.fastq.gz
```

## Known TODOs before this is a real run

This was scaffolded in a sandboxed environment without access to genomics data hosts (NCBI/EBI/GIAB), so a few things are stubbed and need attention on your machine:

1. **`conf/test.config` URLs are placeholders.** Swap in a real small chr21/chr22 subset — `nf-core/test-datasets` (branch `sarek`) is a good source, or subset your own GIAB HG002 BAM with `samtools view -b in.bam chr21 > chr21.bam` and convert back to FASTQ.
2. **Reference `.fai` / `.dict` are assumed pre-built.** Add a `SAMTOOLS_FAIDX` / `GATK CreateSequenceDictionary` process, or run those two commands once locally and point `--genome_fasta` at the prepped reference.
3. **`assets/samplesheet_test.csv` has placeholder URLs** — same as #1.
4. **DeepVariant + GATK calls aren't merged/compared yet.** That's intentional — comparing them against the GIAB truth set with `hap.py` is the Phase 1 benchmarking step, not part of the Nextflow DAG itself (it's normally run once per pipeline version). Suggested next file: `docs/benchmarking.md` with the `hap.py` commands and a results table.
5. **Not yet executed.** I don't have Nextflow or Java available in this sandbox to actually run it — please do a `-profile test,standard` dry run locally as the first sanity check, and share any errors and I'll help debug them.

## Design notes

- **CombineGVCFs over GenomicsDBImport** for joint genotyping — simpler for the small cohort sizes a portfolio project will realistically have. Swap in GenomicsDBImport + an interval list if you scale past ~50 samples.
- **Hard filtering over VQSR** — VQSR needs a much larger training cohort than this project will have. Worth a line in your write-up explaining this trade-off; it's a real judgment call, not a shortcut.
- **Both GATK and DeepVariant run on the same BQSR'd BAM**, so the `hap.py` comparison is an apples-to-apples caller comparison, not confounded by different preprocessing.
