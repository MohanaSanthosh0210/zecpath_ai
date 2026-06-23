import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from nlp.answer_understanding_engine import (
    AnswerUnderstandingEngine
)

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

print(result)