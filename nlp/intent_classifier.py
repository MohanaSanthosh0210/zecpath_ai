class IntentClassifier:

    INTENTS = {
        "experience_information": [
            "experience",
            "worked",
            "years",
            "developed",
            "built"
        ],

        "skill_information": [
            "python",
            "java",
            "django",
            "flask",
            "fastapi",
            "react",
            "aws",
            "docker"
        ],

        "salary_information": [
            "salary",
            "lpa",
            "ctc",
            "package"
        ],

        "availability_information": [
            "notice",
            "join",
            "joining",
            "immediately"
        ],

        "education_information": [
            "degree",
            "btech",
            "mtech",
            "graduation",
            "education"
        ],

        "project_information": [
            "project",
            "application",
            "system",
            "developed"
        ]
    }

    @staticmethod
    def classify(answer):

        answer = answer.lower()

        scores = {}

        for intent, keywords in IntentClassifier.INTENTS.items():

            score = sum(
                1
                for keyword in keywords
                if keyword in answer
            )

            scores[intent] = score

        best_intent = max(
            scores,
            key=scores.get
        )

        if scores[best_intent] == 0:
            return "unknown"

        return best_intent

    @staticmethod
    def classify_with_confidence(answer):
        """Return intent and a simple confidence score (0-1).

        Confidence is computed from the raw keyword matches normalized
        by the number of keywords for the winning intent.
        """
        lower = answer.lower()

        scores = {}
        for intent, keywords in IntentClassifier.INTENTS.items():
            score = sum(1 for keyword in keywords if keyword in lower)
            scores[intent] = score

        best_intent = max(scores, key=scores.get)

        if scores[best_intent] == 0:
            return {"intent": "unknown", "confidence": 0.0}

        # normalize by number of known keywords for that intent
        max_possible = len(IntentClassifier.INTENTS[best_intent])
        confidence = scores[best_intent] / max_possible

        # scale into a slightly higher baseline so single-keyword matches
        # are not treated as zero-confidence
        confidence = 0.3 + 0.7 * confidence

        if confidence > 1.0:
            confidence = 1.0

        return {"intent": best_intent, "confidence": round(confidence, 2)}