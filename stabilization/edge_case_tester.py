class EdgeCaseTester:

    TEST_CASES = [

        {

            "name": "Empty Resume",

            "resume": ""

        },

        {

            "name": "No Skills",

            "resume": {

                "skills": []

            }

        },

        {

            "name": "Zero Experience",

            "experience": 0

        },

        {

            "name": "High Experience",

            "experience": 25

        },

        {

            "name": "Negative Score",

            "score": -10

        },

        {

            "name": "Score Above 100",

            "score": 150

        }

    ]

    @staticmethod
    def run():

        report = []

        for case in (

            EdgeCaseTester.TEST_CASES

        ):

            report.append(

                {

                    "case":

                        case["name"],

                    "status":

                        "Executed"

                }

            )

        return report


if __name__ == "__main__":

    for item in (

        EdgeCaseTester.run()

    ):

        print(item)