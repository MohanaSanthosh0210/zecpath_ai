from reporting.report_generator import (
    generate_screening_reports
)


def main():

    print("\n" + "=" * 60)
    print(" AI SCREENING REPORT GENERATOR ")
    print("=" * 60)

    generate_screening_reports()

    print("\n" + "=" * 60)
    print(" Report generation completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()