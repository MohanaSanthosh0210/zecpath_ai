from behavior_analysis.hesitation_detector import (
    HesitationDetector
)

from behavior_analysis.uncertainty_detector import (
    UncertaintyDetector
)

from behavior_analysis.contradiction_detector import (
    ContradictionDetector
)


class ConfidenceAnalyzer:

    def analyze(self, answer):

        hesitation_count = (
            HesitationDetector.detect(
                answer
            )
        )

        uncertainty_count = (
            UncertaintyDetector.detect(
                answer
            )
        )

        contradictions = (
            ContradictionDetector.detect(
                answer
            )
        )

        confidence_score = 100

        confidence_score -= (
            hesitation_count * 10
        )

        confidence_score -= (
            uncertainty_count * 8
        )

        confidence_score -= (
            len(contradictions) * 15
        )

        confidence_score = max(
            0,
            confidence_score
        )

        return {

            "confidence_score":
                confidence_score,

            "hesitation_count":
                hesitation_count,

            "uncertainty_count":
                uncertainty_count,

            "contradictions":
                contradictions
        }
    