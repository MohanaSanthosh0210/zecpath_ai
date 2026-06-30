class BackgroundNoiseDetector:

    NOISE_MARKERS = [

        "[noise]",

        "[music]",

        "[laughter]",

        "[silence]",

        "[static]",

        "<unk>"

    ]

    @classmethod
    def detect(cls, transcript):

        text = transcript.lower()

        count = 0

        for marker in cls.NOISE_MARKERS:

            count += text.count(

                marker.lower()

            )

        return {

            "background_noise":

                count > 0,

            "noise_markers":

                count

        }