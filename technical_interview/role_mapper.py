import json
from pathlib import Path


class RoleMapper:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG_FILE = (
        BASE_DIR /
        "config" /
        "role_skill_mapping.json"
    )

    @staticmethod
    def load_roles():

        with open(
            RoleMapper.CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data["roles"]

    @staticmethod
    def get_role(role_name):

        roles = RoleMapper.load_roles()

        for role in roles:

            if role["role"].lower() == role_name.lower():

                return role

        return None


if __name__ == "__main__":

    role = RoleMapper.get_role("Python Developer")

    print(role)