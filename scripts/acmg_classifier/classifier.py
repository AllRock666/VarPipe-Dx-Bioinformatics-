from .models import VariantInfo, ClassificationResult
from .rules import get_all_rules

class ACMGClassifier:
    def __init__(self):
        self.rules = get_all_rules()

    def classify(self, variant: VariantInfo) -> ClassificationResult:
        triggered = []
        for rule in self.rules:
            if rule.evaluate(variant):
                triggered.append(rule)

        triggered_names = [r.name for r in triggered]
        
        pathogenic_counts = {"VeryStrong": 0, "Strong": 0, "Moderate": 0, "Supporting": 0}
        benign_counts = {"StandAlone": 0, "Strong": 0, "Supporting": 0}

        for rule in triggered:
            if rule.pathogenicity == "Pathogenic":
                if rule.category in pathogenic_counts:
                    pathogenic_counts[rule.category] += 1
            else:
                if rule.category in benign_counts:
                    benign_counts[rule.category] += 1

        is_pathogenic = self._check_pathogenic(pathogenic_counts)
        is_likely_pathogenic = self._check_likely_pathogenic(pathogenic_counts)
        is_benign = self._check_benign(benign_counts)
        is_likely_benign = self._check_likely_benign(benign_counts)

        # Conflict resolution
        if (is_pathogenic or is_likely_pathogenic) and (is_benign or is_likely_benign):
            final_class = "Uncertain Significance (Conflict)"
        elif is_pathogenic:
            final_class = "Pathogenic"
        elif is_likely_pathogenic:
            final_class = "Likely Pathogenic"
        elif is_benign:
            final_class = "Benign"
        elif is_likely_benign:
            final_class = "Likely Benign"
        else:
            final_class = "Uncertain Significance"

        return ClassificationResult(variant=variant, classification=final_class, triggered_rules=triggered_names)

    def _check_pathogenic(self, counts: dict) -> bool:
        pvs1 = counts["VeryStrong"] >= 1
        strong = counts["Strong"]
        mod = counts["Moderate"]
        sup = counts["Supporting"]

        if pvs1 and (strong >= 1 or mod >= 2 or (mod == 1 and sup == 1) or sup >= 2):
            return True
        if strong >= 2:
            return True
        if strong == 1 and (mod >= 3 or (mod == 2 and sup >= 2) or (mod == 1 and sup >= 4)):
            return True
        return False

    def _check_likely_pathogenic(self, counts: dict) -> bool:
        pvs1 = counts["VeryStrong"] >= 1
        strong = counts["Strong"]
        mod = counts["Moderate"]
        sup = counts["Supporting"]

        if pvs1 and mod == 1:
            return True
        if strong == 1 and (1 <= mod <= 2):
            return True
        if strong == 1 and sup >= 2:
            return True
        if mod >= 3:
            return True
        if mod == 2 and sup >= 2:
            return True
        if mod == 1 and sup >= 4:
            return True
        return False

    def _check_benign(self, counts: dict) -> bool:
        if counts["StandAlone"] >= 1:
            return True
        if counts["Strong"] >= 2:
            return True
        return False

    def _check_likely_benign(self, counts: dict) -> bool:
        if counts["Strong"] == 1 and counts["Supporting"] >= 1:
            return True
        if counts["Supporting"] >= 2:
            return True
        return False
