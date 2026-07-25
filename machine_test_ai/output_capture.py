class OutputCapture:

    @staticmethod
    def describe():

        return {

            "captured_outputs": [

                "submitted_code",

                "execution_result",

                "compiler_output",

                "runtime",

                "memory_usage"

            ]

        }


if __name__ == "__main__":

    print(

        OutputCapture.describe()

    )