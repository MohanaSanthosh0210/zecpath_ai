import json

from behavioral_intelligence.behavioral_confidence_engine import (
    BehavioralConfidenceEngine
)


def main():

    engine = BehavioralConfidenceEngine()

    report = engine.process()

    print(
        "\n======================================"
    )
    print(
        "   AI BEHAVIORAL INTELLIGENCE REPORT"
    )
    print(
        "======================================\n"
    )

    print(

        json.dumps(

            report,

            indent=4

        )

    )

    print(
        "\nBehavioral analysis completed successfully."
    )

    print(
        "Output saved to:"
    )

    print(
        "data/behavioral_analysis/behavioral_report.json"
    )


if __name__ == "__main__":

    main()