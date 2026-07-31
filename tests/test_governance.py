from security_governance.governance_engine import (
    GovernanceEngine
)


def test_governance():

    sample = {

        "candidate_id": "TEST001",

        "decision": "Selected",

        "consent": True

    }

    result = GovernanceEngine.evaluate(sample)

    assert (

        result["governance_status"]

        ==

        "Compliant"

    )

    print(

        "\nGovernance Test Passed."

    )


if __name__ == "__main__":

    test_governance()