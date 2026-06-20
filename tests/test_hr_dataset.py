from data.hr_screening_questions.question_loader import (
    load_questions
)


questions = load_questions(
    "python_developer"
)

print("\nHR Screening Questions\n")

for q in questions:

    print(
        f"[{q['category']}] "
        f"{q['question']}"
    )