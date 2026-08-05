import json

from performance.performance_engine import (
    PerformanceEngine
)


def main():

    summary = (
        PerformanceEngine.generate_reports()
    )

    print("\n========== DAY 60 ==========\n")

    print(
        "Performance Optimization Complete\n"
    )

    print(

        json.dumps(

            summary,

            indent=4

        )

    )


if __name__ == "__main__":

    main()