import json


class LoadSimulator:

    @staticmethod
    def simulate():

        loads = [

            {
                "candidates": 10,
                "instances": 1,
                "expected_latency_ms": 450
            },

            {
                "candidates": 100,
                "instances": 2,
                "expected_latency_ms": 520
            },

            {
                "candidates": 500,
                "instances": 5,
                "expected_latency_ms": 650
            },

            {
                "candidates": 1000,
                "instances": 10,
                "expected_latency_ms": 800
            },

            {
                "candidates": 5000,
                "instances": 20,
                "expected_latency_ms": 1100
            }

        ]

        return {

            "simulation": loads

        }


if __name__ == "__main__":

    print(

        json.dumps(

            LoadSimulator.simulate(),

            indent=4

        )

    )