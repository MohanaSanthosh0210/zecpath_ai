from adaptive_followup.followup_engine import FollowUpEngine
from adaptive_followup.vague_answer_detector import VagueAnswerDetector
from hr_scoring.relevance_scorer import RelevanceScorer
from transcripts.transcript_cleaner import clean_transcript


def test_followup_engine_is_stable_for_short_answers():
    engine = FollowUpEngine()
    decision = engine.decide("Tell me about your experience", "I worked on Python.", confidence_score=80)

    assert decision["trigger"]["trigger"] in {"Deepening", "Example", "Clarification"}
    assert decision["conversation"]["questions_asked"] >= 1


def test_vague_detector_reduces_false_positives():
    result = VagueAnswerDetector.analyze("I worked on Python and delivered a dashboard.")
    assert result["is_vague"] is False
    assert result["is_incomplete"] is False


def test_relevance_scorer_handles_confidence_more_gracefully():
    result = RelevanceScorer.calculate({
        "off_topic": False,
        "missing_details": False,
        "vague_response": False,
        "structured_answer": {"intent_confidence": 0.55},
    })
    assert result["relevance_score"] >= 80


def test_transcript_cleaner_removes_noise_without_overwriting_content():
    cleaned = clean_transcript("Um, I worked on FastAPI [noise] and like shipped features")
    assert "um" not in cleaned
    assert "fastapi" in cleaned
    assert "shipped" in cleaned
