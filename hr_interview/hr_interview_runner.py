import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from hr_interview.interview_flow import InterviewFlow


def main():
    flow = InterviewFlow()
    flow.save(experience_level="Experienced", role_type="Technical")
    return flow


if __name__ == "__main__":
    main()