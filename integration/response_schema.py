import json


class ResponseSchema:

    SCHEMAS = {

        "resume_parser": {

            "candidate_id": "string",

            "skills": "array",

            "education": "string",

            "experience": "number"

        },

        "ats_engine": {

            "ats_score": "number",

            "matched_skills": "array"

        },

        "screening_ai": {

            "screening_score": "number",

            "recommendation": "string"

        },

        "hr_interview": {

            "hr_score": "number"

        },

        "technical_interview": {

            "technical_score": "number"

        },

        "behavior_ai": {

            "behavior_score": "number"

        },

        "integrity_detection": {

            "integrity_score": "number"

        },

        "machine_test_ai": {

            "machine_test_score": "number"

        },

        "hiring_intelligence": {

            "overall_score": "number",

            "decision": "string"

        }

    }

    @staticmethod
    def get_schema(module):

        return ResponseSchema.SCHEMAS.get(module, {})


if __name__ == "__main__":

    print(

        json.dumps(

            ResponseSchema.SCHEMAS,

            indent=4

        )

    )