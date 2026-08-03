class PipelineValidator:

    REQUIRED_MODULES = [

        "ats",

        "screening",

        "hr",

        "technical",

        "behavior",

        "integrity",

        "machine_test",

        "recommendation"

    ]

    @staticmethod
    def validate(results):

        missing = []

        for module in (

            PipelineValidator.REQUIRED_MODULES

        ):

            if module not in results:

                missing.append(module)

                continue

            if results[module] is None:

                missing.append(module)

        return {

            "valid":

                len(missing) == 0,

            "missing_modules":

                missing

        }


if __name__ == "__main__":

    sample = {

        "ats": {},

        "screening": {},

        "hr": {},

        "technical": {},

        "behavior": {},

        "integrity": {},

        "machine_test": {},

        "recommendation": {}

    }

    print(

        PipelineValidator.validate(

            sample

        )

    )