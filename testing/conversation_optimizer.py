import os
import json


class ConversationOptimizer:

    INPUT_FILE = (
        "data/conversation_flow/conversation_decision.json"
    )

    OUTPUT_FILE = (
        "data/optimized/optimized_conversation.json"
    )

    def optimize(self):

        with open(
            self.INPUT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            decision = json.load(file)

        state = decision.get(
            "state",
            "END"
        )

        optimized_flow = {

            "original_state":
                state,

            "optimized_state":
                state,

            "retry_enabled":
                False,

            "fallback_enabled":
                False

        }

        if state == "FOLLOW_UP":

            optimized_flow["retry_enabled"] = True

            optimized_flow["fallback_enabled"] = True

        elif state == "RETRY":

            optimized_flow["fallback_enabled"] = True

        os.makedirs(
            "data/optimized",
            exist_ok=True
        )

        with open(
            self.OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                optimized_flow,
                file,
                indent=4
            )

        return optimized_flow


if __name__ == "__main__":

    optimizer = ConversationOptimizer()

    result = optimizer.optimize()

    print(
        json.dumps(
            result,
            indent=4
        )
    )