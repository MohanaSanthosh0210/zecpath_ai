import json
import os

from communication_evaluation.fluency_analyzer import (
    FluencyAnalyzer
)

from communication_evaluation.grammar_analyzer import (
    GrammarAnalyzer
)

from communication_evaluation.vocabulary_analyzer import (
    VocabularyAnalyzer
)

from communication_evaluation.clarity_analyzer import (
    ClarityAnalyzer
)

from communication_evaluation.filler_word_detector import (
    FillerWordDetector
)

from communication_evaluation.answer_structure_analyzer import (
    AnswerStructureAnalyzer
)


class CommunicationScorer:

    OUTPUT_FILE = (
        "data/communication/communication_score.json"
    )

    def calculate(

        self,

        answer

    ):

        fluency = FluencyAnalyzer.analyze(answer)

        grammar = GrammarAnalyzer.analyze(answer)

        vocabulary = VocabularyAnalyzer.analyze(answer)

        clarity = ClarityAnalyzer.analyze(answer)

        filler = FillerWordDetector.analyze(answer)

        structure = AnswerStructureAnalyzer.analyze(answer)

        # -----------------------------
        # Weighted Score
        # -----------------------------

        communication_score = round(

            (
                fluency["fluency_score"] * 0.20 +

                grammar["grammar_score"] * 0.20 +

                vocabulary["vocabulary_score"] * 0.15 +

                clarity["clarity_score"] * 0.15 +

                filler["filler_score"] * 0.15 +

                structure["structure_score"] * 0.15
            ),

            2

        )

        result = {

            "communication_score":

                communication_score,

            "fluency":

                fluency,

            "grammar":

                grammar,

            "vocabulary":

                vocabulary,

            "clarity":

                clarity,

            "filler_words":

                filler,

            "answer_structure":

                structure

        }

        os.makedirs(

            "data/communication",

            exist_ok=True

        )

        with open(

            self.OUTPUT_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                result,

                file,

                indent=4

            )

        return result