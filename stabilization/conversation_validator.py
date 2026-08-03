class ConversationValidator:

    @staticmethod
    def validate(conversation):

        issues = []

        if not conversation:

            issues.append(
                "Conversation is empty."
            )

            return {

                "valid": False,

                "issues": issues

            }

        for index, message in enumerate(conversation):

            if not message.get("speaker"):

                issues.append(

                    f"Missing speaker at message {index}"

                )

            if not message.get("text"):

                issues.append(

                    f"Empty message at index {index}"

                )

        previous_question = None

        for message in conversation:

            if message.get("speaker") == "AI":

                question = message.get("text")

                if question == previous_question:

                    issues.append(

                        "Duplicate AI question detected."

                    )

                previous_question = question

        return {

            "valid": len(issues) == 0,

            "issues": issues

        }


if __name__ == "__main__":

    sample = [

        {

            "speaker": "AI",

            "text": "Tell me about yourself."

        },

        {

            "speaker": "Candidate",

            "text": "I recently graduated."

        }

    ]

    print(

        ConversationValidator.validate(

            sample

        )

    )