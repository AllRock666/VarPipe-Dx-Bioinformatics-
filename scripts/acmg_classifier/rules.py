
from .models import VariantInfo


class ACMGRule:
    name: str = "Unknown"
    category: str = "Unknown" # 'VeryStrong', 'Strong', 'Moderate', 'Supporting', 'StandAlone'
    pathogenicity: str = "Pathogenic" # 'Pathogenic' or 'Benign'

    def evaluate(self, variant: VariantInfo) -> bool:
        raise NotImplementedError

class BA1(ACMGRule):
    name = "BA1"
    category = "StandAlone"
    pathogenicity = "Benign"

    def evaluate(self, variant: VariantInfo) -> bool:
        # Allele frequency > 5% in a general population
        return variant.allele_frequency > 0.05

class PM2(ACMGRule):
    name = "PM2"
    category = "Moderate"
    pathogenicity = "Pathogenic"

    def evaluate(self, variant: VariantInfo) -> bool:
        # Absent from controls (or at extremely low frequency)
        return variant.allele_frequency < 0.0001

class PVS1(ACMGRule):
    name = "PVS1"
    category = "VeryStrong"
    pathogenicity = "Pathogenic"

    def evaluate(self, variant: VariantInfo) -> bool:
        # Null variant in a gene where LOF is a known mechanism of disease
        lof_terms = {"frameshift_variant", "stop_gained", "splice_acceptor_variant", "splice_donor_variant"}
        return variant.consequence in lof_terms or variant.is_lof

class PP3(ACMGRule):
    name = "PP3"
    category = "Supporting"
    pathogenicity = "Pathogenic"
    
    def evaluate(self, variant: VariantInfo) -> bool:
        # Multiple lines of computational evidence support a deleterious effect
        if variant.in_silico_score is not None:
            return variant.in_silico_score > 0.8
        return False

class BP4(ACMGRule):
    name = "BP4"
    category = "Supporting"
    pathogenicity = "Benign"
    
    def evaluate(self, variant: VariantInfo) -> bool:
        # Multiple lines of computational evidence suggest no impact
        if variant.in_silico_score is not None:
            return variant.in_silico_score < 0.2
        return False

def get_all_rules() -> list[ACMGRule]:
    return [BA1(), PM2(), PVS1(), PP3(), BP4()]
