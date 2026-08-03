from stabilization.stabilization_engine import (
    StabilizationEngine
)


def test_stabilization():

    result = StabilizationEngine.run()

    assert result["system_status"] == "Stable"

    assert result["pipeline_valid"] is True

    assert result["conversation_valid"] is True

    assert result["api_valid"] is True

    print("Stabilization Test Passed")


if __name__ == "__main__":

    test_stabilization()