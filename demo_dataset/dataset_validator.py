from pathlib import Path


class DatasetValidator:

    BASE_DIR = Path(__file__).resolve().parent

    REQUIRED = [

        "data/resumes",
        "data/job_descriptions",
        "data/interview_responses"

    ]

    @staticmethod
    def validate():

        missing = []

        for folder in DatasetValidator.REQUIRED:

            path = (
                DatasetValidator.BASE_DIR /
                folder
            )

            if (

                not path.exists()

                or

                len(
                    list(path.glob("*"))
                ) == 0

            ):

                missing.append(folder)

        return {

            "valid":

                len(missing) == 0,

            "missing":

                missing

        }


if __name__ == "__main__":

    result = DatasetValidator.validate()

    if result["valid"]:

        print(
            "Demo dataset validation successful."
        )

    else:

        print(
            "Missing dataset folders/files:"
        )

        for item in result["missing"]:

            print(
                f"- {item}"
            )