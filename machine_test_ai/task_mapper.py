import json
from pathlib import Path


class TaskMapper:

    BASE_DIR = Path(__file__).resolve().parent

    TASK_FILE = (
        BASE_DIR /
        "config" /
        "task_types.json"
    )

    @staticmethod
    def load_task_types():

        with open(
            TaskMapper.TASK_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    @staticmethod
    def get_supported_tasks():

        tasks = TaskMapper.load_task_types()

        return [

            task["type"]

            for task in tasks["task_types"]

        ]


if __name__ == "__main__":

    print(

        TaskMapper.get_supported_tasks()

    )