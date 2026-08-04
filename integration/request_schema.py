import json
from pathlib import Path


class RequestSchema:

    SCHEMAS = {

        "resume_parser": {

            "candidate_id": "string",

            "resume_path": "string"

        },

        "ats_engine": {

            "candidate_id": "string",

            "resume_data": "object"

        },

        "screening_ai": {

            "candidate_id": "string",

            "ats_score": "number"

        },

        "hr_interview": {

            "candidate_id": "string",

            "transcript": "string"

        },

        "technical_interview": {

            "candidate_id": "string",

            "technical_answers": "array"

        },

        "behavior_ai": {

            "candidate_id": "string",

            "video_stream": "string"

        },

        "integrity_detection": {

            "candidate_id": "string",

            "session_logs": "object"

        },

        "machine_test_ai": {

            "candidate_id": "string",

            "submission_path": "string"

        },

        "hiring_intelligence": {

            "candidate_id": "string"

        }

    }

    @staticmethod
    def get_schema(module):

        return RequestSchema.SCHEMAS.get(module, {})


if __name__ == "__main__":

    print(

        json.dumps(

            RequestSchema.SCHEMAS,

            indent=4

        )

    )