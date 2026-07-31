import json
from pathlib import Path


class SecureStorage:

    @staticmethod
    def encrypt(data):

        """
        Placeholder encryption.
        Replace with AES/Fernet later.
        """

        return {

            "encrypted": True,

            "payload": data

        }

    @staticmethod
    def decrypt(data):

        if data.get("encrypted", False):

            return data["payload"]

        return data

    @staticmethod
    def store(

        filename,

        data,

        output_dir

    ):

        output_dir.mkdir(

            parents=True,

            exist_ok=True

        )

        filepath = output_dir / filename

        encrypted = SecureStorage.encrypt(data)

        with open(

            filepath,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                encrypted,

                file,

                indent=4,

                ensure_ascii=False

            )

        return filepath

    @staticmethod
    def retrieve(filepath):

        with open(

            filepath,

            "r",

            encoding="utf-8"

        ) as file:

            encrypted = json.load(file)

        return SecureStorage.decrypt(

            encrypted

        )


if __name__ == "__main__":

    base = Path(__file__).resolve().parent

    output = (

        base /

        "data" /

        "governance"

    )

    sample = {

        "candidate_id": "C001",

        "report": "Technical Interview Report"

    }

    file = SecureStorage.store(

        "secure_report.json",

        sample,

        output

    )

    print(

        SecureStorage.retrieve(

            file

        )

    )