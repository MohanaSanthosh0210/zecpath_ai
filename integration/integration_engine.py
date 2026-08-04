import json
from pathlib import Path

from integration.api_registry import APIRegistry
from integration.api_mapper import APIMapper
from integration.processing_strategy import ProcessingStrategy
from integration.authentication import Authentication
from integration.retry_policy import RetryPolicy


class IntegrationEngine:

    BASE_DIR = Path(__file__).resolve().parent

    OUTPUT_DIR = (
        BASE_DIR /
        "data" /
        "integration"
    )

    @staticmethod
    def generate():

        IntegrationEngine.OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        registry = APIRegistry.get_all_apis()

        mapping = APIMapper.generate_mapping()

        processing = (
            ProcessingStrategy.get_all_modes()
        )

        authentication = (
            Authentication.get_configuration()
        )

        retry = RetryPolicy.get_policy()

        with open(

            IntegrationEngine.OUTPUT_DIR /
            "api_registry_report.json",

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(
                registry,
                file,
                indent=4,
                ensure_ascii=False
            )

        with open(

            IntegrationEngine.OUTPUT_DIR /
            "processing_report.json",

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(
                processing,
                file,
                indent=4,
                ensure_ascii=False
            )

        with open(

            IntegrationEngine.OUTPUT_DIR /
            "authentication_report.json",

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(
                authentication,
                file,
                indent=4,
                ensure_ascii=False
            )

        summary = {

            "status":
                "Integration Planned",

            "total_apis":
                len(registry),

            "sync_modules":
                len(processing["sync"]),

            "async_modules":
                len(processing["async"]),

            "authentication":
                authentication["method"],

            "retry_policy":
                retry["max_retries"]

        }

        with open(

            IntegrationEngine.OUTPUT_DIR /
            "integration_summary.json",

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(
                summary,
                file,
                indent=4,
                ensure_ascii=False
            )

        return summary


if __name__ == "__main__":

    print(

        json.dumps(

            IntegrationEngine.generate(),

            indent=4

        )

    )