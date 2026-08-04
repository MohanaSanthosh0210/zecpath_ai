import json

from future_ai.roadmap_engine import RoadmapEngine
from future_ai.innovation_proposal import InnovationProposal
from future_ai.architecture_planner import ArchitecturePlanner
from future_ai.scalability_planner import ScalabilityPlanner


def main():

    roadmap = RoadmapEngine.generate()

    innovation = InnovationProposal.generate()

    architecture = ArchitecturePlanner.generate()

    scalability = ScalabilityPlanner.generate()

    print("\n========== DAY 58 ==========")

    print("Future AI Roadmap Generated Successfully")

    print(

        json.dumps(

            {

                "roadmap_status":

                    roadmap["status"],

                "innovation":

                    innovation["title"],

                "future_modules":

                    len(

                        architecture["future_modules"]

                    ),

                "deployment":

                    scalability["deployment"]

            },

            indent=4

        )

    )


if __name__ == "__main__":

    main()