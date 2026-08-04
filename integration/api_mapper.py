import json
from pathlib import Path

from integration.api_registry import APIRegistry
from integration.processing_strategy import ProcessingStrategy


class APIMapper:

    BASE_DIR = Path(__file__).resolve().parent

    OUTPUT_DIR = (
        BASE_DIR /
        "data" /
        "integration"
    )

    @staticmethod
    def generate_mapping():

        APIMapper.OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        mapping = []

        apis = APIRegistry.get_all_apis()

        for api in apis:

            mapping.append({

                "module":

                    api["module"],

                "endpoint":

                    api["endpoint"],

                "processing":

                    ProcessingStrategy.get_processing_mode(

                        api["module"]

                    )

            })

        report = {

            "total_modules":

                len(mapping),

            "api_mapping":

                mapping

        }

        with open(

            APIMapper.OUTPUT_DIR /
            "api_mapping.json",

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                report,

                file,

                indent=4,

                ensure_ascii=False

            )

        return report


if __name__ == "__main__":

    print(

        json.dumps(

            APIMapper.generate_mapping(),

            indent=4

        )

    )