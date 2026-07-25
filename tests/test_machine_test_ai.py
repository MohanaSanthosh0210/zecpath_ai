from machine_test_ai.evaluation_framework import (
    EvaluationFramework
)

from machine_test_ai.task_mapper import (
    TaskMapper
)


def run_test():

    framework = EvaluationFramework.describe()

    assert "supported_tasks" in framework

    assert "evaluation_metrics" in framework

    tasks = TaskMapper.get_supported_tasks()

    assert "coding_problem" in tasks

    print("\nMachine Test AI Test Passed.\n")

    print(framework)


if __name__ == "__main__":

    run_test()