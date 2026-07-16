class VagueAnswerDetector:

    """
    Detects whether a candidate response is
    vague or incomplete without over-triggering
    on short but meaningful answers.
    """

    VAGUE_PHRASES = [
        "i don't know",
        "not sure",
        "maybe",
        "i guess",
        "something like",
        "etc",
        "whatever",
        "nothing much",
        "can't remember",
    ]

    MINIMUM_WORDS = 8
    MINIMUM_CONTENT_WORDS = 4

    @classmethod
    def analyze(cls, answer):
        if not isinstance(answer, str):
            return {
                "is_vague": True,
                "is_incomplete": True,
                "matched_phrases": [],
                "word_count": 0,
            }

        normalized = answer.lower().strip()
        words = normalized.split()
        word_count = len(words)

        is_short = word_count < cls.MINIMUM_WORDS
        vague_phrases = [phrase for phrase in cls.VAGUE_PHRASES if phrase in normalized]

        has_meaningful_content = word_count >= cls.MINIMUM_CONTENT_WORDS and any(
            word not in {"i", "me", "my", "the", "a", "an", "and", "or"} for word in words
        )

        return {
            "is_vague": len(vague_phrases) > 0 and not has_meaningful_content,
            "is_incomplete": is_short and not has_meaningful_content,
            "matched_phrases": vague_phrases,
            "word_count": word_count,
        }


if __name__ == "__main__":

    answer = "Maybe I worked on Python."

    result = VagueAnswerDetector.analyze(

        answer

    )

    print(result)