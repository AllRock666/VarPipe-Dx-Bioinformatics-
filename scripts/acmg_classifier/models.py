from dataclasses import dataclass, field


@dataclass
class VariantInfo:
    chrom: str
    pos: int
    ref: str
    alt: str
    gene: str
    consequence: str
    allele_frequency: float = 0.0
    clinvar_sig: str | None = None
    in_silico_score: float | None = None
    is_lof: bool = False
    
    @property
    def variant_id(self) -> str:
        return f"{self.chrom}:{self.pos}:{self.ref}:{self.alt}"

@dataclass
class ClassificationResult:
    variant: VariantInfo
    classification: str
    triggered_rules: list[str] = field(default_factory=list)
