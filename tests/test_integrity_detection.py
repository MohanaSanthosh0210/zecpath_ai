from integrity_detection.integrity_framework import (
    IntegrityFramework
)

from integrity_detection.risk_engine import (
    RiskEngine
)


def run_test():

    framework = IntegrityFramework.describe()

    assert "signals" in framework

    assert "processing_pipeline" in framework

    level = RiskEngine.determine_level(62)

    assert level == "High"

    print("\nIntegrity Detection Test Passed.\n")

    print(framework)


if __name__ == "__main__":

    run_test()