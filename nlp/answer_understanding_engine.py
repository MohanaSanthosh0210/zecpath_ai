import json
import os

from nlp.intent_classifier import IntentClassifier
from nlp.skill_extractor import SkillExtractor
from nlp.experience_extractor import ExperienceExtractor
from nlp.salary_extractor import SalaryExtractor
from nlp.availability_extractor import AvailabilityExtractor
from nlp.off_topic_detector import OffTopicDetector
from nlp.vague_detector import VagueDetector


class AnswerUnderstandingEngine:

    @staticmethod
    def understand(question, answer):
        # Extract individual pieces
        intent_info = IntentClassifier.classify_with_confidence(answer)

        skills = SkillExtractor.extract(answer)

        experience = ExperienceExtractor.extract(answer)

        salary = SalaryExtractor.extract(answer)

        availability = AvailabilityExtractor.extract(answer)

        off_topic = OffTopicDetector.detect(question, answer)

        vague = VagueDetector.detect(answer)

        # Missing details: short answers or missing expected info for intent
        tokens = answer.split()
        missing_by_length = len(tokens) < 5

        missing_by_intent = False
        if intent_info["intent"] == "experience_information" and not experience:
            missing_by_intent = True
        if intent_info["intent"] == "skill_information" and not skills:
            missing_by_intent = True

        missing_details = missing_by_length or missing_by_intent

        # Compute a composite confidence score from detectors
        # Start with intent confidence
        intent_conf = intent_info.get("confidence", 0.0)

        # skill score: more skills -> higher
        skill_conf = min(1.0, len(skills) / 3) if skills is not None else 0.0

        exp_conf = 0.9 if experience else 0.5
        avail_conf = 0.9 if availability else 0.7
        salary_conf = 0.9 if salary else 0.7

        off_topic_penalty = 0.0 if not off_topic else -0.4
        vague_penalty = -0.2 if vague else 0.0

        # weights chosen to prioritize intent + skills
        weights = {
            "intent": 0.45,
            "skill": 0.25,
            "experience": 0.15,
            "availability": 0.1,
            "salary": 0.05
        }

        raw_conf = (
            intent_conf * weights["intent"] +
            skill_conf * weights["skill"] +
            exp_conf * weights["experience"] +
            avail_conf * weights["availability"] +
            salary_conf * weights["salary"]
        )

        raw_conf = raw_conf + off_topic_penalty + vague_penalty
        confidence = max(0.0, min(1.0, round(raw_conf, 2)))

        structured_answer = {
            "text": answer,
            "tokens": tokens,
            "entities": {
                "skills": skills,
                "experience": experience,
                "availability": availability,
                "salary_expectation": salary
            },
            "intent": intent_info["intent"],
            "intent_confidence": intent_info.get("confidence", 0.0),
            "off_topic": off_topic,
            "vague": vague,
            "missing_details": missing_details
        }

        return {
            "intent": intent_info["intent"],
            "skills": skills,
            "experience": experience,
            "availability": availability,
            "salary_expectation": salary,
            "off_topic": off_topic,
            "missing_details": missing_details,
            "vague_response": vague,
            "confidence": confidence,
            "structured_answer": structured_answer
        }


def save_result(result, filename):

    os.makedirs(
        "data/understood_answers",
        exist_ok=True
    )

    path = (
        f"data/understood_answers/{filename}"
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            result,
            file,
            indent=4
        )

    print(f"Saved: {path}")


if __name__ == "__main__":

    question = (
        "Tell me about your Python experience."
    )

    answer = (
        "I have 2 years of experience in Python. "
        "I worked on Flask and Django projects."
    )

    result = (
        AnswerUnderstandingEngine
        .understand(
            question,
            answer
        )
    )

    save_result(
        result,
        "sample_answer.json"
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )