import json
from pathlib import Path


class RetentionPolicy:

    @staticmethod
    def load_policy(config_path):

        with open(

            config_path,

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(file)

    @staticmethod
    def generate_report(policy):

        return {

            "transcripts_retention_days":

                policy["transcripts_days"],

            "reports_retention_days":

                policy["reports_days"],

            "audit_logs_retention_days":

                policy["audit_logs_days"],

            "auto_delete":

                policy["auto_delete"],

            "consent_required":

                policy["consent_required"]

        }

    @staticmethod
    def save(

        report,

        output_dir

    ):

        output_dir.mkdir(

            parents=True,

            exist_ok=True

        )

        filepath = (

            output_dir /

            "retention_policy_report.json"

        )

        with open(

            filepath,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                report,

                file,

                indent=4,

                ensure_ascii=False

            )

        return filepath


if __name__ == "__main__":

    base = Path(__file__).resolve().parent

    config = (

        base /

        "config" /

        "retention_policy.json"

    )

    policy = RetentionPolicy.load_policy(

        config

    )

    print(

        RetentionPolicy.generate_report(

            policy

        )

    )