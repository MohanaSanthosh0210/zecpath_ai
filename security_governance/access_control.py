import json
from pathlib import Path


class AccessControl:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG = (

        BASE_DIR /

        "config" /

        "access_roles.json"

    )

    @staticmethod
    def load_roles():

        with open(

            AccessControl.CONFIG,

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(file)

    @staticmethod
    def has_permission(

        role,

        permission

    ):

        roles = (

            AccessControl.load_roles()

        )["roles"]

        permissions = roles.get(

            role,

            []

        )

        return permission in permissions

    @staticmethod
    def check_access(

        role,

        permission

    ):

        allowed = AccessControl.has_permission(

            role,

            permission

        )

        return {

            "role": role,

            "permission": permission,

            "access":

                "Granted"

                if allowed

                else

                "Denied"

        }


if __name__ == "__main__":

    print(

        AccessControl.check_access(

            "admin",

            "delete"

        )

    )

    print(

        AccessControl.check_access(

            "viewer",

            "delete"

        )

    )