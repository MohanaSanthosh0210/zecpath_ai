from behavior_analysis.confidence_analyzer import (
    ConfidenceAnalyzer
)

from behavior_analysis.sentiment_scorer import (
    SentimentScorer
)

sample_answer = """
I am confident in Python development.
I achieved excellent results.
"""

confidence = (
    ConfidenceAnalyzer()
    .analyze(sample_answer)
)

sentiment = (
    SentimentScorer.score(
        sample_answer
    )
)

print("\nCONFIDENCE\n")
print(confidence)

print("\nSENTIMENT\n")
print(sentiment)