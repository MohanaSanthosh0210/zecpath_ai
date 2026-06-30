import json

from edge_handling.documentation_generator import (

    DocumentationGenerator

)


def main():

    generator = DocumentationGenerator()

    documentation = generator.generate()

    print(

        "\n========== EDGE CASE DOCUMENTATION ==========\n"

    )

    print(

        json.dumps(

            documentation,

            indent=4

        )

    )

    print(

        "\nDocumentation saved to "

        "data/documentation/edge_case_documentation.json"

    )


if __name__ == "__main__":

    main()