from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class VariantInfo:
    chrom: str
    pos: int
    ref: str
    alt: str
    gene: str
    consequence: str
    allele_frequency: float = 0.0
    clinvar_sig: Optional[str] = None
    in_silico_score: Optional[float] = None
    is_lof: bool = False
    
    @property
    def variant_id(self) -> str:
        return f"{self.chrom}:{self.pos}:{self.ref}:{self.alt}"

@dataclass
class ClassificationResult:
    variant: VariantInfo
    classification: str
    triggered_rules: List[str] = field(default_factory=list)
