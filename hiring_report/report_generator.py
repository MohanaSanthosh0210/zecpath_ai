import json

from hiring_report.profile_builder import (
    CandidateProfileBuilder
)

from hiring_report.summary_generator import (
    SummaryGenerator
)

from hiring_report.report_builder import (
    ReportBuilder
)

from hiring_report.export_formatter import (
    ExportFormatter
)


class HiringReportGenerator:

    @staticmethod
    def generate(candidate_data):

        profile = CandidateProfileBuilder.build(

            candidate_data

        )

        summary = SummaryGenerator.generate(

            profile

        )

        report = ReportBuilder.build(

            profile,

            summary

        )

        ExportFormatter.export(report)

        return report


if __name__ == "__main__":

    sample = {

        "candidate_id": "C001",

        "role": "Software Engineer",

        "ats_summary": {

            "score": 88

        },

        "screening_summary": {

            "score": 84

        },

        "hr_summary": {

            "score": 82

        },

        "technical_summary": {

            "score": 91

        },

        "behavior_summary": {

            "score": 86

        },

        "integrity_summary": {

            "score": 94

        },

        "overall_score": {

            "hiring_fit": 89

        },

        "final_decision": {

            "decision": "Selected"

        }

    }

    report = HiringReportGenerator.generate(

        sample

    )

    print(

        json.dumps(

            report,

            indent=4

        )

    )