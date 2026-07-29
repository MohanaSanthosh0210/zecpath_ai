import json


class ReportBuilder:

    @staticmethod
    def build(profile, summary):

        report = {

            "candidate_id":
                profile.get(
                    "candidate_id",
                    "UNKNOWN"
                ),

            "role":
                profile.get(
                    "role",
                    "UNKNOWN"
                ),

            "ats_summary":
                profile.get(
                    "ats_summary",
                    {}
                ),

            "screening_summary":
                profile.get(
                    "screening_summary",
                    {}
                ),

            "hr_summary":
                profile.get(
                    "hr_summary",
                    {}
                ),

            "technical_summary":
                profile.get(
                    "technical_summary",
                    {}
                ),

            "behavior_summary":
                profile.get(
                    "behavior_summary",
                    {}
                ),

            "integrity_summary":
                profile.get(
                    "integrity_summary",
                    {}
                ),

            "overall_score":
                profile.get(
                    "overall_score",
                    {}
                ),

            "final_decision":
                profile.get(
                    "final_decision",
                    {}
                ),

            "executive_summary":
                summary.get(
                    "executive_summary",
                    ""
                )

        }

        return report


if __name__ == "__main__":

    try:
        from hiring_report.profile_builder import CandidateProfileBuilder
        from hiring_report.summary_generator import SummaryGenerator
    except ImportError:
        from profile_builder import CandidateProfileBuilder
        from summary_generator import SummaryGenerator

    profile = CandidateProfileBuilder.build({})

    summary = SummaryGenerator.generate(profile)

    print(

        json.dumps(

            ReportBuilder.build(
                profile,
                summary
            ),

            indent=4

        )

    )