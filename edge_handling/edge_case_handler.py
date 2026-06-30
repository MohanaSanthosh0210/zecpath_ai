import os
import json

from edge_handling.audio_quality_detector import AudioQualityDetector
from edge_handling.language_mix_detector import LanguageMixDetector
from edge_handling.missing_answer_detector import MissingAnswerDetector
from edge_handling.background_noise_detector import BackgroundNoiseDetector

from edge_handling.clarification_engine import ClarificationEngine
from edge_handling.retry_manager import RetryManager
from edge_handling.safety_fallback import SafetyFallback


class EdgeCaseHandler:

    OUTPUT_FILE = (
        "data/edge_cases/edge_case_report.json"
    )

    def __init__(self):

        self.retry_manager = RetryManager()

    def analyze(self, transcript):

        report = {

            "audio_quality":
                AudioQualityDetector.detect(
                    transcript
                ),

            "language_mix":
                LanguageMixDetector.detect(
                    transcript
                ),

            "missing_answer":
                MissingAnswerDetector.detect(
                    transcript
                ),

            "background_noise":
                BackgroundNoiseDetector.detect(
                    transcript
                )

        }

        action = {

            "status": "Continue",

            "message": None

        }

        # ----------------------------------
        # Missing Answer
        # ----------------------------------

        if report["missing_answer"]:

            retry = self.retry_manager.retry(
                "Missing Answer"
            )

            if retry["status"] == "Retry":

                action = {

                    "status": "Retry",

                    "message":
                        ClarificationEngine.get_message(
                            "missing_answer"
                        )

                }

            else:

                action = SafetyFallback.execute(
                    "Repeated missing answers"
                )

        # ----------------------------------
        # Poor Audio
        # ----------------------------------

        elif report["audio_quality"]["audio_quality"] == "Poor":

            retry = self.retry_manager.retry(
                "Poor Audio"
            )

            if retry["status"] == "Retry":

                action = {

                    "status": "Retry",

                    "message":
                        ClarificationEngine.get_message(
                            "poor_audio"
                        )

                }

            else:

                action = SafetyFallback.execute(
                    "Repeated poor audio"
                )

        # ----------------------------------
        # Language Mixing
        # ----------------------------------

        elif report["language_mix"]["language_mix"]:

            action = {

                "status": "Clarification",

                "message":
                    ClarificationEngine.get_message(
                        "language_mix"
                    )

            }

        # ----------------------------------
        # Background Noise
        # ----------------------------------

        elif report["background_noise"]["background_noise"]:

            action = {

                "status": "Clarification",

                "message":
                    ClarificationEngine.get_message(
                        "background_noise"
                    )

            }

        final_report = {

            "edge_case_detection":
                report,

            "system_action":
                action

        }

        os.makedirs(
            "data/edge_cases",
            exist_ok=True
        )

        with open(
            self.OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                final_report,
                file,
                indent=4
            )

        return final_report