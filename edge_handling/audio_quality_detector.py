class AudioQualityDetector:

    MIN_WORDS = 5

    @classmethod
    def detect(cls, transcript):

        if transcript is None:

            return {

                "audio_quality": "Poor",

                "reason": "Transcript missing"

            }

        words = transcript.split()

        if len(words) < cls.MIN_WORDS:

            return {

                "audio_quality": "Poor",

                "reason": "Very short transcript"

            }

        return {

            "audio_quality": "Good",

            "reason": "Transcript usable"

        }