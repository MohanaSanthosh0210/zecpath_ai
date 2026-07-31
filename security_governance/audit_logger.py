import json
from pathlib import Path
from datetime import datetime


class AuditLogger:

    @staticmethod
    def log_event(

        candidate_id,

        event,

        details

    ):

        return {

            "timestamp":

                datetime.utcnow().isoformat(),

            "candidate_id":

                candidate_id,

            "event":

                event,

            "details":

                details

        }

    @staticmethod
    def save_log(

        audit_entry,

        output_dir

    ):

        output_dir.mkdir(

            parents=True,

            exist_ok=True

        )

        filepath = (

            output_dir /

            "audit_log.json"

        )

        logs = []

        if filepath.exists():

            with open(

                filepath,

                "r",

                encoding="utf-8"

            ) as file:

                logs = json.load(file)

        logs.append(audit_entry)

        with open(

            filepath,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                logs,

                file,

                indent=4,

                ensure_ascii=False

            )

        return filepath


if __name__ == "__main__":

    entry = AuditLogger.log_event(

        "C001",

        "HR_INTERVIEW_COMPLETED",

        {

            "score": 86

        }

    )

    print(entry)