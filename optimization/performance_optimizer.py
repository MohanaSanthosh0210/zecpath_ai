import json
import time
from pathlib import Path


class PerformanceOptimizer:

    @staticmethod
    def benchmark(function):

        start = time.perf_counter()

        function()

        end = time.perf_counter()

        return round(

            end - start,

            4

        )

    @staticmethod
    def generate_report(

        module_name,

        execution_time

    ):

        return {

            "module": module_name,

            "execution_time_seconds":

                execution_time,

            "status":

                "PASS"

                if execution_time < 2

                else

                "WARNING"

        }

    @staticmethod
    def save(report, output_dir):

        output_dir.mkdir(

            parents=True,

            exist_ok=True

        )

        filepath = (

            output_dir /

            "performance_report.json"

        )

        with open(

            filepath,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                report,

                file,

                indent=4,

                ensure_ascii=False

            )

        return filepath


def demo():

    total = 0

    for i in range(100000):

        total += i


if __name__ == "__main__":

    execution = PerformanceOptimizer.benchmark(

        demo

    )

    report = PerformanceOptimizer.generate_report(

        "Optimization Demo",

        execution

    )

    print(report)