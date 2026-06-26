class ScreeningReportBuilder:

    """
    Builds recruiter-friendly screening reports
    from outputs of Day 25, Day 26 and Day 27.
    """

    def __init__(
        self,
        understanding,
        screening_score,
        behavior
    ):

        self.understanding = understanding
        self.screening_score = screening_score
        self.behavior = behavior

    # --------------------------------------------------

    def build_strengths(self):

        strengths = []

        confidence = (
            self.behavior
            .get("confidence", {})
            .get("confidence_score", 0)
        )

        if confidence >= 80:
            strengths.append(
                "Strong communication confidence"
            )

        if (
            self.behavior.get(
                "communication_strength"
            ) == "Strong"
        ):
            strengths.append(
                "Strong communication skills"
            )

        skills = self.understanding.get(
            "skills",
            []
        )

        if skills:
            strengths.append(
                "Relevant technical skills confirmed"
            )

        experience = self.understanding.get(
            "experience"
        )

        if experience:
            strengths.append(
                f"Experience confirmed ({experience})"
            )

        sentiment = (
            self.behavior
            .get("sentiment", {})
            .get("sentiment")
        )

        if sentiment == "Positive":
            strengths.append(
                "Positive interview attitude"
            )

        return strengths

    # --------------------------------------------------

    def build_risks(self):

        risks = []

        confidence = (
            self.behavior
            .get("confidence", {})
            .get("confidence_score", 0)
        )

        if confidence < 60:
            risks.append(
                "Low confidence during interview"
            )

        sentiment = (
            self.behavior
            .get("sentiment", {})
            .get("sentiment")
        )

        if sentiment == "Negative":
            risks.append(
                "Negative communication tone"
            )

        if self.understanding.get(
            "vague_response"
        ):
            risks.append(
                "Candidate provided vague responses"
            )

        if self.understanding.get(
            "missing_details"
        ):
            risks.append(
                "Important information missing"
            )

        if self.understanding.get(
            "salary_expectation"
        ) is None:
            risks.append(
                "Salary expectation not provided"
            )

        if self.understanding.get(
            "availability"
        ) is None:
            risks.append(
                "Availability not provided"
            )

        return risks

    # --------------------------------------------------

    def build_missing_information(self):

        missing = []

        if self.understanding.get(
            "salary_expectation"
        ) is None:
            missing.append(
                "Salary Expectation"
            )

        if self.understanding.get(
            "availability"
        ) is None:
            missing.append(
                "Availability"
            )

        if not self.understanding.get(
            "skills"
        ):
            missing.append(
                "Technical Skills"
            )

        return missing

    # --------------------------------------------------

    def build_key_answers(self):

        return {
            "intent":
                self.understanding.get(
                    "intent"
                ),

            "skills":
                self.understanding.get(
                    "skills",
                    []
                ),

            "experience":
                self.understanding.get(
                    "experience"
                ),

            "salary_expectation":
                self.understanding.get(
                    "salary_expectation"
                ),

            "availability":
                self.understanding.get(
                    "availability"
                )
        }

    # --------------------------------------------------

    def build_report(self):

        report = {

            "candidate_id":

                self.screening_score.get(
                    "candidate_id",
                    "unknown"
                ),

            "overall_status":

                self.screening_score.get(
                    "status"
                ),

            "overall_screening_score":

                self.screening_score.get(
                    "final_screening_score"
                ),

            "communication_strength":

                self.behavior.get(
                    "communication_strength"
                ),

            "confidence_score":

                self.behavior
                .get("confidence", {})
                .get(
                    "confidence_score"
                ),

            "sentiment":

                self.behavior
                .get("sentiment", {})
                .get(
                    "sentiment"
                ),

            "key_answers":

                self.build_key_answers(),

            "strengths":

                self.build_strengths(),

            "risks":

                self.build_risks(),

            "missing_information":

                self.build_missing_information()
        }

        return report