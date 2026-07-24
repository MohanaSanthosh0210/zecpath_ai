from integrity_detection.signal_mapper import SignalMapper
from integrity_detection.risk_engine import RiskEngine
from integrity_detection.warning_engine import WarningEngine


class IntegrityFramework:

    @staticmethod
    def describe():

        return {

            "signals": SignalMapper.get_signal_names(),

            "risk_levels": [

                "Low",

                "Moderate",

                "High",

                "Critical"

            ],

            "warning_rules": (

                WarningEngine.get_actions()

            ),

            "processing_pipeline": [

                "Signal Collection",

                "Threshold Evaluation",

                "Pattern Recognition",

                "Risk Assessment",

                "Warning Generation",

                "Integrity Reporting"

            ]

        }


if __name__ == "__main__":

    import json

    print(

        json.dumps(

            IntegrityFramework.describe(),

            indent=4

        )

    )