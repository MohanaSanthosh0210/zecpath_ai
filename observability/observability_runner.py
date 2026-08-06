import json

from observability.observability_engine import (
    ObservabilityEngine
)


def main():

    summary = (

        ObservabilityEngine.generate_reports()

    )

    print("\n========== DAY 61 ==========\n")

    print(
        "AI Observability Reports Generated\n"
    )

    print(

        json.dumps(

            summary,

            indent=4

        )

    )


if __name__ == "__main__":

    main()