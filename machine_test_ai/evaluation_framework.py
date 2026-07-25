from machine_test_ai.task_mapper import (
    TaskMapper
)

from machine_test_ai.scoring_strategy import (
    ScoringStrategy
)

from machine_test_ai.time_scoring import (
    TimeScoring
)

from machine_test_ai.output_capture import (
    OutputCapture
)


class EvaluationFramework:

    @staticmethod
    def describe():

        return {

            "supported_tasks":

                TaskMapper.get_supported_tasks(),

            "evaluation_metrics":

                list(

                    ScoringStrategy.get_weights().keys()

                ),

            "time_limits": {

                "easy":

                    TimeScoring.get_limit("easy"),

                "medium":

                    TimeScoring.get_limit("medium"),

                "hard":

                    TimeScoring.get_limit("hard"),

                "expert":

                    TimeScoring.get_limit("expert")

            },

            "captured_outputs":

                OutputCapture.describe()

        }


if __name__ == "__main__":

    import json

    print(

        json.dumps(

            EvaluationFramework.describe(),

            indent=4

        )

    )