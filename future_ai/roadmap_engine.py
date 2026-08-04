import json
from pathlib import Path


class RoadmapEngine:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG = (
        BASE_DIR /
        "config" /
        "roadmap.json"
    )

    OUTPUT_DIR = (
        BASE_DIR /
        "data" /
        "roadmap"
    )

    @staticmethod
    def load_roadmap():

        with open(
            RoadmapEngine.CONFIG,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    @staticmethod
    def generate():

        RoadmapEngine.OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
        )

        roadmap = (
        RoadmapEngine.load_roadmap()
        )

        report = {

            "status": "Generated",

            "total_phases": len(roadmap),

            "phases": roadmap

        }

        with open(

            RoadmapEngine.OUTPUT_DIR /
            "roadmap_report.json",

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                report,

                file,

                indent=4,

                ensure_ascii=False

            )

        summary = {

            "platform":

                "Zecpath AI",

            "roadmap_status":

                "Generated",

            "total_phases":

                len(roadmap),

            "future_focus": [

                "Video Analysis",

                "Emotion Detection",

                "AI Coaching",

             "Analytics Dashboard"

            ]

        }

        with open(

            RoadmapEngine.OUTPUT_DIR /
            "future_summary.json",

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                summary,

                file,

                indent=4,

                ensure_ascii=False

            )

        return report


if __name__ == "__main__":

    print(

        json.dumps(

            RoadmapEngine.generate(),

            indent=4

        )

    )