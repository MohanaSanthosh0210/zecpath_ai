from integration.api_registry import APIRegistry
from integration.processing_strategy import (
    ProcessingStrategy
)
from integration.authentication import (
    Authentication
)
from integration.retry_policy import (
    RetryPolicy
)
from integration.integration_engine import (
    IntegrationEngine
)


def test_integration():

    registry = (
        APIRegistry.get_all_apis()
    )

    processing = (
        ProcessingStrategy.get_all_modes()
    )

    auth = (
        Authentication.get_configuration()
    )

    retry = (
        RetryPolicy.get_policy()
    )

    summary = (
        IntegrationEngine.generate()
    )

    assert len(registry) > 0

    assert len(processing["sync"]) > 0

    assert len(processing["async"]) > 0

    assert auth["method"] == "Bearer Token"

    assert retry["max_retries"] == 3

    assert summary["status"] == "Integration Planned"

    print(
        "Integration Test Passed"
    )


if __name__ == "__main__":

    test_integration()