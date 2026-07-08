import json

from aptitude_evaluation.aptitude_engine import (
    AptitudeEngine
)


def main():

    engine = AptitudeEngine()

    report = engine.process()

    print(

        "\n==================================="

    )

    print(

        "      APTITUDE AI REPORT"

    )

    print(

        "===================================\n"

    )

    print(

        json.dumps(

            report,

            indent=4

        )

    )

    print(

        "\nReport saved to:\n"

        "data/aptitude/aptitude_report.json"

    )


if __name__ == "__main__":

    main()