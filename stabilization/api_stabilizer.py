import json
from pathlib import Path


class APIStabilizer:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG = (

        BASE_DIR /

        "config" /

        "api_validation.json"

    )

    @staticmethod
    def load_rules():

        with open(

            APIStabilizer.CONFIG,

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(file)

    @staticmethod
    def validate(response):

        rules = APIStabilizer.load_rules()

        missing = []

        for field in rules["required_fields"]:

            if field not in response:

                missing.append(field)

        return {

            "valid": len(missing) == 0,

            "missing_fields": missing

        }


if __name__ == "__main__":

    response = {

        "status": "success",

        "score": 87,

        "recommendation": "Hire"

    }

    print(

        APIStabilizer.validate(

            response

        )

    )