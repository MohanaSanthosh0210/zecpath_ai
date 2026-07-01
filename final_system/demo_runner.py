import json
import os

from final_system.system_pipeline import AIScreeningPipeline


class DemoRunner:

    OUTPUT_FILE = (

        "data/final_demo/demo_output.json"

    )

    def run(self):

        pipeline = AIScreeningPipeline()

        data = pipeline.run()

        # -----------------------------
        # Candidate Summary
        # -----------------------------

        understood = data.get(
            "understood_answer"
        ) or {}

        screening = data.get(
            "screening_score"
        ) or {}

        behavior = data.get(
            "behavior_report"
        ) or {}

        report = data.get(
            "screening_report"
        ) or {}

        conversation = data.get(
            "conversation"
        ) or {}

        edge = data.get(
            "edge_case"
        ) or {}

        final_result = {

            "candidate": {

                "intent":

                    understood.get(
                        "intent"
                    ),

                "skills":

                    understood.get(
                        "skills"
                    ),

                "experience":

                    understood.get(
                        "experience"
                    )

            },

            "screening": {

                "score":

                    screening.get(
                        "final_screening_score"
                    ),

                "status":

                    screening.get(
                        "status"
                    )

            },

            "behavior": behavior,

            "screening_report": report,

            "conversation": conversation,

            "edge_case": edge

        }

        os.makedirs(

            "data/final_demo",

            exist_ok=True

        )

        with open(

            self.OUTPUT_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                final_result,

                file,

                indent=4

            )

        print(

            "\n========== AI SCREENING DEMO ==========\n"

        )

        print(

            json.dumps(

                final_result,

                indent=4

            )

        )

        print(

            "\nDemo saved to "

            "data/final_demo/demo_output.json"

        )


if __name__ == "__main__":

    DemoRunner().run()