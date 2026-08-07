from .feedback_collector import FeedbackCollector
from .qa_simulator import QASimulator
from .demo_evaluator import DemoEvaluator
from .readiness_checker import ReadinessChecker


class MockDemoRunner:

    @staticmethod
    def run():

        FeedbackCollector.generate()

        QASimulator.generate()

        DemoEvaluator.generate()

        ReadinessChecker.generate()

        print(

            "Mock demo assets generated successfully."

        )


if __name__ == "__main__":

    MockDemoRunner.run()