"""
Day 43 Test

Tests the complete ethics review pipeline.
"""

from ethics_compliance.ethics_review_runner import (
    EthicsReviewRunner
)


def main():

    report = EthicsReviewRunner().run()

    assert report["consent"]["eligible"] is True

    assert (
        report["fairness"]["fairness_status"]
        == "PASS"
    )

    assert (
        report["compliance"]["status"]
        in [
            "READY",
            "PARTIALLY_READY"
        ]
    )

    print("\nEthics Review Test Passed.")


if __name__ == "__main__":

    main()