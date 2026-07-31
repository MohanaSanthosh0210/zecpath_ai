import json
from pathlib import Path

from security_governance.audit_logger import AuditLogger
from security_governance.consent_manager import ConsentManager
from security_governance.retention_policy import RetentionPolicy
from security_governance.secure_storage import SecureStorage
from security_governance.access_control import AccessControl


class GovernanceEngine:

    BASE_DIR = Path(__file__).resolve().parent

    OUTPUT_DIR = (
        BASE_DIR /
        "data" /
        "governance"
    )

    RETENTION_CONFIG = (
        BASE_DIR /
        "config" /
        "retention_policy.json"
    )

    @staticmethod
    def evaluate(candidate):

        GovernanceEngine.OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        # Consent
        consent = ConsentManager.verify(candidate)
        ConsentManager.save(
            consent,
            GovernanceEngine.OUTPUT_DIR
        )

        # Audit Log
        audit = AuditLogger.log_event(
            candidate["candidate_id"],
            "HIRING_EVALUATION",
            {
                "decision":
                candidate.get(
                    "decision",
                    "Unknown"
                )
            }
        )

        AuditLogger.save_log(
            audit,
            GovernanceEngine.OUTPUT_DIR
        )

        # Retention Policy
        policy = RetentionPolicy.load_policy(
            GovernanceEngine.RETENTION_CONFIG
        )

        retention = (
            RetentionPolicy.generate_report(
                policy
            )
        )

        RetentionPolicy.save(
            retention,
            GovernanceEngine.OUTPUT_DIR
        )

        # Secure Storage

        SecureStorage.store(
            "candidate_report.json",
            candidate,
            GovernanceEngine.OUTPUT_DIR
        )

        # Access Control

        access = AccessControl.check_access(
            "recruiter",
            "read"
        )

        summary = {

            "candidate_id":

                candidate["candidate_id"],

            "consent":

                consent,

            "retention_policy":

                retention,

            "access_control":

                access,

            "audit_status":

                "Logged",

            "storage":

                "Secured",

            "governance_status":

                "Compliant"

        }

        filepath = (
            GovernanceEngine.OUTPUT_DIR /
            "governance_summary.json"
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                summary,
                file,
                indent=4,
                ensure_ascii=False
            )

        return summary


if __name__ == "__main__":

    sample = {

        "candidate_id": "C001",

        "decision": "Selected",

        "consent": True

    }

    result = GovernanceEngine.evaluate(sample)

    print(
        json.dumps(
            result,
            indent=4
        )
    )