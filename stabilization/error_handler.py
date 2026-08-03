import json
from pathlib import Path
from datetime import datetime


class ErrorHandler:

    @staticmethod
    def create_error(

        module,

        error_type,

        message

    ):

        return {

            "timestamp":

                datetime.utcnow().isoformat(),

            "module":

                module,

            "error_type":

                error_type,

            "message":

                message

        }

    @staticmethod
    def save(

        error,

        output_dir

    ):

        output_dir.mkdir(

            parents=True,

            exist_ok=True

        )

        filepath = (

            output_dir /

            "debugging_report.json"

        )

        errors = []

        if filepath.exists():

            with open(

                filepath,

                "r",

                encoding="utf-8"

            ) as file:

                errors = json.load(file)

        errors.append(error)

        with open(

            filepath,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                errors,

                file,

                indent=4,

                ensure_ascii=False

            )

        return filepath

    @staticmethod
    def handle(

        module,

        exception,

        output_dir

    ):

        error = ErrorHandler.create_error(

            module,

            type(exception).__name__,

            str(exception)

        )

        ErrorHandler.save(

            error,

            output_dir

        )

        return error


if __name__ == "__main__":

    base = Path(__file__).resolve().parent

    output = (

        base /

        "data" /

        "debugging"

    )

    try:

        10 / 0

    except Exception as e:

        print(

            ErrorHandler.handle(

                "Demo",

                e,

                output

            )

        )