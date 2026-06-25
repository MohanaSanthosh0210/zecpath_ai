import json
import os

from behavior_analysis.confidence_analyzer import (
    ConfidenceAnalyzer
)

from behavior_analysis.sentiment_scorer import (
    SentimentScorer
)


INPUT_DIR = "data/understood_answers"

OUTPUT_DIR = (
    "data/behavioral_reports"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


def get_response_pace(word_count):

    if word_count < 5:
        return "Very Short"

    elif word_count < 15:
        return "Short"

    elif word_count < 40:
        return "Normal"

    return "Long"


def generate_reports():

    analyzer = ConfidenceAnalyzer()

    for file_name in os.listdir(INPUT_DIR):

        if not file_name.endswith(".json"):
            continue

        input_file = os.path.join(
            INPUT_DIR,
            file_name
        )

        with open(
            input_file,
            "r",
            encoding="utf-8"
        ) as file:

            answer_data = json.load(file)

        answer = (
            answer_data
            .get(
                "structured_answer",
                {}
            )
            .get(
                "text",
                ""
            )
        )

        confidence = (
            analyzer.analyze(answer)
        )

        sentiment = (
            SentimentScorer.score(
                answer
            )
        )

        word_count = len(
            answer.split()
        )

        communication_strength = (
            "Strong"
            if confidence[
                "confidence_score"
            ] >= 80
            else
            "Moderate"
            if confidence[
                "confidence_score"
            ] >= 60
            else
            "Weak"
        )

        report = {

            "intent":
                answer_data.get(
                    "intent"
                ),

            "response_length":
                word_count,

            "response_pace":
                get_response_pace(
                    word_count
                ),

            "communication_strength":
                communication_strength,

            "confidence":
                confidence,

            "sentiment":
                sentiment
        }

        output_file = os.path.join(
            OUTPUT_DIR,
            file_name
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )

        print(
            f"Saved: {output_file}"
        )


if __name__ == "__main__":
    generate_reports()