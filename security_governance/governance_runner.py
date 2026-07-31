from security_governance.governance_engine import (
    GovernanceEngine
)


def main():

    candidate = {

        "candidate_id": "C001",

        "decision": "Selected",

        "consent": True

    }

    GovernanceEngine.evaluate(candidate)

    print(

        "\nSecurity & Governance Completed Successfully."

    )


if __name__ == "__main__":

    main()