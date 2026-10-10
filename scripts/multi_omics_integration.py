#!/usr/bin/env python3
import argparse
import csv
import json
from typing import Any


def load_classified_variants(json_path: str) -> list[dict[str, Any]]:
    """Loads ACMG classified variants (mocked as JSON for this step)."""
    with open(json_path, 'r') as f:
        return json.load(f)

def load_deseq2_results(csv_path: str, padj_threshold: float = 0.05) -> dict[str, dict[str, Any]]:
    """Loads DESeq2 results and filters for significant DE genes."""
    de_genes = {}
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                padj = float(row['padj'])
                if padj < padj_threshold:
                    de_genes[row['gene']] = {
                        'log2FoldChange': float(row['log2FoldChange']),
                        'padj': padj
                    }
            except ValueError:
                continue
    return de_genes

def integrate_multi_omics(variants: list[dict[str, Any]], de_genes: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Cross-references pathogenic variants against differentially expressed genes."""
    integrated = []
    for variant in variants:
        gene = variant.get('gene')
        # Only care about Pathogenic / Likely Pathogenic variants for this report
        if variant.get('classification') in ["Pathogenic", "Likely Pathogenic"]:
            if gene in de_genes:
                merged = {**variant, **de_genes[gene]}
                merged['multi_omics_flag'] = "Pathogenic Variant + Significant DE"
                integrated.append(merged)
    return integrated

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-omics integration: Variants + DE Genes")
    parser.add_argument("--variants", required=True, help="JSON file containing classified variants")
    parser.add_argument("--deseq2", required=True, help="CSV file from DESeq2")
    parser.add_argument("--output", required=True, help="Output JSON for integrated results")
    args = parser.parse_args()

    variants = load_classified_variants(args.variants)
    de_genes = load_deseq2_results(args.deseq2)
    
    integrated_results = integrate_multi_omics(variants, de_genes)
    
    with open(args.output, 'w') as f:
        json.dump(integrated_results, f, indent=4)
        
    print(f"Integration complete. Found {len(integrated_results)} genes with pathogenic variants AND significant differential expression.")
