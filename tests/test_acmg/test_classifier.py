import pytest
from scripts.acmg_classifier.models import VariantInfo
from scripts.acmg_classifier.classifier import ACMGClassifier

@pytest.fixture
def classifier():
    return ACMGClassifier()

def test_benign_standalone(classifier):
    # AF > 5% triggers BA1 (StandAlone Benign)
    variant = VariantInfo(chrom="chr1", pos=1000, ref="A", alt="T", gene="GENE1", consequence="missense_variant", allele_frequency=0.06)
    result = classifier.classify(variant)
    assert result.classification == "Benign"
    assert "BA1" in result.triggered_rules

def test_pathogenic_pvs1_pm2(classifier):
    # Null variant (PVS1) + absent from controls (PM2) => PVS1 (VeryStrong) + PM2 (Moderate) => Likely Pathogenic
    variant = VariantInfo(chrom="chr1", pos=1000, ref="A", alt="T", gene="GENE1", consequence="stop_gained", allele_frequency=0.00001)
    result = classifier.classify(variant)
    
    # 1 Very Strong + 1 Moderate -> Likely Pathogenic
    assert result.classification == "Likely Pathogenic"
    assert "PVS1" in result.triggered_rules
    assert "PM2" in result.triggered_rules

def test_uncertain_significance(classifier):
    # Just PM2 (Moderate) is not enough to classify as Likely Pathogenic
    variant = VariantInfo(chrom="chr1", pos=1000, ref="A", alt="T", gene="GENE1", consequence="missense_variant", allele_frequency=0.00001)
    result = classifier.classify(variant)
    assert result.classification == "Uncertain Significance"
    assert "PM2" in result.triggered_rules

def test_pathogenic_pvs1_pm2_pp3(classifier):
    # PVS1 (VeryStrong) + PM2 (Moderate) + PP3 (Supporting) => Pathogenic
    variant = VariantInfo(
        chrom="chr1", pos=1000, ref="A", alt="T", gene="GENE1", 
        consequence="stop_gained", allele_frequency=0.00001, in_silico_score=0.9
    )
    result = classifier.classify(variant)
    
    # 1 Very Strong + 1 Moderate + 1 Supporting -> Pathogenic
    assert result.classification == "Pathogenic"
    assert set(["PVS1", "PM2", "PP3"]).issubset(set(result.triggered_rules))
