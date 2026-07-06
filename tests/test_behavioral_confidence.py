import json

from behavioral_intelligence.behavioral_confidence_engine import (
    BehavioralConfidenceEngine
)


def test_behavioral_engine():

    engine = BehavioralConfidenceEngine()

    report = engine.process()

    assert isinstance(report, dict)

    assert "confidence" in report

    assert "sentiment" in report

    assert "stress" in report

    assert "contradictions" in report

    assert "behavioral_confidence_score" in report

    assert (

        0 <=

        report["behavioral_confidence_score"]

        <= 100

    )

    print(

        "\nBehavioral Confidence Test Passed."

    )

    print(

        json.dumps(

            report,

            indent=4

        )

    )


if __name__ == "__main__":

    test_behavioral_engine()