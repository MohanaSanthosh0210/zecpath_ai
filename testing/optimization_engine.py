import json

from testing.threshold_optimizer import ThresholdOptimizer
from testing.conversation_optimizer import ConversationOptimizer


class OptimizationEngine:

    def run(self):

        threshold_result = (

            ThresholdOptimizer()

            .optimize()

        )

        conversation_result = (

            ConversationOptimizer()

            .optimize()

        )

        result = {

            "threshold_optimization":
                threshold_result,

            "conversation_optimization":
                conversation_result

        }

        print("\n========== OPTIMIZATION SUMMARY ==========\n")

        print(

            json.dumps(

                result,

                indent=4

            )

        )


if __name__ == "__main__":

    OptimizationEngine().run()