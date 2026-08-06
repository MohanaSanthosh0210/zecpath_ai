import json
from datetime import datetime
from pathlib import Path


class AuditMonitor:

    BASE_DIR = Path(__file__).resolve().parent

    OUTPUT_FILE = (
        BASE_DIR /
        "data" /
        "observability" /
        "audit_report.json"
    )

    @staticmethod
    def log(

        candidate_id,

        decision,

        hiring_score,

        modified_by="AI"

    ):

        AuditMonitor.OUTPUT_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        record = {

            "timestamp":

                datetime.now().isoformat(),

            "candidate_id":

                candidate_id,

            "decision":

                decision,

            "hiring_score":

                hiring_score,

            "modified_by":

                modified_by

        }

        logs = []

        if AuditMonitor.OUTPUT_FILE.exists():

            with open(

                AuditMonitor.OUTPUT_FILE,

                "r",

                encoding="utf-8"

            ) as file:

                logs = json.load(file)

        logs.append(record)

        with open(

            AuditMonitor.OUTPUT_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                logs,

                file,

                indent=4

            )


if __name__ == "__main__":

    AuditMonitor.log(

        "C001",

        "Selected",

        91.4

    )

    print("Audit Entry Created")